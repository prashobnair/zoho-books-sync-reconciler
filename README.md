# Zoho Books Sync Reconciler

A **dry-run**, offline check of fictional CRM deals against fictional Books invoices across two fictional legal entities. It flags duplicate invoice references, missing invoices, wrong entity/currency, net amount mismatch, tax review gaps and failed sync states. It never creates an invoice, computes tax, calls Zoho, or moves money.

## Contract use-case

The [Zoho CRM contract board](https://www.upwork.com/freelance-jobs/zoho-crm/) samples multi-entity Zoho One/Books requests. An older [CRM/Books/Xero implementation brief](https://www.freelancer.com/projects/xero/zoho-expert-for-crm-books) calls for connected sales and finance workflows. This repo isolates the *reconciliation and safety* slice; it is not a Books connector or accounting application, and these postings are not client engagements.

## Run

Python 3.10+ and standard library only. From the repository root:

```sh
python3 cli.py examples.json
python3 cli.py examples.json --strict  # exit 2 on findings
python3 -m unittest discover -p 'test_*.py' -v
```

No Zoho trial, API key, invoice account, Docker or paid service is needed. The synthetic sample has three deals and three invoices: `d-1` agrees, `d-2` has a duplicate invoice reference, amount/currency/entity mismatch, unreviewed tax and one failed sync; `d-3` has no invoice. It produces seven distinct finding codes and `created_invoices: 0`. The unit tests contain a clean one-deal example.

## Model and interpretation

Each deal has an `id`, entity, currency and `net_amount` as a decimal string. An invoice has `deal_ref`, entity, currency, `net_amount`, `tax_reviewed` and `sync_state`. `entities` maps fictional entity keys to their expected currency. All amounts are finite, nonnegative and at most two decimal places. An exact net-amount comparison is only a demo convention: tax, discounts, fees, FX, credit notes, partial billing and timing are deliberately not calculated. A `ready_for_sync` pass says the narrow input checks agree, not that posting an invoice is safe.

The schema is a **fictional intermediate model**, not an assertion about Zoho CRM or Books API payloads. See `DESIGN.md` for mappings, idempotency, review and rollback requirements before any real integration. Never put employer or client finance data into this repository.
