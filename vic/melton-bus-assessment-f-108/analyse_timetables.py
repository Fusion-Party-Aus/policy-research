"""Reproduce a bounded 457/459 schedule comparison, using Python's standard library.

Research — not adopted Fusion policy. Scheduled service is not observed performance.
Run --archive /path/to/gtfs.zip once, then without arguments for offline analysis.
Only the selected routes' original rows are retained (DTP, CC BY 4.0).
"""
import argparse
import collections
import csv
import datetime
import hashlib
import io
import json
from pathlib import Path
import statistics
import zipfile

HERE = Path(__file__).resolve().parent
DATA = HERE / 'timetable-data'
DATES = ('20261016', '20261018')


def write_csv(path, rows, fields=None):
    rows = list(rows)
    with path.open('w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=fields or list(rows[0]), lineterminator='\n')
        w.writeheader()
        w.writerows(rows)


def extract(archive):
    DATA.mkdir(exist_ok=True)
    with zipfile.ZipFile(archive) as outer:
        raw = outer.read('4/google_transit.zip')
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        def rows(name):
            return csv.DictReader(io.TextIOWrapper(z.open(name + '.txt'), encoding='utf-8-sig'))
        routes = [r for r in rows('routes') if r['route_short_name'] in ('457', '459')]
        route_ids = {r['route_id'] for r in routes}
        trips = [r for r in rows('trips') if r['route_id'] in route_ids]
        trip_ids = {r['trip_id'] for r in trips}
        service_ids = {r['service_id'] for r in trips}
        # Stream the large statewide stop_times member; never materialise it in RAM.
        times = [r for r in rows('stop_times') if r['trip_id'] in trip_ids]
        stop_ids = {r['stop_id'] for r in times}
        tables = {
            'routes': routes, 'trips': trips, 'stop_times': times,
            'stops': [r for r in rows('stops') if r['stop_id'] in stop_ids],
            'calendar': [r for r in rows('calendar') if r['service_id'] in service_ids],
            'calendar_dates': [r for r in rows('calendar_dates') if r['service_id'] in service_ids],
        }
        for name, data in tables.items():
            write_csv(DATA / (name + '.csv'), data)
        meta = {
            'source_url': 'https://data.ptv.vic.gov.au/downloads/gtfs.zip',
            'archive_sha256': hashlib.file_digest(open(archive, 'rb'), 'sha256').hexdigest(),
            'member': '4/google_transit.zip',
            'member_sha256': hashlib.sha256(raw).hexdigest(),
            'archive_member_timestamp': list(outer_info_date(archive)),
            'license': 'CC BY 4.0; Department of Transport and Planning, Victoria',
            'dates': list(DATES),
            'rows': {name: len(data) for name, data in tables.items()},
            'scope': 'all route IDs numbered 457/459 in metropolitan bus member; calendar exceptions retained',
        }
        (DATA / 'provenance.json').write_text(json.dumps(meta, indent=2) + '\n')


def outer_info_date(archive):
    with zipfile.ZipFile(archive) as z:
        return z.getinfo('4/google_transit.zip').date_time


def active_services(date, calendar, exceptions):
    day = datetime.datetime.strptime(date, '%Y%m%d').strftime('%A').lower()
    active = {r['service_id'] for r in calendar
              if r['start_date'] <= date <= r['end_date'] and r[day] == '1'}
    for r in exceptions:
        if r['date'] == date:
            if r['exception_type'] == '1':
                active.add(r['service_id'])
            elif r['exception_type'] == '2':
                active.discard(r['service_id'])
    return active


def seconds(value):
    h, m, s = map(int, value.split(':'))
    return h * 3600 + m * 60 + s


def analyse():
    def rows(name):
        with (DATA / (name + '.csv')).open() as f:
            return list(csv.DictReader(f))
    routes = {r['route_id']: r for r in rows('routes')}
    trips = {r['trip_id']: r for r in rows('trips')}
    stops = {r['stop_id']: r for r in rows('stops')}
    by_trip = collections.defaultdict(list)
    for r in rows('stop_times'):
        by_trip[r['trip_id']].append(r)
    for data in by_trip.values():
        data.sort(key=lambda r: int(r['stop_sequence']))
    calendar, exceptions = rows('calendar'), rows('calendar_dates')
    departures, pairs, summaries = [], [], []
    for date in DATES:
        active = active_services(date, calendar, exceptions)
        # A shared directed edge, rather than direction_id, proves common travel direction.
        edges = collections.defaultdict(lambda: collections.defaultdict(list))
        for tid, trip in trips.items():
            if trip['service_id'] not in active:
                continue
            route = routes[trip['route_id']]['route_short_name']
            for a, b in zip(by_trip[tid], by_trip[tid][1:]):
                if a.get('pickup_type', '0') == '1' or b.get('drop_off_type', '0') == '1':
                    continue
                edges[(a['stop_id'], b['stop_id'])][route].append((a, b, trip))
        for (start, end), rt in sorted(edges.items()):
            if set(rt) != {'457', '459'}:
                continue
            seq = []
            for route, values in sorted(rt.items()):
                for a, b, trip in values:
                    out = dict(date=date, from_stop=start, from_name=stops[start]['stop_name'],
                               to_stop=end, to_name=stops[end]['stop_name'], route=route,
                               route_id=trip['route_id'], trip_id=trip['trip_id'],
                               direction_id=trip['direction_id'], headsign=trip['trip_headsign'],
                               departure=a['departure_time'], arrival=b['arrival_time'])
                    departures.append(out)
                    sec = seconds(a['departure_time'])
                    if 9 * 3600 <= sec < 15 * 3600:
                        seq.append((sec, route, trip['trip_id']))
            seq.sort()
            if len(seq) < 2:
                continue
            gaps = [(b[0] - a[0]) / 60 for a, b in zip(seq, seq[1:])]
            for a, b in zip(seq, seq[1:]):
                if a[1] != b[1] and b[0] - a[0] <= 300:
                    pairs.append(dict(date=date, from_stop=start, to_stop=end,
                                      route_a=a[1], trip_a=a[2], route_b=b[1], trip_b=b[2],
                                      gap_minutes=(b[0] - a[0]) / 60))
            summaries.append(dict(date=date, from_stop=start, from_name=stops[start]['stop_name'],
                                  to_stop=end, to_name=stops[end]['stop_name'],
                                  window='09:00<=departure<15:00 Australia/Melbourne',
                                  departures_457=sum(x[1] == '457' for x in seq),
                                  departures_459=sum(x[1] == '459' for x in seq),
                                  min_gap_minutes=min(gaps), median_gap_minutes=statistics.median(gaps),
                                  max_gap_minutes=max(gaps),
                                  adjacent_crossroute_pairs_within_5min=sum(
                                      a[1] != b[1] and b[0] - a[0] <= 300
                                      for a, b in zip(seq, seq[1:]))))
    write_csv(HERE / 'shared-corridor-departures.csv', departures)
    write_csv(HERE / 'shared-corridor-summary.csv', summaries)
    write_csv(HERE / 'shared-corridor-close-pairs.csv', pairs,
              ['date', 'from_stop', 'to_stop', 'route_a', 'trip_a', 'route_b', 'trip_b', 'gap_minutes'])
    print(json.dumps(dict(shared_directed_edges=len({(s['from_stop'], s['to_stop']) for s in summaries}),
                          edge_date_summaries=len(summaries), departures=len(departures),
                          close_pair_edge_occurrences=len(pairs)), indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--archive', type=Path)
    args = parser.parse_args()
    if args.archive:
        extract(args.archive)
    analyse()
