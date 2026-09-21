## ADDED Requirements

### Requirement: Addresses resolve through the advanced Web Key Directory

The host `openpgpkey.martinzeman.net` MUST serve `/.well-known/openpgpkey/martinzeman.net/policy` and, for every address in `keys.yaml`, `/.well-known/openpgpkey/martinzeman.net/hu/<hash>` where `<hash>` is the Z-Base-32 SHA-1 of the lowercased local part, as `draft-koch-openpgp-webkey-service` defines. Each `hu` file MUST hold the binary transferable public key, never armor, with `Content-Type: application/octet-stream` and `Access-Control-Allow-Origin: *`.

#### Scenario: gpg resolves the ceremony key

- **WHEN** a client runs `gpg --locate-external-keys git@martinzeman.net`
- **THEN** it receives the key whose primary fingerprint is `786F851F8AE345F5A98B822EC92F47D08BCD9F72` from `openpgpkey.martinzeman.net`

#### Scenario: Unknown address

- **WHEN** a client asks for a local part `keys.yaml` does not list
- **THEN** the host answers 404 and no key

### Requirement: The served tree is generated and checked

`keys.yaml` MUST be the only hand-edited input: a domain and, per key, a fingerprint and its addresses. `scripts/build-wkd.py` MUST render the tree from `pubkeys/<fingerprint>.asc`, MUST refuse a block whose primary fingerprint differs from its file name, MUST refuse an address the key carries no user id for, and `--check` MUST fail when `site/` differs from the render. The commit-stage hook and the `quality` workflow MUST run that check.

#### Scenario: Address without a user id

- **WHEN** `keys.yaml` lists `mail` under a key whose user ids carry no `mail@martinzeman.net`
- **THEN** the build exits nonzero naming the address and the user ids the key has

#### Scenario: Tree edited by hand

- **WHEN** a commit changes a file under `site/.well-known/openpgpkey/` without changing `keys.yaml` or `pubkeys/`
- **THEN** the `wkd-check` hook fails with the differing paths

### Requirement: One key may answer several addresses

A key MUST be listed once in `keys.yaml` with every local part it answers for, and the build MUST write the same binary under each address hash.

#### Scenario: Two addresses, one key

- **WHEN** `keys.yaml` lists `git` and `github.com` under `786F851F8AE345F5A98B822EC92F47D08BCD9F72`
- **THEN** `hu/e5a4bxki1ktx1jncwco5nkcofedmkxod` and `hu/aeoeixxjc48e7gyiapwooixp48udixic` hold identical bytes
