# Victorian problems and first research agenda — F-112

**Status:** internal draft for human review; not endorsed Fusion policy. **Jurisdiction:** Victoria. **Author:** Policy Researcher, AI-assisted. **Date:** 17 October 2026 AEDT. Factual sources were checked through accessible official pages and one full research article; no independent human peer review occurred.

This pack ranks **11 outcome problems** and retains **one unranked child-safety sentinel**. Housing security leads the proposed research queue. Recommend a bounded first investigation of **preventing loss of safe, affordable tenancies among low-income renters**, capped at 12 research hours, 80 candidate records and 30 deeply appraised documents. This is a recommendation about what to research, not a finding that any response works.

The independently derived ranking was dated and hashed before the policy-export comparison. `ranking-frozen.json` identifies the preserved bytes; `freeze-receipt.json` records the local Git tree. The researcher was not fully blinded to party context: issue history, onboarding and an incidental excluded search snippet were visible. Corpus contents and F-107's policy queue were withheld until the freeze.

## Initial ranking

| Rank | Stable ID | Outcome problem | Research-priority score |
| --- | --- | --- | ---: |
| 1 | VP-001 | Housing insecurity/affordability/suitability | 91 |
| 2 | VP-002 | Family violence and repeat harm | 88 |
| 3 | VP-004 | Climate-related exposure and avoidable harm | 87 |
| 4 | VP-005 | Delays in clinically appropriate care | 86 |
| 5 | VP-010 | Native ecosystem condition and resilience | 85 |
| 6 | VP-011 | Unequal justice exposure and repeat harm | 83 |
| 7 | VP-006 | Inability to afford essential food/home conditions | 82 |
| 8 | VP-003 | Suicide, distress and unmet support | 79 |
| 9 | VP-008 | Exclusion from useful accessible transport | 79 |
| 10 | VP-009 | Early-childhood developmental opportunity | 76 |
| 11 | VP-007 | Road deaths and serious injury | 75 |
| Unranked | VP-012 | Child safety/culturally appropriate care: baseline gap | — |

These are analyst judgements under declared weights: scale 20%, harm 30%, inequity 25%, state tractability 15%, decision-relevant uncertainty 10%. Differences of a few points are not reliably distinguishable. Housing leads all five weight-only scenarios tested. Family violence leads if housing's scale rating falls by one point; biodiversity leads if its inequity/value rating rises to 5. Humans decide weights and the value of ecological loss, rights, distributive priorities and acceptable risk. See [ranking method](ranking-method.md) and [sensitivity calculations](sensitivity.csv).

## Evidence and interpretation

Housing is operationalised using historical Census homelessness rates, recent new-letting rents and allocation-cohort social-housing waits; none alone measures current unmet need. The priority-allocation wait reported for 2024–25 is 17.2 months, including transfers. [VAGO service review](https://www.audit.vic.gov.au/report/service-delivery-performance-2025?section=35269--3-service-delivery-performance-over-time-&show-sections=1)

Severity is not synonymous with deterioration. Recorded family incidents fell in the extracted March 2026 window; a newer June release awaits extraction. Provisional suicides varied between years and the matched partial-2026 count was lower. Road deaths were above the ten-year count average while the per-capita rate was below Australia's. These qualifications remain visible in the source-linked register. [DataVic](https://www.data.vic.gov.au/updated-crime-statistics-and-bail-data-0), [AIHW](https://www.aihw.gov.au/suicide-self-harm-monitoring/geography/states-territories/monthly-suicide-registers), [road data](https://www.vic.gov.au/victorian-road-trauma-statistics)

The Victorian Healthy Homes trial establishes that a relevant state-level intervention can improve some outcomes; its non-significant hospital/ED findings limit claims of acute-care savings. It does not establish homelessness prevention. This is a disconfirming constraint, not a response recommendation. [Page et al., 2025](https://pmc.ncbi.nlm.nih.gov/articles/PMC11865758/)

See [problem register](problem-register.csv) for baselines, groups, harms, state roles and neutral questions; [evidence matrix](evidence-matrix.csv) and [sources](sources.csv) for methods, dates, access, uncertainty and transferability. Baseline observations are separate from causal assumptions, economic reasoning and political choices.

## Differences from the corpus and next decisions

The post-freeze [crosswalk](corpus-crosswalk.csv) finds strong transport overlap and partial housing/justice overlap. Several highly ranked outcomes have no dedicated broad response identified in the reviewed export fields; generic safety or environmental mentions do not close those gaps. Governance/fiscal proposals outside this initial outcome frame remain valid candidates for a later baseline scan. No omission claim extends beyond the 41-policy/25-resource public export. [Comparison and provenance](crosswalk-note.md)

F-107's proposed first policy-led batch tests Melton bus-access proposals. This agenda instead selects housing retention from outcome data. Keep the inquiries and assessment ledgers separate; compare their results later. F-112 does not repeat the import or evaluate the 66 corpus items' evidence. The original export bytes are preserved, without adopted-text changes; Sanity completeness and adoption records remain unverified.

Humans are asked to review the problem framing, value weights, unranked safety gap and [first batch](first-batch.md), then confirm or amend the [screening protocol](screening-protocol.md) and [config](screening-config.json). No formal screening has run. Mika coordinates acceptance and stage promotion through F-105; F-113 and later work stay parked. The proposed following response tranche is family violence, alongside urgent child-safety/baseline validation. No schedule or recurring search was created.

## Review pack navigation and limits

- [Methods and coverage limits](methods-and-limitations.md), [search log](search-log.csv) and [coverage ledger](coverage-ledger.csv).
- [Prioritised residual questions](gap-register.csv), [shared assessment template](assessment-template.md) and [quality review](quality-review.md).
- `provenance/`: unchanged exports and hashes; `corpus-coverage.csv`: all 66 original IDs/pointers and mapping exceptions.
- `validation.json` and `validate_agenda.py`: deterministic checks, plus documented network/access limits.

This is a purposive initial evidence scan, not an exhaustive review, representative consultation, intervention-effectiveness synthesis or completed PRISMA screening. Several distributional effects are hypotheses awaiting subgroup data. Historic, provisional, proxy and inaccessible measures cannot supply a complete contemporary burden comparison. No policy adoption follows.

The GitHub repository is public. New material remains unpushed and no PR was created without publication approval. Git author identity is also absent; no identity was invented or changed. The attached Git patch and archive allow review independently of that limitation.
