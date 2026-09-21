# Tasks

## 1. Build

- [x] 1.1 `keys.yaml`, `pubkeys/786F851F8AE345F5A98B822EC92F47D08BCD9F72.asc`, `scripts/build-wkd.py` with `--check`
- [x] 1.2 `site/` rendered: `policy`, two `hu` files, `_headers`, `index.html`
- [x] 1.3 `wrangler.jsonc` with the custom domain
- [x] 1.4 `wkd-check` and `wkd-tests` hooks, the `quality` step

## 2. Verification

- [x] 2.1 `tests/test_wkd.py`: the GnuPG reference hash vector, the tree matches `keys.yaml`, every served key is binary
- [ ] 2.2 `wrangler deploy` by the owner, then `gpg --locate-external-keys git@martinzeman.net` returns `786F851F…`
- [ ] 2.3 Both prek stages in an isolated clone

## 3. Record

- [ ] 3.1 Archive moves `adr.md` to `docs/decisions/` as `WKD-0001`
