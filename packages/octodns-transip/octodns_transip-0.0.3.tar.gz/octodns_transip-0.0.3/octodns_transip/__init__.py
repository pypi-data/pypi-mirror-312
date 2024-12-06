#
#
#

from collections import defaultdict, namedtuple
from logging import getLogger

from requests.utils import is_ipv4_address
from transip import TransIP
from transip.exceptions import TransIPHTTPError
from transip.v6.objects import DnsEntry, Nameserver
from urllib3.util.ssl_ import is_ipaddress

from octodns.provider import ProviderException, SupportsException
from octodns.provider.base import BaseProvider
from octodns.record import Record

# TODO: remove __VERSION__ with the next major version release
__version__ = __VERSION__ = '0.0.3'

DNSEntry = namedtuple('DNSEntry', ('name', 'expire', 'type', 'content'))


class TransipException(ProviderException):
    pass


class TransipConfigException(TransipException):
    pass


class TransipNewZoneException(TransipException):
    pass


class TransipRetrieveRecordsException(ProviderException):
    pass


class TransipRetrieveNameserverException(ProviderException):
    pass


class TransipSaveRecordsException(ProviderException):
    pass


class TransipSaveNameserverException(ProviderException):
    pass


class TransipProvider(BaseProvider):
    SUPPORTS_GEO = False
    SUPPORTS_DYNAMIC = False
    SUPPORTS_ROOT_NS = True
    SUPPORTS = set(
        (
            'A',
            'AAAA',
            'CNAME',
            'MX',
            'NS',
            'SRV',
            'SPF',
            'TXT',
            'SSHFP',
            'CAA',
            'TLSA',
            'NAPTR',
            'ALIAS',
            'DS',
        )
    )
    MIN_TTL = 120
    TIMEOUT = 15
    ROOT_RECORD = '@'

    # TransIP root nameservers don't have TTL configurable.
    # This value is enforced on root NS records to prevent TTL-only changes
    # See root NS handling in _process_desired_zone for more information
    ROOT_NS_TTL = 3600

    def __init__(self, id, account, key=None, key_file=None, *args, **kwargs):
        self.log = getLogger('TransipProvider[{}]'.format(id))
        self.log.debug('__init__: id=%s, account=%s, token=***', id, account)
        super().__init__(id, *args, **kwargs)

        if key_file is not None:
            self._client = TransIP(login=account, private_key_file=key_file)
        elif key is not None:
            self._client = TransIP(login=account, private_key=key)
        else:
            raise TransipConfigException(
                'Missing `key` or `key_file` parameter in config'
            )

    def populate(self, zone, target=False, lenient=False):
        '''
        Populate the zone with records in-place.
        '''
        self.log.debug(
            'populate: name=%s, target=%s, lenient=%s',
            zone.name,
            target,
            lenient,
        )

        before = len(zone.records)
        try:
            domain = self._client.domains.get(zone.name.strip('.'))

        except TransIPHTTPError as e:
            if e.response_code == 404 and target is False:
                # Zone not found in account, and not a target so just
                # leave an empty zone.
                return False
            elif e.response_code == 404 and target is True:
                self.log.warning('populate: Transip can\'t create new zones')
                raise TransipNewZoneException(
                    (
                        'populate: ({}) Transip used '
                        + 'as target for non-existing zone: {}'
                    ).format(e.response_code, zone.name)
                )
            else:
                self.log.error('populate: (%s) %s ', e.response_code, e.message)
                raise TransipException(
                    'Unhandled error: ({}) {}'.format(
                        e.response_code, e.message
                    )
                )

        # Retrieve dns records from transip api
        try:
            records = domain.dns.list()
            self.log.debug(
                'populate: found %s records for zone %s',
                len(records),
                zone.name,
            )
        except TransIPHTTPError as e:
            self.log.error('populate: (%s) %s ', e.response_code, e.message)
            raise TransipRetrieveRecordsException(
                (
                    'populate: ({}) failed to get ' + 'dns records for zone: {}'
                ).format(e.response_code, zone.name)
            )

        # Retrieve nameservers from transip api
        try:
            nameservers = domain.nameservers.list()
            self.log.debug(
                'populate: found %s root nameservers for zone %s',
                len(nameservers),
                zone.name,
            )
        except TransIPHTTPError as e:
            self.log.error('populate: (%s) %s ', e.response_code, e.message)
            raise TransipRetrieveNameserverException(
                (
                    'populate: ({}) failed to get '
                    + 'root nameservers for zone: {}'
                ).format(e.response_code, zone.name)
            )

        # If nameservers are found, add them as ROOT NS records
        if nameservers:
            values = []
            for ns in nameservers:
                if ns.hostname != '':
                    values.append(ns.hostname + '.')
                if ns.ipv4 != '':
                    values.append(ns.ipv4 + '.')
                if ns.ipv6 != '':
                    values.append(ns.ipv6 + '.')

            record = Record.new(
                zone,
                '',
                {'type': 'NS', 'ttl': self.ROOT_NS_TTL, 'values': values},
                source=self,
                lenient=lenient,
            )
            zone.add_record(record, lenient=lenient)
            zone.root_ns

        # If records are found, add them to the zone
        if records:
            values = defaultdict(lambda: defaultdict(list))
            for record in records:
                name = zone.hostname_from_fqdn(record.name)
                if name == self.ROOT_RECORD:
                    name = ''

                if record.type in self.SUPPORTS:
                    values[name][record.type].append(record)

            for name, types in values.items():
                for _type, records in types.items():
                    record = Record.new(
                        zone,
                        name,
                        _data_for(_type, records, zone),
                        source=self,
                        lenient=lenient,
                    )
                    zone.add_record(record, lenient=lenient)

        self.log.info(
            'populate:   found %s records', len(zone.records) - before
        )

        return True

    def _process_desired_zone(self, desired):

        for record in desired.records:
            if record._type == 'NS' and record.name == '':

                # Check values for FQDN, IP's are not supported
                values = record.values

                for value in values:
                    if is_ipaddress(value.strip(".")):
                        msg = f'ip address not supported for root NS value for {record.fqdn}'
                        raise SupportsException(f'{self.id}: {msg}')

                # TransIP root nameservers don't have TTL configurable.
                # Check if TTL differs and enforce our fixed value if needed.
                if record.ttl != self.ROOT_NS_TTL:
                    updated_record = record.copy()
                    updated_record.ttl = self.ROOT_NS_TTL
                    msg = f'TTL value not supported for root NS values for {record.fqdn}'
                    fallback = f'modified to fixed value ({self.ROOT_NS_TTL})'
                    # Not using self.supports_warn_or_except(msg, fallback)
                    # because strict_mode shouldn't be disabled just for an ignored value
                    # so always return a warning even in strict_mode
                    self.log.warning('%s; %s', msg, fallback)
                    desired.add_record(updated_record, replace=True)

        return super()._process_desired_zone(desired)

    def _apply(self, plan):
        desired = plan.desired
        changes = plan.changes
        self.log.debug('apply: zone=%s, changes=%d', desired.name, len(changes))

        try:
            domain = self._client.domains.get(plan.desired.name[:-1])
        except TransIPHTTPError as e:
            self.log.exception('_apply: getting the domain failed')
            raise TransipException(
                'Unhandled error: ({}) {}'.format(e.response_code, e.message)
            )

        for change in changes:
            record = change.record

            if record.name == '' and record._type == 'NS':
                values = record.values

                nameservers = []
                for value in values:
                    nameservers.append(
                        Nameserver(
                            domain.nameservers, _attr_for_nameserver(value)
                        )
                    )
                try:
                    domain.nameservers.replace(nameservers)
                except TransIPHTTPError as e:
                    self.log.warning(
                        '_apply: Set Nameservers returned one or more errors: {}'.format(
                            e
                        )
                    )
                    raise TransipSaveNameserverException(
                        'Unhandled error: ({}) {}'.format(
                            e.response_code, e.message
                        )
                    )

        records = []
        for record in plan.desired.records:
            if record._type in self.SUPPORTS:
                # Root records have '@' as name
                name = record.name
                if name == '' and record._type == 'NS':
                    continue
                if name == '':
                    name = self.ROOT_RECORD

                records.extend(_entries_for(name, record))

        # Transform DNSEntry namedtuples into transip.v6.objects.DnsEntry
        # objects, which is a bit ugly because it's quite a magical object.
        api_records = [DnsEntry(domain.dns, r._asdict()) for r in records]
        try:
            domain.dns.replace(api_records)
        except TransIPHTTPError as e:
            self.log.warning(
                '_apply: Set DNS returned one or more errors: {}'.format(e)
            )
            raise TransipSaveRecordsException(
                'Unhandled error: ({}) {}'.format(e.response_code, e.message)
            )


