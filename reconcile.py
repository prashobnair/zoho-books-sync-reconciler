"""Offline reconciliation only. No accounting writes or tax computation."""
from __future__ import annotations
from collections import defaultdict
from decimal import Decimal, InvalidOperation


def amount(value):
    if not isinstance(value, str):
        raise ValueError('Amounts must be decimal strings')
    try:
        number = Decimal(value)
    except InvalidOperation as exc:
        raise ValueError(f'Invalid decimal amount: {value}') from exc
    if not number.is_finite() or number < 0 or number.as_tuple().exponent < -2:
        raise ValueError('Amounts must be finite nonnegative with at most two places')
    return number


def reconcile(data):
    """Compare synthetic CRM deals against synthetic Books invoices by external key."""
    if not isinstance(data, dict) or any(not isinstance(data.get(k), list) for k in ('deals', 'invoices')):
        raise ValueError('deals and invoices must be lists')
    entities = data.get('entities')
    if not isinstance(entities, dict):
        raise ValueError('entities must be an object')
    findings = []
    invoices_by_key = defaultdict(list)
    deals_by_key = defaultdict(list)
    for inv in data['invoices']:
        if not isinstance(inv, dict):
            raise ValueError('invoice must be an object')
        key = str(inv.get('deal_ref', ''))
        invoices_by_key[key].append(inv)
    for deal in data['deals']:
        if not isinstance(deal, dict):
            raise ValueError('deal must be an object')
        key = str(deal.get('id', ''))
        deals_by_key[key].append(deal)
    for key, rows in sorted(deals_by_key.items()):
        if not key or len(rows) != 1:
            findings.append({'deal':key,'code':'duplicate_or_missing_deal_id'})
            continue
        deal = rows[0]
        tenant = str(deal.get('entity', ''))
        currency = str(deal.get('currency', ''))
        if tenant not in entities or currency != entities.get(tenant):
            findings.append({'deal':key,'code':'entity_currency_mismatch'})
        expected = amount(deal.get('net_amount'))
        matches = invoices_by_key.get(key, [])
        if not matches:
            findings.append({'deal':key,'code':'missing_invoice'})
        if len(matches) > 1:
            findings.append({'deal':key,'code':'duplicate_invoice_reference'})
        for inv in matches:
            if str(inv.get('entity', '')) != tenant:
                findings.append({'deal':key,'code':'cross_entity_invoice'})
            if str(inv.get('currency', '')) != currency:
                findings.append({'deal':key,'code':'currency_mismatch'})
            if amount(inv.get('net_amount')) != expected:
                findings.append({'deal':key,'code':'net_amount_mismatch'})
            if inv.get('tax_reviewed') is not True:
                findings.append({'deal':key,'code':'tax_not_reviewed'})
            if inv.get('sync_state') == 'failed':
                findings.append({'deal':key,'code':'sync_failed'})
    for key in sorted(invoices_by_key):
        if key not in deals_by_key:
            findings.append({'deal':key,'code':'orphan_invoice_reference'})
    findings.sort(key=lambda f: (f['deal'], f['code']))
    return {'mode':'dry_run_only','ready_for_sync':not findings,'deal_count':len(data['deals']),
            'invoice_count':len(data['invoices']),'findings':findings,'created_invoices':0}
