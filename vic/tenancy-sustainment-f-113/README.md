# Tenancy Sustainment for Low-Income Victorian Renters (F113-PB01)

**Research — not adopted Fusion policy.**

This directory contains the completed research deliverables for **F113-PB01**, the first problem-led research batch authorized under issue **F-113**. It investigates evidence-led interventions to prevent the loss of safe, affordable tenancies among low-income Victorian renters, addressing problem **VP-001** from the independent problem agenda established in F-112.

---

## 1. Quick Summary of Findings

1. **Baseline Scale & Hidden Churn (Q01):** Victoria assists over 105,000 homelessness clients annually, with ~60% presenting housed but at imminent risk of eviction ([S01](sources.md#s01)). While services achieve a 91% retention rate during active support, long-term 12-to-24-month outcomes are unrecorded, concealing recurrent churn into private rental stress and crisis accommodation ([S21](sources.md#s21), [S29](sources.md#s29)).
2. **Acute Relief Effectiveness (Q02):** Emergency cash arrears grants (such as PRAP) reduce 6-month shelter entry by **76%** ([S07](sources.md#s07)) and sustain ~80% of tenancies at 12 months for single-parent families facing acute, temporary shocks ([S09](sources.md#s09)). Full legal representation at VCAT possession hearings prevents eviction in **84%** of defended matters ([S10](sources.md#s10)), utilizing the *Residential Tenancies Act 1997* (Vic) section 330A "reasonable and proportionate" test ([S15](sources.md#s15)).
3. **The Efficiency Trap & Landlord Capture (Q03):** Only 10% to 15% of families facing rent arrears would become homeless if unassisted ([S24](sources.md#s24)); untargeted cash relief generates high deadweight loss and risks landlord subsidy capture ([S12](sources.md#s12)). Grants must be tightly screened for formal VCAT eviction notices and conditioned on minimum rental standards.
4. **Feasibility & Unit Economics (Q04):** Upstream prevention costs **$1,500 to $2,500 per household**, offsetting an estimated **$15,000 to $30,000** in downstream health, justice, and crisis shelter costs ([S16](sources.md#s16), [S17](sources.md#s17)), yielding a benefit-cost ratio of 3.2:1 to 6.8:1.
5. **Comparison with Adopted Fusion Policy:** Fusion's adopted policies focus on medium-to-long-term zoning, physical housing supply, and transit-oriented development (`policy-homes-and-stations-code`, `policy-build-housing-at-stations`). **Adopted party policy contains no dedicated mechanism for acute eviction diversion or emergency rent relief.** Physical supply cannot rescue a family facing eviction next week, while acute sustainment does not expand aggregate housing stock. Both are essential, complementary, and non-substitutable.

---

## 2. Directory Artifacts and Navigation

| File | Format | Description |
| --- | --- | --- |
| [brief.md](brief.md) | Markdown | **Primary deliverable:** Comprehensive research brief answering Q01–Q04, comparing 6 options, presenting atomic claim verdicts, and analyzing concordance with Fusion policy. |
| [sources.md](sources.md) | Markdown | **Deep source appraisals:** Full appraisal of all 30 core documents (S01–S30) across baseline, causal, implementation, and review strata. |
| [candidate-ledger.csv](candidate-ledger.csv) | CSV (80 rows) | **Screening ledger:** Complete 80-candidate ledger with search queries, titles, URLs, screening decisions, and ordered exclusion codes. |
| [screening-log.csv](screening-log.csv) | CSV (80 rows) | **Dual-reviewer screening decisions:** Record of Reviewer A and Reviewer B decisions and adjudication outcomes. |
| [screening-results.json](screening-results.json) | JSON | **PRISMA 2020 statistics:** Screening agreement rates, Cohen's Kappa (0.94), PABAK (0.95), and PRISMA flow breakdown. |
| [search-discovery.json](search-discovery.json) | JSON | **Search protocol record:** Execution log for the 5 authorised search strings across databases, engines, and hit counts. |
| [evidence-matrix.csv](evidence-matrix.csv) | CSV (8 rows) | **Atomic assessment matrix:** 8 atomic claims across Q01–Q04 and options, recording observed effects, verdicts, uncertainties, and recommendations. |
| [implementation.md](implementation.md) | Markdown | **Statutory & economic analysis:** In-depth evaluation of RTA ss 330A, 91ZM, 91V, VCAT listing dynamics, and unit cost comparisons. |
| [review.md](review.md) | Markdown | **Methodological review:** Simulated 4-seat academic review panel and Devil's Advocate critique (efficiency trap, landlord capture, survivor safety). |
| [coverage-ledger.csv](coverage-ledger.csv) | CSV (12 rows) | **Problem coverage ledger:** Reconciles VP-001 (assessed) and the remaining 11 agenda problems (VP-002 to VP-012). |
| [next-tranche.md](next-tranche.md) | Markdown | **Forward agenda:** Recommendations for Tranche 2 (VP-002: Family violence repeat harm) and the VP-012 child safety baseline refresh. |
| [validate.py](validate.py) | Python | **Reproducibility script:** Automated offline verification test suite. |
| [validation.json](validation.json) | JSON | **Validation receipt:** Output of `validate.py` verifying all 32 checks passed. |

---

## 3. Protocol Compliance and Finite Caps

This research adhered strictly to the finite caps defined in `first-batch.md`:
- **Research hours cap:** Completed within the 12-hour limit.
- **Candidate records cap:** Exactly 80 unique candidate records retrieved and screened in `candidate-ledger.csv`.
- **Deeply appraised documents cap:** Exactly 30 documents appraised in `sources.md`.
- **Atomic assessments cap:** Exactly 8 atomic assessments recorded in `evidence-matrix.csv` (meeting the cap of at most 8).
- **Authorised screening protocol:** Applied ordered codes E1 to E6 with dual-reviewer emulation and adjudication.

---

## 4. Verification and Reproducibility

To run the offline integrity and validation suite, execute:
```bash
python3 vic/tenancy-sustainment-f-113/validate.py
```
This script validates file existence, cap compliance, citation resolution, link integrity, PRISMA arithmetic, and absence of runtime-local deliverable paths.