def _data_for(type_, records, current_zone):
    if type_ == 'CNAME' or type_ == 'ALIAS':
        return {
            'type': type_,
            'ttl': records[0].expire,
            'value': _parse_to_fqdn(records[0].content, current_zone),
        }

    def format_mx(record):
        preference, exchange = record.content.split(' ', 1)
        return {
            'preference': preference,
            'exchange': _parse_to_fqdn(exchange, current_zone),
        }

    def format_srv(record):
        priority, weight, port, target = record.content.split(' ', 3)
        return {
            'port': port,
            'priority': priority,
            'target': _parse_to_fqdn(target, current_zone),
            'weight': weight,
        }

    def format_sshfp(record):
        algorithm, fp_type, fingerprint = record.content.split(' ', 2)
        return {
            'algorithm': algorithm,
            'fingerprint': fingerprint.lower(),
            'fingerprint_type': fp_type,
        }

    def format_caa(record):
        flags, tag, value = record.content.split(' ', 2)
        return {'flags': flags, 'tag': tag, 'value': value}

    def format_txt(record):
        return record.content.replace(';', '\\;')

    def format_tlsa(record):
        (
            certificate_usage,
            selector,
            matching_type,
            certificate_association_data,
        ) = record.content.split(' ', 4)
        return {
            'certificate_usage': certificate_usage,
            'selector': selector,
            'matching_type': matching_type,
            'certificate_association_data': certificate_association_data,
        }

    def format_naptr(record):
        order, preference, flags, service, regexp, replacement = (
            record.content.split(' ', 6)
        )
        return {
            'order': order,
            'preference': preference,
            'flags': flags,
            'service': service,
            'regexp': regexp,
            'replacement': replacement,
        }

    def format_ds(record):
        key_tag, algorithm, digest_type, digest = record.content.split(' ', 4)
        return {
            'key_tag': key_tag,
            'algorithm': algorithm,
            'digest_type': digest_type,
            'digest': digest,
        }

    value_formatter = {
        'MX': format_mx,
        'SRV': format_srv,
        'SSHFP': format_sshfp,
        'CAA': format_caa,
        'TXT': format_txt,
        'TLSA': format_tlsa,
        'NAPTR': format_naptr,
        'DS': format_ds,
    }.get(type_, lambda r: r.content)

    return {
        'type': type_,
        'ttl': _get_lowest_ttl(records),
        'values': [value_formatter(r) for r in records],
    }


