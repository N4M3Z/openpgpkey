# openpgpkey.martinzeman.net

> Prepare an openpgpkey checkout for maintenance and run its checks.

I want you to prepare this openpgpkey checkout for maintenance and run its checks. The checkout keeps its local changes, and setup installs no hooks, deploys nothing, and does not run the key discovery command from the README.

## OBJECTIVE

The maintainer tools are present and `make validate` passes.

## DONE WHEN

`make validate` exits 0 at the repository root.

## TODO

- [ ] Check Git, uv, Python 3.12 or later, GnuPG, and Make
- [ ] Run `make validate`

## Steps

1. At the repository root, check the tools. If one is missing or Python is older than 3.12, report it and stop.

```sh
git --version
uv --version
python3 -c 'import sys; print(sys.version); sys.exit(sys.version_info < (3, 12))'
gpg --version
make --version
```

2. Run the checks. uv may download the locked dependencies. If the checks fail, report the output.

```sh
make validate
```

EXECUTE NOW: Complete the above TODO list to achieve: maintainer tools confirmed and `make validate` passing.
