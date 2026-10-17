"""Rebuild the F-107 inventory from preserved exports (Python standard library).

Run from any directory. No network or source mutations by default.
--check-links performs one bounded GET per distinct exported content URL and
retains status/final URL only, not third-party full texts. Reachability is not
source identity, citation accuracy, or evidence validation.
"""
import argparse
import collections
import concurrent.futures
import csv
import datetime
import hashlib
import json
from pathlib import Path
import re
import urllib.error
import urllib.request

HERE = Path(__file__).resolve().parent
VIC = HERE.parent
ORIGINAL = VIC / 'corpus'

CLUSTERS = {
    'C1': ['end-flexiride-s-fake-flexibility', 'fix-the-order-not-just-the-fare',
           'guarantee-the-one-kilometre-standard', 'stagger-the-timetables',
           'fund-the-outer-suburbs', 'fix-transit-deserts'],
    'C2': ['tram-surface-rapid-transit', 'deliver-accessible-public-transport',
           'no-single-points-of-failure', 'finish-the-network', 'connect-the-regions',
           'build-the-melton-line'],
    'C3': ['complete-neighbourhoods', 'homes-and-stations-code',
           'build-housing-at-stations', 'charge-the-car-parks'],
    'C4': ['take-back-public-assets', 'unmask-transurban-s-discount',
           'audit-southern-cross', 'expose-the-tunnel-deal', 'claw-back-franchise-profits'],
    'C5': ['police-integrity-independent-accountability', 'prevention-first-public-safety',
           'problem-oriented-policing', 'safer-night-time-precincts',
           'youth-diversion-early-intervention', 'neighbourhood-police-posts'],
    'C6': ['open-government-by-default', 'protect-whistleblowers',
           'count-your-volunteer-hours', 'ban-corporate-fundraisers', 'abolish-preference-deals'],
    'C7': ['nothing-without-the-people', 'communities-set-policy', 'citizens-in-every-room'],
    'C8': ['set-the-rules-for-data-centres'],
    'C9': ['pay-every-victorian', 'build-the-sovereign-fund', 'tax-the-land-windfalls',
           'audit-the-fake-surplus', 'smooth-the-pension-cliff'],
}
FIRST = {'fix-transit-deserts', 'guarantee-the-one-kilometre-standard',
         'stagger-the-timetables', 'end-flexiride-s-fake-flexibility'}
BATCHES = {
    'B1': sorted(FIRST),
    'B2': ['audit-the-fake-surplus', 'smooth-the-pension-cliff'],
    'B3': ['prevention-first-public-safety', 'problem-oriented-policing', 'youth-diversion-early-intervention'],
    'B4': CLUSTERS['C8'],
    'B5': ['tram-surface-rapid-transit', 'deliver-accessible-public-transport', 'no-single-points-of-failure'],
    'B6': CLUSTERS['C3'],
    'B7': ['pay-every-victorian', 'build-the-sovereign-fund', 'tax-the-land-windfalls'],
    'B8': ['take-back-public-assets', 'claw-back-franchise-profits', 'audit-southern-cross'],
    'B9': ['open-government-by-default', 'protect-whistleblowers', 'abolish-preference-deals'],
    'B10': ['police-integrity-independent-accountability', 'safer-night-time-precincts', 'neighbourhood-police-posts'],
    'B11': ['fix-the-order-not-just-the-fare', 'fund-the-outer-suburbs'],
    'B12': ['finish-the-network', 'connect-the-regions', 'build-the-melton-line'],
    'B13': ['unmask-transurban-s-discount', 'expose-the-tunnel-deal'],
    'B14': ['count-your-volunteer-hours', 'ban-corporate-fundraisers'],
    'B15': CLUSTERS['C7'],
}


def sha(b):
    return hashlib.sha256(b).hexdigest()


def canonical(obj):
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()


def dump(name, obj):
    (HERE / name).write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def table(name, rows):
    assert rows, name
    with (HERE / name).open('w', encoding='utf-8', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]), lineterminator='\n')
        writer.writeheader()
        writer.writerows(rows)


