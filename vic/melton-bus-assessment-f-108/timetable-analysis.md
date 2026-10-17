# A reproducible current check of routes 457 and 459

> **Research — not adopted Fusion policy**

Policy Researcher · 17 October 2026 AEDT · under human review. Source: Department of Transport and Planning, [Victorian GTFS](https://data.ptv.vic.gov.au/downloads/gtfs.zip), [dataset/CC BY 4.0 attribution](https://discover.data.vic.gov.au/dataset/timetable-and-geographic-information-gtfs). Analysis is new research; underlying selected rows retain their original values.

## What was extracted

The statewide archive was retrieved at 23:50:10 UTC on 16 October (10:50:10 AEDT on 17 October). Metropolitan-bus member `4/google_transit.zip` has an archive timestamp of 15 October 2026 10:50:18 (timezone unspecified by ZIP). See [provenance](timetable-data/provenance.json) for original archive/member SHA-256 hashes and selected table counts: 4 route IDs, 753 trips, 19,573 stop-time rows, 92 stops, 18 service calendars and 333 date exceptions. A route number is not a unique route ID; retaining all matching IDs matters for temporary service patterns.

Analysis dates: **Friday 16 October 2026** and **Sunday 18 October 2026**, using the same release. The latter is a prospective schedule, not a service already observed. Standard weekly calendars are filtered by start/end dates; `calendar_dates` additions/removals are then applied. After filtering we identify identical **directed consecutive stop pairs** served by both routes. Direction IDs alone are not used to infer common direction. Non-pickup/non-dropoff rows are removed from edge comparisons. This yields six shared directed edges (three each way), with twelve edge/date summaries. It is a conservative overlap definition; shared paths with different intermediate stops may be missed.

All eligible departures are retained in [shared-corridor-departures.csv](shared-corridor-departures.csv). Summaries use `09:00 <= departure < 15:00`, in local timetable time; gaps are between consecutive departures within the window, not the boundary waits before/after it. A close pair is adjacent cross-route departures no more than five minutes apart. Counts repeated on adjacent edges are **not unique buses, riders or independent events**. No observed running times, occupancy, complete passenger destination substitutability or rail-transfer matching was analysed.

## Main finding

| Directed edge | Date | 457 / 459 departures in window | Combined minimum / median / maximum gap (minutes) | Close pairs |
| --- | --- | --- | --- | --- |
| Brooklyn Rd/Coburns Rd 13428 → Campaspe Cres/Coburns Rd 13427 | Friday 16 October | 12 / 12 | 1 / 4 / 34 | 12 |
| Same edge | Sunday 18 October | 9 / 10 | 0 / 15 / 40 | 8 |
| Richard Rd/Coburns Rd 13374 → Joy St/Coburns Rd 13375 | Friday 16 October | 12 / 12 | 2 / 9 / 29 | 1 |
| Same opposite-direction corridor | Sunday 18 October | 9 / 9 | 7 / 7 / 33 | 0 |

The Sunday simultaneous pattern at 13428 repeats every 40 minutes from 09:14 to 13:54; later departures change. The weekday pattern is neither two uniform 40-minute routes nor identical to Sunday. Signs/GTFS headsigns show different destinations after the shared part. This supports the narrow proposition that selected current schedules cluster, not that a uniform statewide change doubles useful service for every rider. The [station disruption notice](https://transport.vic.gov.au/disruptions/disruptions-information/article/melton-station) also records temporary stop/access arrangements; no separate journey accessibility audit was performed.

For a stylised repeating 40/0-minute gap pattern, uniform random passenger arrivals imply expected waiting `sum(gap²)/(2*sum(gap)) = 20 minutes`. A feasible 20/20 offset gives `10 minutes`. This scenario assumes the same destinations are usable on either service, no capacity/transfer constraints, no reliability change and no strategic passenger arrival behaviour. It is arithmetic, not an empirical welfare estimate or a tested operating plan. Medians above are descriptive headway medians; they must not be read as passenger-weighted expected waiting times.

## Reproduction and checks

From the repository root, run `python3 vic/melton-bus-assessment-f-108/analyse_timetables.py` to regenerate all three analytical CSVs from the committed filtered input. Standard library only. To reproduce extraction, download the official feed independently, verify its archive hash against the receipt, then run the script with `--archive /path/to/gtfs.zip`. The live URL changes; a different hash is a new release and is not expected to reproduce these exact dates/results.

Offline validation checks date exceptions override regular calendars, hours above 24 are parsed, outputs reproduce byte-for-byte, all extracted rows resolve, and the eight Sunday simultaneous pairs match the retained records. This analysis does not model new offsets or prove driver/fleet feasibility. No live timetable was changed.
