---
title: "Publish OpenPGP keys through a self-hosted Web Key Directory"
description: "The owner's OpenPGP keys are resolved by address from openpgpkey.martinzeman.net, rendered from a reviewed fingerprint list, not from keyservers or a mail provider's WKD."
type: adr
category: infrastructure
tags:
    - openpgp
    - wkd
    - keys
status: proposed
created: 2026-09-21
updated: 2026-09-21
author: "@N4M3Z"
project: openpgpkey
related: []
responsible: ["@N4M3Z"]
accountable: ["@N4M3Z"]
consulted: ["claude-fable-5-1"]
informed: []
upstream:
    - "https://datatracker.ietf.org/doc/draft-koch-openpgp-webkey-service/"
change: web-key-directory-publication
---

# Publish OpenPGP keys through a self-hosted Web Key Directory

## Context and Problem Statement

Four keys carry the owner's name in public: the 2026 YubiKey (`786F851F…`, the ceremony signer), a 2016 MacGPG RSA key (`7206934F…`, still used on an older machine, published on GitHub and `keys.openpgp.org` without identities), and two Proton mail keys served only by Proton's WKD for `pm.me` and `proton.me`. The ceremony pins a fingerprint in every repository and needs key bytes from a source the owner controls. Nothing published today is both under the owner's control and addressable by a standard client lookup.

## Considered Options

1. Keep the armored block in every repository's `KEYS` file (the Apache convention).
2. SKS or `keys.openpgp.org` lookup by fingerprint.
3. Proton's WKD for the `pm.me` address.
4. `github.com/N4M3Z.gpg`, pinned by fingerprint.
5. A Web Key Directory on the owner's domain, advanced method, static assets on Cloudflare, rendered from a reviewed fingerprint list.

## Decision Outcome

Option 5, with option 4 as the fallback source and the pinned fingerprint as the check in both cases. The SKS pool is gone and `keys.openpgp.org` strips unverified identities (option 2). Proton publishes only its own mail keys and a hardware certify key never leaves the token, so it cannot appear there (option 3). GitHub's key list is account state a token can edit (option 4 alone). Option 1 works offline but puts 2.8 KB of armor in fifteen repositories, which no reviewer reads.

The directory MUST keep these rules:

- `keys.yaml` is the only hand-edited input. The served tree is generated, and the check refuses a tree that differs.
- A block MUST prove its fingerprint against its file name, and an address MUST appear as a user id on the key that answers it.
- The 2016 key stays unrevoked while the older machine uses it, and it is not published here.

## Consequences

- Any OpenPGP client resolves `git@martinzeman.net` with no configuration, and the ceremony's `KEYS` shrinks to fingerprint lines.
- Deployment depends on Cloudflare. The GitHub fallback covers an outage for the ceremony, and offline signing uses `rune sign`'s cache.
- Adding a Proton mail key for a `@martinzeman.net` address is one `keys.yaml` entry and one exported block.
