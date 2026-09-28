# zoho-books-sync-reconciler (moved)

This project moved to [zoho-implementation-toolkit](https://github.com/prashobnair/zoho-implementation-toolkit) as the `books` module. Its full commit history was preserved there.

It reconciles CRM deals against Books invoices across entities — mismatches and missing invoices flagged before close.

## Use it now

```sh
pip install https://github.com/prashobnair/zoho-implementation-toolkit/releases/download/v0.1.0/zohokit-0.1.0-py3-none-any.whl
```

or

```sh
uv tool install git+https://github.com/prashobnair/zoho-implementation-toolkit@v0.1.0
```

The old `python cli.py period.json [--strict]` is now:

```sh
zohokit books reconcile period.json [--strict]
```

`--strict` exits 2 when the period does not reconcile. Reports render with `--format json|table|markdown|html` and `--out`.

## Links

- Module guide: https://prashobnair.github.io/zoho-implementation-toolkit/modules/books/
- What changed versus this repo: https://prashobnair.github.io/zoho-implementation-toolkit/legacy-parity/
- Source: https://github.com/prashobnair/zoho-implementation-toolkit/tree/main/src/zohokit/modules/books

This repository is archived and read-only.
