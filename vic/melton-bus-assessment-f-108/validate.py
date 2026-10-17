"""Offline integrity and schedule-behaviour checks for F-108. Standard library only."""
import csv
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import sys

HERE = Path(__file__).resolve().parent
VIC = HERE.parent


def rows(name):
    with (HERE / name).open() as f:
        return list(csv.DictReader(f))


def pointer(obj, path):
    for part in path.split('/'):
        if part:
            obj = obj[int(part)] if isinstance(obj, list) else obj[part]
    return obj


def main():
    checks = {}
    prov = json.loads((HERE / 'provenance.json').read_text())
    for name, digest in prov['original_snapshot_hashes'].items():
        assert hashlib.sha256((VIC / 'corpus' / name).read_bytes()).hexdigest() == digest
    checks['original_snapshot_hashes'] = True
    corpus = json.loads((VIC / 'corpus/policies.json').read_text())
    claims = rows('claim-evidence.csv')
    assert len(claims) == len({r['claim_id'] for r in claims}) == 12
    assert len({r['policy_id'] for r in claims}) == 4
    source_ids = set(re.findall(r'^## (S\d{2})$', (HERE / 'sources.md').read_text(), re.M))
    assert len(source_ids) == 19
    for row in claims:
        assert set(row['source_ids'].split(';')) <= source_ids
        for value in row['original_fields'].split(';'):
            value = pointer(corpus, value.split('#')[1])
            assert isinstance(value, str) and value
    checks['12_claims_4_policies_all_pointers_and_sources_resolve'] = True
    coverage = rows('coverage-ledger.csv')
    old = list(csv.DictReader((VIC / 'research-plan-f-107/coverage-ledger.csv').open()))
    assert len(coverage) == len(old) == 66
    assert {r['id'] for r in coverage} == {r['id'] for r in old}
    assert sum(r['stage_2_status'] == 'bounded selected-claim assessment' for r in coverage) == 4
    assert sum(r['stage_2_status'] == 'internal framing inspected' for r in coverage) == 3
    assert all(r['fully_validated'] == 'no' for r in coverage)
    by_id = {r['id']: r for r in old}
    assert all(all(row[k] == v for k, v in by_id[row['id']].items()) for row in coverage)
    points = rows('key-point-coverage.csv')
    assert len(points) == len({r['point_id'] for r in points}) == 12
    checks['66_record_ledger_preserves_original_columns_and_12_key_points'] = True
    discovery = json.loads((HERE / 'search-discovery.json').read_text())
    candidates = rows('candidate-ledger.csv')
    assert sum(len(r['queries']) for r in discovery['runs']) == 18
    assert len(candidates) == len(discovery['candidates']) == 305
    assert len({r['url'] for r in candidates}) == 289
    assert len(rows('forward-citation-leads.csv')) == 217
    checks['search_occurrences_and_pending_citation_leads_reconcile'] = True
    for p in HERE.glob('*.md'):
        assert 'Research — not adopted Fusion policy' in p.read_text()
        for target in re.findall(r'\]\(([^)]+)\)', p.read_text()):
            if target == 'validation.json':  # This receipt is produced below on first run.
                continue
            if not target.startswith(('http://', 'https://', 'mailto:', '#')):
                assert (p.parent / target.split('#')[0]).exists(), (p.name, target)
    checks['research_labels_and_local_links'] = True
    spec = importlib.util.spec_from_file_location('timetable', HERE / 'analyse_timetables.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    cal = [dict(service_id='normal', start_date='20261001', end_date='20261031',
                monday='1', tuesday='1', wednesday='1', thursday='1', friday='1', saturday='0', sunday='0')]
    exceptions = [dict(service_id='normal', date='20261016', exception_type='2'),
                  dict(service_id='extra', date='20261016', exception_type='1')]
    assert module.active_services('20261016', cal, exceptions) == {'extra'}
    assert module.active_services('20261018', cal, exceptions) == set()
    assert module.active_services('20261102', cal, exceptions) == set()
    assert module.seconds('25:10:00') == 90600
    checks['calendar_exceptions_weekends_boundaries_and_overnight_times'] = True
    meta = json.loads((HERE / 'timetable-data/provenance.json').read_text())
    tables = {}
    for table, count in meta['rows'].items():
        tables[table] = rows('timetable-data/' + table + '.csv')
        assert len(tables[table]) == count
    trip_ids = {r['trip_id'] for r in tables['trips']}
    stop_ids = {r['stop_id'] for r in tables['stops']}
    assert all(r['trip_id'] in trip_ids and r['stop_id'] in stop_ids for r in tables['stop_times'])
    checks['all_filtered_gtfs_rows_resolve_and_counts_match'] = True
    output_names = ['shared-corridor-departures.csv', 'shared-corridor-summary.csv', 'shared-corridor-close-pairs.csv']
    before = {n: (HERE / n).read_bytes() for n in output_names}
    subprocess.run([sys.executable, str(HERE / 'analyse_timetables.py')], check=True, capture_output=True)
    assert all((HERE / n).read_bytes() == data for n, data in before.items())
    departures = rows('shared-corridor-departures.csv')
    sunday = [r for r in departures if r['date'] == '20261018' and r['from_stop'] == '13428'
              and '09:00:00' <= r['departure'] < '14:00:00']
    by_time = {}
    for row in sunday:
        by_time.setdefault(row['departure'], set()).add(row['route'])
    assert len(by_time) == 8 and all(v == {'457', '459'} for v in by_time.values())
    summaries = rows('shared-corridor-summary.csv')
    assert len(summaries) == 12
    assert len({(r['from_stop'], r['to_stop']) for r in summaries}) == 6
    checks['byte_identical_reproduction_and_sunday_simultaneous_pairs'] = True
    receipt = dict(scope='offline artifact integrity and described timetable behaviour; not empirical truth certification',
                   checks=checks, all_passed=all(checks.values()),
                   verdict_counts={v: sum(r['verdict'] == v for r in claims) for v in sorted({r['verdict'] for r in claims})})
    (HERE / 'validation.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps(receipt, indent=2))


if __name__ == '__main__':
    main()
