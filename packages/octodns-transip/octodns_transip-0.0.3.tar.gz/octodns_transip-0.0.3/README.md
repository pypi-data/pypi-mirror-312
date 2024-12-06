## Transip DNS provider for octoDNS

An [octoDNS](https://github.com/octodns/octodns/) provider that targets [Transip DNS](https://www.transip.eu/knowledgebase/entry/155-dns-and-nameservers/).

### Installation

#### Command line

```
pip install octodns-transip
```

#### requirements.txt/setup.py

Pinning specific versions or SHAs is recommended to avoid unplanned upgrades.

##### Versions

```
# Start with the latest versions and don't just copy what's here
octodns==0.9.14
octodns-transip==0.0.1
```

##### SHAs

```
# Start with the latest/specific versions and don't just copy what's here
-e git+https://git@github.com/octodns/octodns.git@9da19749e28f68407a1c246dfdf65663cdc1c422#egg=octodns
-e git+https://git@github.com/octodns/octodns-transip.git@ec9661f8b335241ae4746eea467a8509205e6a30#egg=octodns_transip
```

### Configuration

```yaml
providers:
  transip:
    class: octodns_transip.TransipProvider
    # Your Transip account name (required)
    account: env/TRANSIP_ACCOUNT
    # Path to a private key file (required if key is not used)
    key_file: /path/to/file
    # The api key as string (required if key_file is not used)
    #key: env/TRANSIP_KEY
    #    -----BEGIN PRIVATE KEY-----
    #    ...
    #    -----END PRIVATE KEY-----
    # if both `key_file` and `key` are presented `key_file` is used
```

### Support Information

#### Records

TransipProvider A, AAAA, ALIAS, CAA, CNAME, DS, MX, NAPTR, NS, SPF, SRV, SSHFP, TLSA, TXT

#### Root NS records

TransipProvider support root NS record management.   
**notes:** 
  - Transip currently only supports FQDN values for root nameservers.
  - Transip has no TTL for root nameservers, so the TTL value from the source is ignored 


#### Dynamic

TransipProvider does not support dynamic records.

### Development

See the [/script/](/script/) directory for some tools to help with the development process. They generally follow the [Script to rule them all](https://github.com/github/scripts-to-rule-them-all) pattern. Most useful is `./script/bootstrap` which will create a venv and install both the runtime and development related requirements. It will also hook up a pre-commit hook that covers most of what's run by CI.
