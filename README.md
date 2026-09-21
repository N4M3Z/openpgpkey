# openpgpkey.martinzeman.net

> Web Key Directory for `@martinzeman.net` addresses.

The site publishes OpenPGP public keys with the advanced method of the [Web Key Directory draft][WKD]. A client such as GnuPG finds a key from the email address alone.

## Find a key

If you want the key, run:

```sh
gpg --locate-external-keys git@martinzeman.net
```

This imports the key into your own keyring. It is not part of maintainer setup. Compare its fingerprint with this table, which follows `keys.yaml`:

| Address | Key |
|---|---|
| `git@martinzeman.net`, `github.com@martinzeman.net` | `786F851F8AE345F5A98B822EC92F47D08BCD9F72`, signing subkey `29DD2145CE7A818929459B2649F08103D3DA399E` |

## Maintain

`keys.yaml` and `pubkeys/` are the source. The builder produces the tracked key and policy files in `site/` from them, in a temporary GnuPG home that leaves your keyring alone. `site/_headers` and `site/index.html` are static files and are not generated.

You need Git, uv, Python 3.12 or later, GnuPG, and Make. Agents can follow [INSTALL.md](INSTALL.md).

```sh
make validate
```

This checks that the site files match the source and runs the unit tests through `uv run --locked`. uv may download the locked dependencies.

## Deploy

The owner deploys by hand with `wrangler deploy`.

## License

[EUPL-1.2](LICENSE).

[WKD]: https://datatracker.ietf.org/doc/draft-koch-openpgp-webkey-service/