def paths(obj, path=''):
    if isinstance(obj, dict):
        for key, val in obj.items():
            yield from paths(val, path + '/' + key.replace('~', '~0').replace('/', '~1'))
    elif isinstance(obj, list):
        for index, val in enumerate(obj):
            yield from paths(val, path + '/' + str(index))
    elif isinstance(obj, str):
        for match in re.finditer(r'https?://[^\s<>"\[\]]+', obj):
            yield path, match.group(0).rstrip('.,;)')


def fetch_link(url):
    started = datetime.datetime.now(datetime.timezone.utc).isoformat()
    result = {'url': url, 'checked_at': started, 'method': 'GET; first 1024 bytes only',
              'status': None, 'final_url': '', 'content_type': '', 'error': ''}
    request = urllib.request.Request(url, headers={'User-Agent': 'Fusion-policy-research-link-audit/1.0'})
    try:
        with urllib.request.urlopen(request, timeout=12) as response:
            response.read(1024)
            result.update(status=response.status, final_url=response.url,
                          content_type=response.headers.get('Content-Type', ''))
    except urllib.error.HTTPError as error:
        result.update(status=error.code, final_url=error.url, error=str(error))
    except Exception as error:
        result['error'] = str(error)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check-links', action='store_true')
    args = parser.parse_args()
    snapshots = {}
    comparison = []
    for stem, array in [('policies', 'policies'), ('research', 'resources')]:
        original_bytes = (ORIGINAL / (stem + '.json')).read_bytes()
        fresh_bytes = (HERE / 'snapshots' / (stem + '.json')).read_bytes()
        old, fresh = json.loads(original_bytes), json.loads(fresh_bytes)
        snapshots[stem] = old
        ids = [x['id'] for x in old[array]]
        slugs = [x['slug'] for x in old[array]]
        urls = [x['canonical_url'] for x in old[array]]
        assert len(ids) == len(set(ids))
        assert len(slugs) == len(set(slugs))
        assert len(urls) == len(set(urls))
        changed_root = sorted(k for k in old.keys() | fresh.keys() if old.get(k) != fresh.get(k))
        old_ids, fresh_ids = {x['id']: x for x in old[array]}, {x['id']: x for x in fresh[array]}
        comparison.append({
            'kind': stem, 'original_file': '../corpus/' + stem + '.json',
            'original_bytes': len(original_bytes), 'original_sha256': sha(original_bytes),
            'original_generated_at': old['generated_at'],
            'original_retrieved_at_reported': '2026-10-16T14:16:29Z',
            'fresh_file': 'snapshots/' + stem + '.json', 'fresh_bytes': len(fresh_bytes),
            'fresh_sha256': sha(fresh_bytes), 'fresh_generated_at': fresh['generated_at'],
            'original_count': len(old[array]), 'fresh_count': len(fresh[array]),
            'changed_root_keys': changed_root,
            'added_ids': sorted(fresh_ids.keys() - old_ids.keys()),
            'removed_ids': sorted(old_ids.keys() - fresh_ids.keys()),
            'changed_records': sorted(k for k in old_ids.keys() & fresh_ids.keys() if old_ids[k] != fresh_ids[k]),
            'original_array_sha256_canonical_json': sha(canonical(old[array])),
            'fresh_array_sha256_canonical_json': sha(canonical(fresh[array])),
        })
    p = snapshots['policies']['policies']
    r = snapshots['research']['resources']
    assert len(p) == snapshots['policies']['policy_count']
    cluster_by_slug = {slug: cluster for cluster, slugs in CLUSTERS.items() for slug in slugs}
    assert len(cluster_by_slug) == sum(map(len, CLUSTERS.values())) == len(p)
    assert set(cluster_by_slug) == {x['slug'] for x in p}
    batch_by_slug = {slug: batch for batch, slugs in BATCHES.items() for slug in slugs}
    assert len(batch_by_slug) == sum(map(len, BATCHES.values())) == len(p)
    assert set(batch_by_slug) == set(cluster_by_slug)
    policy_by_url = {x['canonical_url']: x for x in p}
    research_by_url = {x['canonical_url']: x for x in r}
    manifest = (ORIGINAL / 'MANIFEST.md').read_text()
    matrix = (VIC / 'evidence-matrix.md').read_text()
    gap = (VIC / 'gap-register.md').read_text()
    policy_rows, point_rows, research_rows, edges, citations, occurrences = [], [], [], [], [], []
    for i, x in enumerate(p):
        cluster = cluster_by_slug[x['slug']]
        refs = x['supporting_research']
        pointer = '/policies/' + str(i)
        policy_rows.append({
            'id': x['id'], 'slug': x['slug'], 'title': x['title'], 'canonical_url': x['canonical_url'],
            'source_file': '../corpus/policies.json', 'json_pointer': pointer,
            'record_sha256_canonical_json': sha(canonical(x)), 'export_status': x['status'],
            'authority_status': x['authority']['status'], 'authority_adopted_policy': x['authority']['adopted_policy'],
            'status_verification': 'export-declared; adoption instrument not supplied',
            'publisher': x['authority']['publisher'], 'author': 'not exported',
            'published_at': x['published_at'], 'updated_at': x['updated_at'],
            'substantive_updated_at': x['substantive_updated_at'] or '',
            'license': 'not exported', 'attachments': 'no policy attachment field exported',
            'pillar': x['pillar'], 'category': x['category'], 'primary_cluster': cluster,
            'delivery_horizon': x['delivery_horizon'], 'summary_verbatim': x['summary'],
            'key_point_count': len(x['key_points']), 'supporting_research_count': len(refs),
            'supporting_research_ids': '|'.join(research_by_url[y['canonical_url']]['id'] for y in refs if y['canonical_url'] in research_by_url),
            'manifest_title_present': x['title'] in manifest,
            'matrix_title_present': x['title'] in matrix,
            'batch': batch_by_slug[x['slug']],
            'inventory': 'reconciled', 'claim_assessment': 'unassessed', 'verdict': 'not yet assessed',
        })
        for j, point in enumerate(x['key_points']):
            point_rows.append({'point_id': x['id'] + ':' + point['_key'], 'policy_id': x['id'],
                               'policy_slug': x['slug'], 'original_key': point['_key'],
                               'source_file': '../corpus/policies.json',
                               'json_pointer': pointer + '/key_points/' + str(j),
                               'point_verbatim': point.get('point', ''),
                               'description_verbatim': point.get('description', ''),
                               'primary_cluster': cluster, 'assessment': 'unassessed; may mix facts, proposals and values'})
        for ref in refs:
            target = research_by_url.get(ref['canonical_url'])
            edges.append({'direction': 'policy_to_research', 'from_id': x['id'],
                          'to_url': ref['canonical_url'], 'to_id': target['id'] if target else '',
                          'resolved': target is not None,
                          'reciprocal': bool(target and any(z['canonical_url'] == x['canonical_url'] for z in target['related_policies']))})
        for path, url in paths(x, pointer):
            occurrences.append({'kind': 'policy', 'id': x['id'], 'json_pointer': path, 'url': url})
    for i, x in enumerate(r):
        incoming = [y for y in p if any(z['canonical_url'] == x['canonical_url'] for z in y['supporting_research'])]
        pointer = '/resources/' + str(i)
        research_rows.append({
            'id': x['id'], 'slug': x['slug'], 'title': x['title'], 'canonical_url': x['canonical_url'],
            'source_file': '../corpus/research.json', 'json_pointer': pointer,
            'record_sha256_canonical_json': sha(canonical(x)), 'authority_status': x['authority']['status'],
            'authority_adopted_policy': x['authority']['adopted_policy'], 'resource_type': x['resource_type'],
            'research_area': x['research_area'], 'version': x['version'],
            'authors': '|'.join(a['name'] for a in x['authors']) or 'not exported',
            'publisher': x['authority']['publisher'], 'published_at': x['published_at'],
            'updated_at': x['updated_at'], 'research_first_documented_at': x['research_first_documented_at'] or '',
            'research_provenance_verbatim': x['research_provenance'] or '',
            'license_exported': x['license'] or 'not exported',
            'downloads_count': len(x['downloads']), 'external_project_url': x['external_project_url'] or '',
            'repository_url': x['repository_url'] or '', 'source_count': len(x['sources']),
            'policy_incoming_count': len(incoming), 'policy_incoming_ids': '|'.join(y['id'] for y in incoming),
            'manifest_title_present': x['title'] in manifest, 'inventory': 'reconciled',
            'evidence_validation': 'unassessed; internal research is not independent corroboration',
        })
        for ref in x['related_policies']:
            target = policy_by_url.get(ref['canonical_url'])
            edges.append({'direction': 'research_to_policy', 'from_id': x['id'],
                          'to_url': ref['canonical_url'], 'to_id': target['id'] if target else '',
                          'resolved': target is not None,
                          'reciprocal': bool(target and any(z['canonical_url'] == x['canonical_url'] for z in target['supporting_research']))})
        for j, source in enumerate(x['sources']):
            citations.append({'source_instance_id': x['id'] + ':' + source.get('_key', str(j)),
                              'research_id': x['id'], 'json_pointer': pointer + '/sources/' + str(j),
                              'title_exported': source.get('title', ''), 'publisher_exported': source.get('publisher', ''),
                              'url': source.get('url', ''), 'note_exported': source.get('note', ''),
                              'claim_alignment': 'unchecked', 'metadata_identity': 'unchecked',
                              'full_text': 'not collected', 'third_party_license': 'not established'})
        for path, url in paths(x, pointer):
            occurrences.append({'kind': 'research', 'id': x['id'], 'json_pointer': path, 'url': url})
    assert all(e['resolved'] for e in edges)
    assert all(x['manifest_title_present'] for x in policy_rows + research_rows)
    assert all(x['matrix_title_present'] for x in policy_rows)
    assert len({x['point_id'] for x in point_rows}) == len(point_rows)
    table('proposal-register.csv', policy_rows)
    table('key-point-register.csv', point_rows)
    table('research-register.csv', research_rows)
    table('cross-references.csv', edges)
    table('citation-instances.csv', citations)
    table('url-occurrences.csv', occurrences)
    dump('snapshot-comparison.json', comparison)
    summary = {
        'policies': len(p), 'research_resources': len(r), 'key_points': len(point_rows),
        'status_counts': dict(collections.Counter(x['status'] for x in p)),
        'policies_with_research': sum(bool(x['supporting_research']) for x in p),
        'policies_without_research': sum(not x['supporting_research'] for x in p),
        'research_without_incoming_policy': [x['id'] for x in research_rows if x['policy_incoming_count'] == 0],
        'directed_cross_references': len(edges), 'broken_cross_references': sum(not x['resolved'] for x in edges),
        'nonreciprocal_cross_references': sum(not x['reciprocal'] for x in edges),
        'citation_instances': len(citations), 'distinct_cited_urls': len({x['url'] for x in citations}),
        'url_occurrences': len(occurrences), 'distinct_content_urls': len({x['url'] for x in occurrences}),
        'research_licenses': dict(collections.Counter(x['license_exported'] for x in research_rows)),
        'research_without_authors': [x['id'] for x in research_rows if x['authors'] == 'not exported'],
        'research_downloads': sum(x['downloads_count'] for x in research_rows),
        'cluster_policy_counts': dict(collections.Counter(x['primary_cluster'] for x in policy_rows)),
        'independently_assessed_policies': 0, 'independently_validated_research_resources': 0,
        'all_original_hashes_match_log': all(c['original_sha256'] in (ORIGINAL / 'RETRIEVAL-LOG.md').read_text() for c in comparison),
        'fresh_record_changes': sum(len(c['changed_records']) for c in comparison),
        'fresh_added_or_removed': sum(len(c['added_ids']) + len(c['removed_ids']) for c in comparison),
        'difference_limited_to_generated_at': all(c['changed_root_keys'] == ['generated_at'] for c in comparison),
        'matrix_title_coverage': sum(x['matrix_title_present'] for x in policy_rows),
        'manifest_title_coverage': sum(x['manifest_title_present'] for x in policy_rows + research_rows),
        'note': 'Title presence checks are inventory checks, not substantive verification of derived prose.'
    }
    dump('audit-summary.json', summary)
    if args.check_links:
        urls = sorted({x['url'] for x in occurrences})
        with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
            results = list(pool.map(fetch_link, urls))
        table('link-checks.csv', results)
        print('Link status counts:', dict(collections.Counter(str(x['status']) for x in results)))
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()
