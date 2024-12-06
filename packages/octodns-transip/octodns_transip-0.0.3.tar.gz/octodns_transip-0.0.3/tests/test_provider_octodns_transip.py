#
#
#

from operator import itemgetter
from os.path import dirname, join
from unittest import TestCase
from unittest.mock import Mock, patch

from octodns.provider.yaml import YamlProvider
from octodns.record import Record
from octodns.zone import Zone

from octodns_transip import (
    DNSEntry,
    Nameserver,
    SupportsException,
    TransipConfigException,
    TransipException,
    TransIPHTTPError,
    TransipNewZoneException,
    TransipProvider,
    TransipRetrieveNameserverException,
    TransipRetrieveRecordsException,
    TransipSaveNameserverException,
    TransipSaveRecordsException,
    _attr_for_nameserver,
    _entries_for,
    _parse_to_fqdn,
)


def make_expected():
    expected = Zone("unit.tests.", [])
    source = YamlProvider("test", join(dirname(__file__), "config"))
    source.populate(expected)
    return expected


def make_mock():
    zone = make_expected()

    # Turn Zone.records into TransIP DNSEntries
    api_entries = []
    for record in zone.records:
        if record._type in TransipProvider.SUPPORTS:
            # Root records have '@' as name
            name = record.name
            if name == "":
                name = TransipProvider.ROOT_RECORD

            api_entries.extend(_entries_for(name, record))

    # Append bogus entry so test for record type not being in SUPPORTS is
    # executed. For 100% test coverage.
    api_entries.append(DNSEntry("@", "3600", "BOGUS", "ns.transip.nl"))

    return zone, api_entries


def make_mock_with_nameservers():
    zone = make_expected()

    # Turn Zone.records into TransIP DNSEntries
    api_entries = []
    root_ns_entries = []
    for record in zone.records:
        if record._type in TransipProvider.SUPPORTS:
            # Root records have '@' as name
            name = record.name
            if name == "" and record._type == "NS":
                for value in (
                    record.values
                    if hasattr(record, 'values')
                    else [record.value]
                ):
                    root_ns_entries.append(
                        Nameserver(
                            service={}, attrs=_attr_for_nameserver(value)
                        )
                    )
                continue
            if name == "":
                name = TransipProvider.ROOT_RECORD

            api_entries.extend(_entries_for(name, record))

    # Append bogus entry so test for record type not being in SUPPORTS is
    # executed. For 100% test coverage.
    api_entries.append(DNSEntry("@", "3600", "BOGUS", "ns.transip.nl"))

    return zone, api_entries, root_ns_entries


def make_mock_empty():
    mock = Mock()
    mock.return_value.domains.get.return_value.dns.list.return_value = []
    mock.return_value.domains.get.return_value.nameservers.list.return_value = (
        []
    )
    return mock


def make_domainmock_existing():
    mock = Mock()

    api_entries = []
    api_entries.append(DNSEntry("@", 300, "A", "1.2.3.4"))
    api_entries.append(DNSEntry("@", 300, "A", "1.2.3.5"))
    api_entries.append(DNSEntry("delete-me", 3600, "A", "1.1.1.1"))
    api_entries.append(DNSEntry("delete-me-too", 3600, "CNAME", "unit.tests."))

    mock.dns.list.return_value = api_entries
    mock.nameservers.list.return_value = make_mock_nameservers()

    return mock


def make_mock_nameservers():
    nameservers = []
    for value in [
        'ns0.transip.net',
        'ns1.transip.nl',
        'ns2.transip.eu',
        "2.2.2.2",
        "2601:644:500:e210:62f8:1dff:feb8:947a",
    ]:
        nameservers.append(
            Nameserver(service={}, attrs=_attr_for_nameserver(value))
        )

    return nameservers


def make_failing_mock(response_code):
    mock = Mock()
    mock.return_value.domains.get.side_effect = [
        TransIPHTTPError(str(response_code), response_code)
    ]
    mock.return_value.domains.get.return_value.dns.list.side_effect = [
        TransIPHTTPError(str(response_code), response_code)
    ]
    mock.return_value.domains.get.return_value.nameservers.list.side_effect = [
        TransIPHTTPError(str(response_code), response_code)
    ]
    return mock


