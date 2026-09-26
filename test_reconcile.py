import copy
import json
import unittest
from pathlib import Path
from reconcile import amount, reconcile

DATA = json.loads(Path(__file__).with_name('examples.json').read_text())

class ReconcileTests(unittest.TestCase):
    def test_bad_fixture(self):
        report = reconcile(DATA)
        self.assertFalse(report['ready_for_sync'])
        self.assertEqual({'duplicate_invoice_reference','net_amount_mismatch','tax_not_reviewed','sync_failed',
                          'cross_entity_invoice','currency_mismatch','missing_invoice'},
                         {x['code'] for x in report['findings']})
        self.assertEqual(0, report['created_invoices'])

    def test_clean_fixture(self):
        data = copy.deepcopy(DATA)
        data['deals'] = data['deals'][:1]
        data['invoices'] = data['invoices'][:1]
        self.assertTrue(reconcile(data)['ready_for_sync'])
        self.assertEqual([], reconcile(data)['findings'])

    def test_cross_entity_never_passes(self):
        data = copy.deepcopy(DATA)
        data['deals'] = data['deals'][:1]
        data['invoices'] = data['invoices'][:1]
        data['invoices'][0]['entity'] = 'fictional-us'
        self.assertIn('cross_entity_invoice', [x['code'] for x in reconcile(data)['findings']])

    def test_reject_float_and_precision(self):
        for value in (1.2, '1.234', 'NaN', '-1'):
            with self.assertRaises(ValueError):
                amount(value)

    def test_orphan_invoice(self):
        data = copy.deepcopy(DATA)
        data['invoices'].append(dict(data['invoices'][0], deal_ref='missing'))
        self.assertIn('orphan_invoice_reference', [x['code'] for x in reconcile(data)['findings']])

    def test_stable_readonly(self):
        data = copy.deepcopy(DATA)
        result = reconcile(data)
        self.assertEqual(data, DATA)
        self.assertEqual(result, reconcile(data))

if __name__ == '__main__':
    unittest.main()