def _parse_to_fqdn(value, current_zone):
    # TransIP allows '@' as value to alias the root record.
    # this provider won't set an '@' value, but can be an existing record
    if value == TransipProvider.ROOT_RECORD:
        value = current_zone.name

    if value[-1] != '.':
        value = '{}.{}'.format(value, current_zone.name)

    return value


def _get_lowest_ttl(records):
    return min([r.expire for r in records] + [100000])


def _entries_for(name, record):
    values = record.values if hasattr(record, 'values') else [record.value]

    def entry_mx(v):
        return f'{v.preference} {v.exchange}'

    def entry_srv(v):
        return f'{v.priority} {v.weight} {v.port} {v.target}'

    def entry_sshfp(v):
        return f'{v.algorithm} {v.fingerprint_type} {v.fingerprint}'

    def entry_caa(v):
        return f'{v.flags} {v.tag} {v.value}'

    def entry_txt(v):
        return v.replace('\\;', ';')

    def entry_tlsa(v):
        return f'{v.certificate_usage} {v.selector} {v.matching_type} {v.certificate_association_data}'

    def entry_naptr(v):
        return f'{v.order} {v.preference} {v.flags} {v.service} {v.regexp} {v.replacement}'

    def entry_ds(v):
        return f'{v.key_tag} {v.algorithm} {v.digest_type} {v.digest}'

    formatter = {
        'MX': entry_mx,
        'SRV': entry_srv,
        'SSHFP': entry_sshfp,
        'CAA': entry_caa,
        'TXT': entry_txt,
        'TLSA': entry_tlsa,
        'NAPTR': entry_naptr,
        'DS': entry_ds,
    }.get(record._type, lambda r: r)

    return [
        DNSEntry(name, record.ttl, record._type, formatter(value))
        for value in values
    ]


def _attr_for_nameserver(nameserver):
    nameserver = nameserver.strip('.')
    return {
        'hostname': nameserver if not is_ipaddress(nameserver) else '',
        'ipv4': nameserver if is_ipv4_address(nameserver) else '',
        'ipv6': (
            nameserver
            if is_ipaddress(nameserver) and not is_ipv4_address(nameserver)
            else ''
        ),
    }
