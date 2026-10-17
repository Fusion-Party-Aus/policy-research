# Victorian corpus audit and research work plan — F-107

> **Research — not adopted Fusion policy**

**Status:** internal draft for human acceptance; no policy changes or publication approval. **Jurisdiction:** Victoria, Australia. **Author:** Policy Researcher, AI-assisted. **Review date:** 17 October 2026 AEDT (16 October UTC). **Scope:** stage 1 of F-105 only.

The earlier import is reusable. Its original bytes match the recorded hashes, and a fresh export has the same 41 policy records and 25 research records. Only the two root `generated_at` timestamps changed. All 66 records reconcile to preserved JSON objects and existing manifest entries; all 41 policy titles occur in the existing evidence matrix. The new registers retain IDs, JSON pointers, record hashes, dates, status and provenance. They also expose all **149 key points** for later claim decomposition.

This verifies an inventory, not the proposals' truth or effectiveness. Independent claim assessment remains **0/41 policies and 0/25 research resources**. The prior ratings and gap priorities are inherited annotations, not validated findings. The export declares all 41 policies adopted; no separate draft policy collection is exposed. Adoption instruments and unpublished Sanity content remain unverified.

## Read and use

| Artifact | Purpose |
| --- | --- |
| [Audit report](audit-report.md) | Source reconciliation, PR state, status, rights, omissions and explicit exceptions |
| [Work plan](work-plan.md) | Nine policy clusters, bounded batches, scoring rationale and the separate F-112 boundary |
| [First-batch protocol](first-batch-protocol.md) | Concrete proposed stage-2 scope, searches, comparators and stopping rules |
| [Screening protocol](screening-protocol.md) / [config](screening-config.json) | Proposed eligibility rules; unconfirmed, no screening run |
| [Shared assessment template](assessment-template.md) | Facts, mechanisms, values, economic reasoning, contradictions and allowed verdicts |
| [Coverage ledger](coverage-ledger.csv) | 41 policies + 25 research resources; policy-led evidence work explicitly pending; no F-112 records |
| [Proposal register](proposal-register.csv) / [readable index](proposal-index.md) | Every policy, exact summary, stable ID, original location, metadata and cluster |
| [Key-point register](key-point-register.csv) | All 149 original point/description pairs; not assumed to be 149 distinct proposals or causal claims |
| [Research register](research-register.csv) | All 25 resources, authorship, provenance, dates, version, rights and source counts |
| [Citation instances](citation-instances.csv) | 92 exported source entries, retaining all parent IDs and original source keys; 79 distinct cited URLs |
| [Cross-references](cross-references.csv) | 68 directed links = 34 reciprocal policy/research pairs |
| [URL occurrences](url-occurrences.csv) / [link checks](link-checks.csv) | Every exported content URL occurrence and one HTTP check per distinct URL |
| [Exceptions](exceptions.csv) | Import limits, missing metadata, link/access failures and follow-up owners |
| [Snapshot comparison](snapshot-comparison.json) / [audit summary](audit-summary.json) | Reproducible counts, hashes and content comparison |
| [Fresh retrieval](snapshots/retrieval.json) | Exact response bytes, UTC timestamps, headers and SHA-256; does not overwrite originals |
| [Methods and review](methods-and-review.md) / [search log](search-log.csv) | Skill use, bounded discovery, critique and limitations |
| [Validation record](validation.json) | Checks and their limits, including verbatim source whitespace |

The originals remain in [policies.json](../corpus/policies.json), [research.json](../corpus/research.json), [retrieval log](../corpus/RETRIEVAL-LOG.md) and [manifest](../corpus/MANIFEST.md). The [original matrix](../evidence-matrix.md) and [original gap register](../gap-register.md) are unchanged.

## Delivery boundary

[PR #2](https://github.com/Fusion-Party-Aus/policy-research/pull/2) is OPEN, non-draft, head `agent/policy-researcher/50ea441694e9` at `70a8128719610594d4e396ad809e169408cac1a3`, base `main`. It contains the seven earlier import files and is not linked in Multica's F-105 PR table at inspection. The audit continues locally on the isolated F-107 branch from that head. No PR was merged, retitled or otherwise changed.

The [repository visibility record](repository-visibility.json) says PUBLIC. New analysis and political research drafts were not pushed: public publication requires specific human approval. The issue attachment contains the reviewable work, originals and a Git patch. The new changes are staged on the local task branch, with no new commit or public PR. If publication is approved, use the local patch as a follow-up to PR #2, or target `main` after PR #2 is accepted; do not accidentally use its head branch as the base. Publication approval and policy adoption are distinct decisions.

F-112 owns the independent problem-led ranking and F-113 its response research. This revised pack delivers only the policy-led register/queue; ledgers remain separate and mapping waits until F-112 records its independent ranking. For acceptance, humans should review the scope/omissions, proposed policy-led rankings and B1 protocol. Mika controls later-stage promotion. No later issue has been started, no study screening has run, and no monitoring has been scheduled.

## Reproduce

From the repository root, run `python3 vic/research-plan-f-107/audit_corpus.py`. This regenerates the inventory outputs from the preserved originals and verification snapshots and makes no network requests. `--check-links` explicitly repeats the bounded network check and replaces `link-checks.csv`; retain the existing file before any repeat. Register files describe this stage-1 baseline; record later evidence work in a versioned copy of the coverage ledger, retaining this baseline.

No software build or repository test suite is configured. Validation checks original hashes, object counts, unique IDs/slugs/URLs, all point IDs, manifest/matrix title coverage, reciprocal references and snapshot differences. Separate offline checks reconcile the 66 coverage rows, 41 readable index rows, relative artifact links and the delivery archive. These checks do not validate the policy claims.

## Publication handoff — 17 October 2026

Ethan’s continuation approval, recorded in F-108, supersedes this pack’s historical publication hold. The revised pack from attachment `01a1453f-001b-7e08-9537-d3e8c9a4325c` is now incorporated into existing PR #2. Historical statuses and zero-assessment counts below describe stage 1 at delivery, not current programme progress. Stage 2 is recorded separately; no adopted wording has been amended. All 41 archive payload hashes were checked against the supplied manifest (the manifest lists 41 files); original corpus snapshots remain byte-identical. Source-pack rights metadata is preserved; no external full texts are republished.
