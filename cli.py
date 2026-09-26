import argparse
import json
from pathlib import Path
from reconcile import reconcile

def main():
    parser = argparse.ArgumentParser(description='Dry-run fictional CRM-to-Books reconciliation')
    parser.add_argument('fixture')
    parser.add_argument('--strict', action='store_true')
    args = parser.parse_args()
    try:
        report = reconcile(json.loads(Path(args.fixture).read_text(encoding='utf-8')))
    except (OSError, ValueError, KeyError) as exc:
        parser.exit(1, f'Input error: {exc}\n')
    print(json.dumps(report, indent=2, sort_keys=True))
    if args.strict and not report['ready_for_sync']:
        parser.exit(2)

if __name__ == '__main__':
    main()
