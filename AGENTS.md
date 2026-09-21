# openpgpkey

This repository publishes the Web Key Directory for `martinzeman.net`.

- `keys.yaml` selects public keys and their addresses.
- `pubkeys/` contains public key blocks. Never add private keys or credentials.
- `scripts/build-wkd.py` generates `site/.well-known/openpgpkey/` and validates each key fingerprint and address.
- `site/_headers` and `site/index.html` are static publication files. Preserve them when rebuilding keys.
- `wrangler.jsonc` defines the existing Cloudflare deployment. Do not change or deploy it without the owner's request.

Run `make build` after changing key inputs. Run `make validate` to check the generated tree and tests.
Run `make secret-scan` before publication. Local hooks are optional and use `make install-hooks`.
Keep generated WKD files in version control. Do not edit them by hand.
The builder uses a temporary GPG home. It must not use the owner's keyring or agent.

Use JJ for repository changes when `.jj/` exists. Keep existing signing settings and push checks.
Do not commit or push without approval for the exact change.
Use a short conventional commit subject. Credit model contributors with `Co-Authored-By` trailers from `authors.yaml`.
No review bot, release-note form, or specification ceremony is required.

The older 2016 RSA key remains intentionally unpublished here. Do not revoke or replace it as part of maintenance.
Keep `.wrangler/`, session logs, and local configuration outside version control.
