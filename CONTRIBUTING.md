# Contributing

Clone `https://github.com/N4M3Z/openpgpkey.git` and follow [INSTALL.md](INSTALL.md).

Change `keys.yaml` and the matching public block in `pubkeys/` when adding or replacing a published key.
Run `make build`, then `make validate`. Include the generated WKD files with the input change.
Preserve `site/_headers` and `wrangler.jsonc` unless the deployment itself must change.
Never add private keys, credentials, Cloudflare caches, or session logs.

Run `make secret-scan` before publication. Use `make install-hooks` only when you want local commit and push checks.
Keep the existing signing policy. Use JJ when the checkout contains `.jj/`.

Use a short `type: description` commit subject and credit model contributors through `Co-Authored-By` trailers.
Describe the behavior change and its checks in the pull request. No draft sequence, review labels, or release-note template is required.
Deployment is a separate owner-authorized operation.
