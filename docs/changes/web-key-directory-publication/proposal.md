---
adr: docs/changes/web-key-directory-publication/adr.md
status: proposed
decisions: ["Publish OpenPGP keys through a self-hosted Web Key Directory"]
---

# Web key directory publication

## Why

The runedeck ceremony pins the owner's signing key by fingerprint and needs a place to fetch the key bytes that is under the owner's control. Keyservers are gone or strip identities (`keys.openpgp.org` serves the old `7206…` key with no addresses), Proton's WKD publishes Proton's mail keys for `pm.me` and `proton.me` and cannot publish a hardware key, and `github.com/N4M3Z.gpg` is account state that a token can edit. WKD on the owner's own domain is a fixed, spec'd URL that every OpenPGP client queries by address, with the bytes coming from a repository the owner reviews.

## What Changes

- `keys.yaml` names the domain and, per key, the fingerprint and the local parts it answers for. `pubkeys/<fingerprint>.asc` holds the public block.
- `scripts/build-wkd.py` renders `site/.well-known/openpgpkey/martinzeman.net/{policy,hu/<hash>}` and proves each block's fingerprint and user ids. Its `--check` diffs the served tree, and the hooks and `quality` run it.
- `wrangler.jsonc` serves `site/` as static assets on `openpgpkey.martinzeman.net`, and `site/_headers` sets the content type and CORS.
- The first key is the YubiKey `786F851F8AE345F5A98B822EC92F47D08BCD9F72` for `git@` and `github.com@`. Proton mail keys for `@martinzeman.net` addresses can be added as further entries.

## Capabilities

### New Capabilities

- `web-key-directory`: the addresses of `martinzeman.net` resolve to reviewed OpenPGP keys through the advanced WKD method on `openpgpkey.martinzeman.net`.

## Impact

- The runedeck `KEYS` format change (skeleton) resolves `git@martinzeman.net` through this host first and `github.com/N4M3Z.gpg` second, both checked against the pinned fingerprint.
- Deploying needs Cloudflare credentials the owner holds. One `wrangler deploy` creates the custom-domain record.
