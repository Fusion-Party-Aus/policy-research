# Useful bus access in Melton: what survives testing?

> **Research — not adopted Fusion policy**

**Policy Researcher · Victoria · 17 October 2026 AEDT · under human review · AI-assisted**

The four proposals identify a credible access problem. The assessment supports measuring usable journeys and investigating local timetable spacing. It does not establish an optimal grid, a statewide threshold, costless rescheduling, or a costless door-to-door FlexiRide guarantee. Initial verdicts below were recorded without consulting F-113; they are research judgments, not adopted positions.

## Context before choosing a mechanism

Melton municipality had 178,960 residents in the 2021 Census. Among the specified occupied private dwellings, 1,733 (3.2%) reported no motor vehicle; the municipal average was 2.1 vehicles per dwelling. These household figures do not tell us whether every person can drive or use the available vehicle. The Census predates this assessment and its journey-to-work results reflect pandemic conditions. Do not substitute the Melton suburb, electorate or urban-centre geography for LGA24650. [ABS, S02](sources.md#s02)

VAGO distinguishes nearby stops from useful services. Its 2026 audit reports 87% of metropolitan households within 400 metres of a bus but 26% within 800 metres of a high-quality bus. The report groups Casey/Melton public-transport access at 9–12%; it does not warrant assigning either endpoint to Melton without the underlying figure. These are dated audit measures, not a new whole-journey map produced here. [VAGO, S01](sources.md#s01)

The do-minimum comparator includes funded changes, not a frozen pre-2026 network: the April 2026 government announcement includes a Melton South network and Route 454 improvements. An announcement establishes a commitment, not an observed first-service date or realised benefit. Council's current advocacy seeks route reform and an additional $10 million annually; this is an advocacy request, not an independent cost estimate for these four proposals. [Premier, S17](sources.md#s17); [Melton Council, S16](sources.md#s16)

## Twelve initial verdicts

These verdicts concern the specified proposition only. The [matrix](claim-evidence.csv) contains source pointers, assumptions and falsifiers. “Unsupported” means support was not established within this search, not that an effect is impossible.

| Claim | Proposition tested | Verdict and confidence |
| --- | --- | --- |
| C01 | Stop proximity alone overstates useful access | **Supported; moderate.** Frequency/span and journey barriers matter. No neighbourhood-level reachability calculation is claimed. |
| C02 | The cited VAGO transfer figures describe priority sampled connections | **Supported with qualification; moderate.** The detailed analysis reports 73% within a 5–10-minute window for sampled high-priority connections in June 2025, with Laverton using 7–12 minutes. The key findings separately say 68%. Preserve this discrepancy; neither is an all-route observed-success rate. V/Line is excluded. |
| C03 | A frequent direct network would improve Melton access over the current/funded comparator | **Uncertain; low.** Victoria-specific planning/modelling supports testing it, but no Melton counterfactual, costed service plan or local causal estimate establishes superiority. |
| C04 | Network walking plus service measures capture access better than straight-line stop distance | **Supported as a measurement approach; moderate.** Whole-journey guidance corroborates the principle; it does not validate a particular score or crossing dataset. |
| C05 | A uniform statewide distance threshold would be inappropriate across place types | **Supported as a design caution; moderate.** Context and individual mobility matter. Which differentiated floor should be guaranteed remains a value choice informed by further evidence. |
| C06 | An annual access map and funded programme would improve delivery | **Uncertain; low.** It makes delivery testable; a causal improvement beyond existing reporting/planning is not demonstrated. |
| C07 | Current 457/459 schedules cluster on a shared corridor | **Supported locally; high for the extracted schedule.** Both named dates show uneven spacing, with repeated simultaneous Sunday departures on one directed shared section. This is scheduled clustering, not observed traffic-induced bunching. |
| C08 | Staggering can deliver the improvement at zero additional resource cost | **Unsupported; moderate confidence that the categorical claim is unjustified.** Headway arithmetic omits driver/fleet cycles, rail connections, other passengers, planning and contract costs. |
| C09 | Ministerial direction alone is sufficient to implement every timetable correction | **Uncertain; low.** General powers exist, but the reviewed law does not establish the sufficiency of this route for all contracts and operational constraints. |
| C10 | The reported three-hour Woodgrove booking occurred as described | **Uncertain; low.** The historical trip was not independently established; representativeness is separately pending. A current public booking page is not a dispatch history. |
| C11 | Successful overseas DRT typically provides door-to-door delivery | **Unsupported as a general benchmark; moderate.** No representative successful-service denominator establishes “typically”. Stop-to-stop gains show door-to-door is not necessary; a counterexample alone does not disprove a typical pattern. |
| C12 | Tighter FlexiRide delivery standards need no additional service resources | **Unsupported; moderate confidence that the guarantee is uncosted.** A delivery obligation cannot create capacity; demand, detours, refusals and accessibility assistance must be tested. |

Evidence for C01/C02/C06 comes from [S01](sources.md#s01); for C03 from [S03–S04](sources.md#s03) and [S14](sources.md#s14); for C04/C05 from [S09](sources.md#s09) and [S10](sources.md#s10); for C07 from the [new GTFS analysis](timetable-analysis.md); for C08/C09 from [S08](sources.md#s08), [S18](sources.md#s18) and the operational reasoning in [implementation](implementation.md); for C10 from [S07](sources.md#s07); and for C11/C12 from [S10–S13](sources.md#s10). The sources have different roles: legal authority, descriptive evidence and modelled effects are not interchangeable.

## What the current timetable actually shows

The public feed's metropolitan-bus member is dated 15 October 2026. We applied weekday calendars **and date exceptions** for Friday 16 October and Sunday 18 October, retaining all four route IDs numbered 457/459. At Brooklyn Road/Coburns Road, stop 13428, the Sunday schedule has both routes at 09:14, 09:54, 10:34 and then every 40 minutes together through 13:54. At the same directed shared edge, the Friday 09:00–15:00 window has 12 departures per route, with combined gaps from 1 to 34 minutes. The opposite direction differs. See the [complete reproducible comparison](timetable-analysis.md).

Two perfectly regular 40-minute services offset by 20 minutes give a 20-minute shared service. Under uniform random arrivals, the stylised expected wait falls from 20 to 10 minutes. This is **analytical arithmetic**, conditional on either bus being useful, stable travel times and an operationally feasible offset. It is not a measured Melton benefit. The extracted overlap is only three consecutive edges in each direction, and the headsigns diverge. School, train-connection and destination-specific passengers may not be able to substitute between routes. Station access disruptions also affect the baseline. [DTP data, S05](sources.md#s05); [disruption notice, S06](sources.md#s06)

## Counterevidence and credible alternatives

The source exports themselves qualify costs in the `cost` and `funding` fields while some key points and `economic_logic` retain categorical no-new-cost wording. C08/C12 test those categorical claims; the assessment does not silently treat every field of either proposal as costless. Humans should reconcile this internal inconsistency if considering revisions.

The strongest objection to a uniform grid is distributional: faster frequent corridors can still leave some existing users with longer or inaccessible walks. The Richmond study's accessible abstract/introduction reports that aggregate equity conclusions depend on the measures used and baseline access remains poor. Its full methods were unavailable here, so no transferable effect size is asserted. [Liu et al., S14](sources.md#s14)

DRT is neither vindicated nor ruled out as a class. Alonso-González et al.'s Nijmegen case uses stop-to-stop service and compares operational requests with scheduled fixed-transit alternatives. It shows gains without door-to-door, without establishing how typical either design is or predicting Victorian benefit or long-run viability. UWE's English evaluation documents access provision alongside subsidy and unfulfilled-booking challenges; it is a process/monitoring evaluation, with impact/value-for-money work separate. Currie and Fournier provide an adverse survival/cost lead, but only their abstract/preview was available, so numerical failure rates are not treated as independently appraised results. [S13](sources.md#s13); [S11](sources.md#s11); [S12](sources.md#s12)

Compare six options against the funded do-minimum: targeted frequency/span improvements; direct/grid corridors with retained local coverage; feasible timetable coordination; DRT/community or assisted transport for specific trips; walking/crossing/interchange fixes; and fare concessions. Infrastructure Victoria explicitly includes fares, community transport and stop quality alongside service reform. Its WSP model has acknowledged limitations for detailed stops and transfers, so it cannot settle this local package. No option is declared “best” without comparable costs and access outcomes. [S03–S04](sources.md#s03); [options table](implementation.md)

## Human decisions and limits

Consider retaining the useful-access objective and commissioning a constrained local scheduling test. Consider qualifying categorical zero-cost and universal overseas-success wording; **this assessment makes no policy edits**. A mobility floor, acceptable subsidy, tolerated walking burden and distribution of service gains are political choices. Evidence can reveal their consequences, not choose them for the party.

The remaining gaps are substantial: no pedestrian-network audit, dispatch microdata, driver blocks, contract variation clauses, local cost model, current observed reliability, disability-user validation or quantified destination access comparison. The 18-query search was bounded and uneven; three academic sources were partial-text only. No complete systematic search, pooled causal estimate or independence claim is made. [Methods](methods.md), [source appraisals](sources.md) and [next batch](next-batch.md) make those boundaries explicit.
