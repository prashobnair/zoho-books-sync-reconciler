# Reconciliation and operations

## Proposed mapping boundary

The fictional deal-to-invoice reference is `deal.id` → `invoice.deal_ref`. A real tenant needs approved organization IDs, customer identities, tax jurisdiction, currency rules, item/catalog mapping, invoice status, permissions, external idempotency key and the current Zoho CRM/Books API metadata. Multiple invoices per deal may be legitimate for staged billing, but this *one-invoice demo policy* flags them for review instead of guessing. Cross-entity invoices must not silently be reclassified.

## Workflow before production

1. Inventory legal entities, chart of accounts, tax and invoicing policy with a qualified finance owner. These are not inferred from sales data.
2. Map deal/customer IDs to Books organization/customer IDs in a sandbox. Never cross the organization boundary by matching on name alone.
3. Dry-run a small synthetic or approved sandbox set. Reconcile amounts, currency, tax decisions, invoice numbers and status; review every finding.
4. Define idempotency and retry behavior for timeouts and partial failures. A failed response may still have created an invoice; query the destination before retrying.
5. Capture a backup and a reviewed reversal/credit-note process. Deleting financial records is not a generic rollback.
6. Limit production permissions, log redacted evidence, monitor failures and explicitly approve the first real posting.

## Tests and limits

Six tests cover bad and clean fixtures, entity isolation, monetary input validation, orphan invoices and deterministic read-only runs. Missing: legitimate partial invoices, tax/FX engines, rounding policy, credits, concurrency, customer matching, API/webhook authentication, rate limits and settlement. None should be faked as done. This prototype is not a finance tool and must not be connected to a live Books organization without a new design and owner approval.