def make_failing_mock_records(response_code):
    mock = make_mock_empty()
    mock.return_value.domains.get.return_value.dns.list.side_effect = [
        TransIPHTTPError(str(response_code), response_code)
    ]
    return mock


def make_failing_mock_nameservers(response_code):
    mock = make_mock_empty()
    mock.return_value.domains.get.return_value.nameservers.list.side_effect = [
        TransIPHTTPError(str(response_code), response_code)
    ]
    return mock


class TestTransipProvider(TestCase):
    bogus_key = "-----BEGIN RSA PRIVATE KEY-----Z-----END RSA PRIVATE KEY-----"

    @patch("octodns_transip.TransIP", make_mock_empty())
    def test_init(self):
        with self.assertRaises(TransipConfigException) as ctx:
            TransipProvider("test", "unittest")

        self.assertEqual(
            "Missing `key` or `key_file` parameter in config",
            str(ctx.exception),
        )

        # Those should work
        TransipProvider("test", "unittest", key=self.bogus_key)
        TransipProvider("test", "unittest", key_file="/fake/path")
        TransipProvider("test", "unittest", key_file="/fake/path")

    @patch("octodns_transip.TransIP", make_failing_mock(401))
    def test_populate_unauthenticated(self):
        # Unhappy Plan - Not authenticated
        provider = TransipProvider("test", "unittest", self.bogus_key)
        zone = Zone("unit.tests.", [])
        with self.assertRaises(TransipException):
            provider.populate(zone, True)

    @patch("octodns_transip.TransIP", make_failing_mock(404))
    def test_populate_new_zone_as_target(self):
        # Unhappy Plan - Zone does not exists
        # Will trigger an exception if provider is used as a target for a
        # non-existing zone
        provider = TransipProvider("test", "unittest", self.bogus_key)
        zone = Zone("notfound.unit.tests.", [])
        with self.assertRaises(TransipNewZoneException):
            provider.populate(zone, True)

    @patch("octodns_transip.TransIP", make_failing_mock_records(404))
    def test_populate_records_get_error(self):
        # Happy Plan - Error while retreiving nameservers
        # Will trigger an exception if provider is used as a target for a
        # non-existing zone

        provider = TransipProvider("test", "unittest", self.bogus_key)
        zone = Zone("unit.tests.", [])
        with self.assertRaises(TransipRetrieveRecordsException):
            provider.populate(zone, False)

    @patch("octodns_transip.TransIP", make_failing_mock_nameservers(404))
    def test_populate_nameserver_get_error(self):
        # Happy Plan - Error while retreiving nameservers
        # Will trigger an exception if provider is used as a target for a
        # non-existing zone

        provider = TransipProvider("test", "unittest", self.bogus_key)
        zone = Zone("unit.tests.", [])
        with self.assertRaises(TransipRetrieveNameserverException):
            provider.populate(zone, False)

    @patch("octodns_transip.TransIP", make_mock_empty())
    def test_populate_new_zone_not_target(self):
        # Happy Plan - Zone does not exists
        # Won't trigger an exception if provider is NOT used as a target for a
        # non-existing zone.
        provider = TransipProvider("test", "unittest", self.bogus_key)
        zone = Zone("notfound.unit.tests.", [])
        provider.populate(zone, False)

    @patch("octodns_transip.TransIP", make_failing_mock(404))
    def test_populate_zone_does_not_exist(self):
        # Happy Plan - Zone does not exists
        # Won't trigger an exception if provider is NOT used as a target for a
        # non-existing zone.
        provider = TransipProvider("test", "unittest", self.bogus_key)
        zone = Zone("notfound.unit.tests.", [])
        provider.populate(zone, False)

    @patch("octodns_transip.TransIP")
    def test_populate_zone_exists_not_target(self, mock_client):
        # Happy Plan - Populate
        source_zone, api_records, root_ns_entries = make_mock_with_nameservers()
        mock_client.return_value.domains.get.return_value.dns.list.return_value = (
            api_records
        )
        mock_client.return_value.domains.get.return_value.nameservers.list.return_value = (
            root_ns_entries
        )

        provider = TransipProvider("test", "unittest", self.bogus_key)
        zone = Zone("unit.tests.", [])

        exists = provider.populate(zone, False)

        self.assertTrue(exists, "populate should return True")

        # Due to the implementation of Record._equality_tuple() we can't do a
        # normal compare, as that ingores ttl's for example. We therefor use
        # the __repr__ to compare. We do need to filter out `.geo` attributes
        # that Transip doesn't support.
        expected = set()
        for r in source_zone.records:
            if r._type in TransipProvider.SUPPORTS:
                if hasattr(r, "geo"):
                    r.geo = None
                data = r.data
                # we want to ignore the octodns bits
                data.pop('octodns', None)
                expected.add(str(data))
        self.assertEqual({str(r.data) for r in zone.records}, expected)

    @patch("octodns_transip.TransIP", make_mock_empty())
    def test_populate_zone_exists_as_target(self):
        # Happy Plan - Even if the zone has no records the zone should exist
        provider = TransipProvider("test", "unittest", self.bogus_key)
        zone = Zone("unit.tests.", [])
        exists = provider.populate(zone, True)
        self.assertTrue(exists, "populate should return True")

    @patch("octodns_transip.TransIP")
    def test_populate_nameservers(self, mock_client):
        # Happy Plan - Zone loads

        mock_client.return_value.domains.get.return_value.nameservers.list.return_value = (
            make_mock_nameservers()
        )

        provider = TransipProvider("test", "unittest", self.bogus_key)
        zone = Zone("unit.tests.", [])
        success = provider.populate(zone, False, lenient=True)
        self.assertTrue(success, "populate should return True")

        self.assertEqual(
            1, len(zone.records), "zone.records should have 1 record"
        )

        firstRecord = zone.records.pop()

        self.assertEqual(firstRecord._type, "NS", "Record type should be NS")
        self.assertEqual(firstRecord.ttl, 3600, "TTL should be 3600")
        self.assertEqual(
            firstRecord.values,
            [
                '2.2.2.2.',
                '2601:644:500:e210:62f8:1dff:feb8:947a.',
                'ns0.transip.net.',
                'ns1.transip.nl.',
                'ns2.transip.eu.',
            ],
            "Values should match list",
        )

    @patch("octodns_transip.TransIP", make_mock_empty())
    def test_plan(self):
        # Test happy plan, only create
        provider = TransipProvider(
            "test", "unittest", self.bogus_key, strict_supports=False
        )

        plan = provider.plan(make_expected())

        self.assertIsNotNone(plan)
        self.assertEqual(22, plan.change_counts["Create"])
        self.assertEqual(0, plan.change_counts["Update"])
        self.assertEqual(0, plan.change_counts["Delete"])

    @patch("octodns_transip.TransIP")
    def test_apply(self, client_mock):
        # Test happy flow. Create all supported records

        provider = TransipProvider(
            "test", "unittest", self.bogus_key, strict_supports=False
        )

        plan = provider.plan(make_expected())
        self.assertIsNotNone(plan)
        provider.apply(plan)

        client_mock.return_value.domains.get.return_value.dns.replace.assert_called_once()
        client_mock.return_value.domains.get.return_value.nameservers.replace.assert_called_once()

        # These are the supported ones from tests/config/unit.test.yaml
        expected_entries = [
            {
                "name": "ignored",
                "expire": 3600,
                "type": "A",
                "content": "9.9.9.9",
            },
            {
                "name": "@",
                "expire": 3600,
                "type": "ALIAS",
                "content": "www.example.com.",
            },
            {
                "name": "@",
                "expire": 3600,
                "type": "CAA",
                "content": "0 issue ca.unit.tests",
            },
            {
                "name": "sub",
                "expire": 3600,
                "type": "NS",
                "content": "6.2.3.4.",
            },
            {
                "name": "sub",
                "expire": 3600,
                "type": "NS",
                "content": "7.2.3.4.",
            },
            {
                "name": "naptr",
                "expire": 600,
                "type": "NAPTR",
                "content": "10 100 S SIP+D2U !^.*$!sip:info@bar.example.com! .",
            },
            {
                "name": "naptr",
                "expire": 600,
                "type": "NAPTR",
                "content": "100 100 U SIP+D2U !^.*$!sip:info@bar.example.com! .",
            },
            {
                "name": "spf",
                "expire": 600,
                "type": "SPF",
                "content": "v=spf1 ip4:192.168.0.1/16-all",
            },
            {
                "name": "_srv._tcp",
                "expire": 600,
                "type": "SRV",
                "content": "10 20 30 foo-1.unit.tests.",
            },
            {
                "name": "_srv._tcp",
                "expire": 600,
                "type": "SRV",
                "content": "12 20 30 foo-2.unit.tests.",
            },
            {
                "name": "_pop3._tcp",
                "expire": 600,
                "type": "SRV",
                "content": "0 0 0 .",
            },
            {
                "name": "_imap._tcp",
                "expire": 600,
                "type": "SRV",
                "content": "0 0 0 .",
            },
            {
                "name": "sub.txt",
                "expire": 3600,
                "type": "NS",
                "content": "ns1.test.",
            },
            {
                "name": "sub.txt",
                "expire": 3600,
                "type": "NS",
                "content": "ns2.test.",
            },
            {
                "name": "subzone",
                "expire": 3600,
                "type": "NS",
                "content": "192.0.2.1.",
            },
            {
                "name": "subzone",
                "expire": 3600,
                "type": "NS",
                "content": "192.0.2.8.",
            },
            {
                "name": "tlsa",
                "expire": 3600,
                "type": "TLSA",
                "content": "1 1 1 ABABABABABABABABAB",
            },
            {
                "name": "tlsa",
                "expire": 3600,
                "type": "TLSA",
                "content": "2 0 2 ABABABABABABABABAC",
            },
            {
                "name": "txt",
                "expire": 600,
                "type": "TXT",
                "content": "Bah bah black sheep",
            },
            {
                "name": "txt",
                "expire": 600,
                "type": "TXT",
                "content": "have you any wool.",
            },
            {
                "name": "txt",
                "expire": 600,
                "type": "TXT",
                "content": (
                    "v=DKIM1;k=rsa;s=email;h=sha256;"
                    "p=A/kinda+of/long/string+with+numb3rs"
                ),
            },
            {
                "name": "cname",
                "expire": 300,
                "type": "CNAME",
                "content": "unit.tests.",
            },
            {
                "name": "excluded",
                "expire": 3600,
                "type": "CNAME",
                "content": "unit.tests.",
            },
            {
                "name": "www.sub",
                "expire": 300,
                "type": "A",
                "content": "2.2.3.6",
            },
            {
                "name": "included",
                "expire": 3600,
                "type": "CNAME",
                "content": "unit.tests.",
            },
            {
                "name": "mx",
                "expire": 300,
                "type": "MX",
                "content": "10 smtp-4.unit.tests.",
            },
            {
                "name": "mx",
                "expire": 300,
                "type": "MX",
                "content": "20 smtp-2.unit.tests.",
            },
            {
                "name": "mx",
                "expire": 300,
                "type": "MX",
                "content": "30 smtp-3.unit.tests.",
            },
            {
                "name": "mx",
                "expire": 300,
                "type": "MX",
                "content": "40 smtp-1.unit.tests.",
            },
            {
                "name": "aaaa",
                "expire": 600,
                "type": "AAAA",
                "content": "2601:644:500:e210:62f8:1dff:feb8:947a",
            },
            {"name": "@", "expire": 300, "type": "A", "content": "1.2.3.4"},
            {"name": "@", "expire": 300, "type": "A", "content": "1.2.3.5"},
            {"name": "www", "expire": 300, "type": "A", "content": "2.2.3.6"},
            {
                "name": "@",
                "expire": 3600,
                "type": "SSHFP",
                "content": "1 1 7491973e5f8b39d5327cd4e08bc81b05f7710b49",
            },
            {
                "name": "@",
                "expire": 3600,
                "type": "SSHFP",
                "content": "1 1 bf6b6825d2977c511a475bbefb88aad54a92ac73",
            },
            {
                "name": "ds",
                "expire": 300,
                "type": "DS",
                "content": "0 1 2 abcdef0123456",
            },
            {
                "name": "ds",
                "expire": 300,
                "type": "DS",
                "content": "1 1 2 abcdef0123456",
            },
        ]

        # Unpack from the transip library magic structure...
        seen_entries = [
            e.__dict__["_attrs"]
            for e in client_mock.return_value.domains.get.return_value.dns.replace.mock_calls[
                0
            ][
                1
            ][
                0
            ]
        ]
        self.assertEqual(
            sorted(expected_entries, key=itemgetter("name", "type", "expire")),
            sorted(seen_entries, key=itemgetter("name", "type", "expire")),
        )

        seen_nameservers = [
            e.__dict__["_attrs"]
            for e in client_mock.return_value.domains.get.return_value.nameservers.replace.mock_calls[
                0
            ][
                1
            ][
                0
            ]
        ]
        expected_nameservers = [
            {'hostname': 'ns0.transip.net', 'ipv4': '', 'ipv6': ''},
            {'hostname': 'ns1.transip.nl', 'ipv4': '', 'ipv6': ''},
            {'hostname': 'ns2.transip.eu', 'ipv4': '', 'ipv6': ''},
        ]
        self.assertEqual(
            sorted(
                expected_nameservers, key=itemgetter("hostname", "ipv4", "ipv6")
            ),
            sorted(
                seen_nameservers, key=itemgetter("hostname", "ipv4", "ipv6")
            ),
        )

    @patch("octodns_transip.TransIP")
    def test_plan_ipv4_nameservers(self, client_mock):
        provider = TransipProvider(
            "test", "unittest", self.bogus_key, strict_supports=False
        )

        expected = make_expected()

        record = Record.new(
            expected,
            "",
            {
                'type': "NS",
                'ttl': 3600,
                'values': ['2601:644:500:e210:62f8:1dff:feb8:947a.'],
            },
            lenient=True,
        )

        expected.add_record(record, replace=True)

        with self.assertRaises(SupportsException):
            plan = provider.plan(expected)
            self.assertIsNotNone(plan)

    @patch("octodns_transip.TransIP")
    def test_plan_ipv6_nameservers(self, client_mock):
        provider = TransipProvider(
            "test", "unittest", self.bogus_key, strict_supports=False
        )

        expected = make_expected()

        record = Record.new(
            expected,
            "",
            {'type': "NS", 'ttl': 3600, 'values': ['2.2.2.2.', '3.3.3.3.']},
        )

        expected.add_record(record, replace=True)

        with self.assertRaises(SupportsException):
            plan = provider.plan(expected)
            self.assertIsNotNone(plan)

    @patch("octodns_transip.TransIP")
    def test_apply_nameservers_ttl_only(self, client_mock):

        x, entries, nameservers = make_mock_with_nameservers()

        client_mock.return_value.domains.get.return_value.nameservers.list.return_value = (
            nameservers
        )

        provider = TransipProvider(
            "test", "unittest", self.bogus_key, strict_supports=False
        )
        provider.ROOT_NS_TTL = 0  # Enforce a diff from unit-test root NS ttl

        plan = provider.plan(make_expected())
        self.assertIsNotNone(plan)
        provider.apply(plan)

        client_mock.return_value.domains.get.return_value.dns.replace.assert_called_once()
        client_mock.return_value.domains.get.return_value.nameservers.replace.assert_not_called()

    @patch("octodns_transip.TransIP")
    def test_apply_nameservers_fail(self, client_mock):

        client_mock.return_value.domains.get.return_value.nameservers.replace.side_effect = [
            TransIPHTTPError(str(404), 404)
        ]

        provider = TransipProvider(
            "test", "unittest", self.bogus_key, strict_supports=False
        )
        provider.ROOT_NS_TTL = 0

        plan = provider.plan(make_expected())
        self.assertIsNotNone(plan)
        with self.assertRaises(TransipSaveNameserverException):
            provider.apply(plan)

    @patch("octodns_transip.TransIP")
    def test_apply_deletions(self, client_mock):
        domain_mock = make_domainmock_existing()
        client_mock.return_value.domains.get.return_value = domain_mock
        domain_mock.nameservers.list.return_value = []
        provider = TransipProvider(
            "test", "unittest", self.bogus_key, strict_supports=False
        )

        plan = provider.plan(make_expected())

        self.assertIsNotNone(plan)
        self.assertEqual(21, plan.change_counts["Create"])
        self.assertEqual(0, plan.change_counts["Update"])
        self.assertEqual(2, plan.change_counts["Delete"])

        provider.apply(plan)

        for e in domain_mock.dns.replace.mock_calls[0][1][0]:
            self.assertNotRegex(
                e.name,
                r'^delete-me.*$',
                "This record should be deleted, and be seen within the api call",
            )

    @patch("octodns_transip.TransIP")
    def test_apply_unsupported(self, client_mock):
        # This triggers the if supported statement to give 100% code coverage
        domain_mock = Mock()
        client_mock.return_value.domains.get.return_value = domain_mock
        domain_mock.dns.list.return_value = []
        domain_mock.nameservers.list.return_value = []
        provider = TransipProvider(
            "test", "unittest", self.bogus_key, strict_supports=False
        )

        plan = provider.plan(make_expected())
        self.assertIsNotNone(plan)

        # Test apply with only support for A records
        provider.SUPPORTS = set(("A"))

        provider.apply(plan)
        seen_entries = [
            e.__dict__["_attrs"]
            for e in domain_mock.dns.replace.mock_calls[0][1][0]
        ]
        expected_entries = [
            {
                "name": "ignored",
                "expire": 3600,
                "type": "A",
                "content": "9.9.9.9",
            },
            {
                "name": "www.sub",
                "expire": 300,
                "type": "A",
                "content": "2.2.3.6",
            },
            {"name": "@", "expire": 300, "type": "A", "content": "1.2.3.4"},
            {"name": "@", "expire": 300, "type": "A", "content": "1.2.3.5"},
            {"name": "www", "expire": 300, "type": "A", "content": "2.2.3.6"},
        ]
        self.assertEqual(
            sorted(seen_entries, key=itemgetter("name", "type", "expire")),
            sorted(expected_entries, key=itemgetter("name", "type", "expire")),
        )

    @patch("octodns_transip.TransIP")
    def test_apply_failure_on_not_found(self, client_mock):
        # Test unhappy flow. Trigger 'not found error' in apply stage
        # This should normally not happen as populate will capture it first
        # but just in case.
        domain_mock = Mock()
        domain_mock.dns.list.return_value = []
        domain_mock.nameservers.list.return_value = []
        client_mock.return_value.domains.get.side_effect = [
            domain_mock,
            TransIPHTTPError("Not Found", 404),
        ]
        provider = TransipProvider(
            "test", "unittest", self.bogus_key, strict_supports=False
        )

        plan = provider.plan(make_expected())

        with self.assertRaises(TransipException):
            provider.apply(plan)

    @patch("octodns_transip.TransIP")
    def test_apply_failure_on_error(self, client_mock):
        # Test unhappy flow. Trigger a unrecoverable error while saving
        domain_mock = Mock()
        domain_mock.dns.list.return_value = []
        domain_mock.nameservers.list.return_value = []
        domain_mock.dns.replace.side_effect = [
            TransIPHTTPError("Not Found", 500)
        ]
        client_mock.return_value.domains.get.return_value = domain_mock
        provider = TransipProvider(
            "test", "unittest", self.bogus_key, strict_supports=False
        )

        plan = provider.plan(make_expected())

        with self.assertRaises(TransipSaveRecordsException):
            provider.apply(plan)

    @patch("octodns_transip.TransIP")
    def test_apply_failure_on_error_nameserver(self, client_mock):
        # Test unhappy flow. Trigger a unrecoverable error while saving
        domain_mock = Mock()
        domain_mock.dns.list.return_value = []
        domain_mock.nameservers.list.return_value = []
        domain_mock.nameservers.replace.side_effect = [
            TransIPHTTPError("Not Found", 500)
        ]
        client_mock.return_value.domains.get.return_value = domain_mock
        provider = TransipProvider(
            "test", "unittest", self.bogus_key, strict_supports=False
        )

        plan = provider.plan(make_expected())

        with self.assertRaises(TransipSaveNameserverException):
            provider.apply(plan)


class TestParseFQDN(TestCase):
    def test_parse_fqdn(self):
        zone = Zone("unit.tests.", [])
        self.assertEqual("www.unit.tests.", _parse_to_fqdn("www", zone))
        self.assertEqual(
            "www.unit.tests.", _parse_to_fqdn("www.unit.tests.", zone)
        )
        self.assertEqual(
            "www.sub.sub.sub.unit.tests.",
            _parse_to_fqdn("www.sub.sub.sub", zone),
        )
        self.assertEqual("unit.tests.", _parse_to_fqdn("@", zone))
