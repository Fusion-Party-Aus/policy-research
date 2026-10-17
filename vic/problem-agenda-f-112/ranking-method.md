# Ranking method — frozen version 1

Status: internal research draft, not endorsed policy. Author: Policy Researcher (AI). Date: 17 October 2026. This is a queue for investigation, not a budget allocation or moral ranking of people.

## Selection before corpus mapping

Question: Which outcome deficits warrant bounded Victorian policy research, considering harm, reach, unequal exposure, state influence and the value of resolving uncertainty?

The candidate frame covers secure housing, freedom from violence, mental and physical health, material adequacy, safe and accessible travel, childhood opportunity, ecosystems and fair justice. These are analyst-selected outcome domains, not a representative consultation or comprehensive social-welfare function. Official statistics, independent audits and research inform operationalisation. No Fusion proposal is required. IDs VP-001–VP-012 are permanent; changing rank never changes an ID.

Issue history and repository onboarding disclosed broad party topics and F-107's proposed transport batch. One general search incidentally returned a Fusion bus-research snippet; it was excluded from evidence and scoring. The researcher is therefore **not blinded** to all party context. Policy exports, proposal register, F-107 cluster rankings and topic work plan were withheld until the freeze. Only common research standards and assessment template were read beforehand. This sequencing reduces, but cannot eliminate, framing bias.

## Criteria and anchors

Each ordinal judgement is 1–5. Scores indicate priority for further research; they are not measured effect sizes. The score is `sum(weight × rating)/5`, on a 20–100 scale. Interpolation at 2 and 4 is allowed; uncertain ratings need a reason. Do not add problem scores or populations: the same people and harms recur.

| Criterion | Weight | 1 | 3 | 5 |
| --- | --- | --- | --- | --- |
| Scale | 20 | Narrow/local exposure | Material statewide subgroup | Broad statewide/systemic or ecosystem-wide exposure |
| Harm | 30 | Limited reversible inconvenience | Durable loss of functioning/security | Death, severe injury, serious liberty loss or irreversible ecosystem loss |
| Inequity | 25 | Little established distributional concentration | Plausible concentrated disadvantage | Marked observed disparity or severe exclusion of a disadvantaged group |
| Tractability | 15 | Few state levers | Shared powers or major delivery uncertainty | Direct state influence plus credible tested mechanism and delivery path |
| Uncertainty | 10 | Little decision-relevant uncertainty | Some unresolved baseline/mechanism issues | Major uncertainty likely resolvable within a bounded inquiry |

Uncertainty earns a limited research premium, not an implementation premium. A problem with no verified signal of need cannot enter the scored queue solely because evidence is missing. All current tractability ratings are at most 4: no whole response package is demonstrated. Scale uses qualitative reach, not the count of deaths as if it were all affected people. VP-003 is especially sensitive to this judgement. Ecological scale and irreversible loss enter explicitly; humans may prefer a separate ecological decision track.

Ties: higher harm, then inequity, then scale, then stable ID solely for reproducible display. Adjacent scores are not reliably distinguishable. Source-linked rating rationales are in the problem register. Inequity scores for climate, care and childhood partly reflect testable distributional hypotheses rather than fully extracted Victorian subgroup estimates; lowering those scores is a legitimate sensitivity case.

## Selection and deferral

VP-001 leads under the declared weights. Select **one** first response batch: low-income tenancy sustainment, nested within housing. This is narrower than the problem and does not claim to cover rough sleeping, new supply, owner-occupier costs or all housing mechanisms. VP-002 is the proposed subsequent response tranche because of severe repeat harm and the housing/safety intersection; retain separate survivor outcomes and avoid counting service contacts as success.

VP-012 (child safety/culturally appropriate care) is retained as an **unranked urgent baseline gap**, not assigned a low score. Aboriginal-led framing and child-safety outcomes are needed before scoring. Other sentinels for a later domain scan: chronic disease, disability support outside transport, gambling, insecure work, water quality and governance/service-data quality. No claim of absence or low importance follows from deferral. National-only tax/monetary/international-security mechanisms are outside the first state-response batch, while their Victorian consequences remain relevant.

## Sensitivity and revision

`sensitivity.csv` recalculates: equal weights; harm+inequity emphasis; delivery emphasis; and no uncertainty premium. It also includes an explicit ecological-value scenario and a conservative reduced-scale housing scenario. Housing need remains substantial even if it ceases to lead. Choosing the first batch is a human judgement about the value of information and scope, not a statistical dominance claim.

Freeze the independent register, evidence, sources and method with hashes and a local Git commit before reading proposal contents. Later crosswalks cannot rewrite version 1. New evidence or human weights create a separately dated v2 with a change log; keep v1 and report changes.
