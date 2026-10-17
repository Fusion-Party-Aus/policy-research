# Audit of the accessible Victorian export

> **Research — not adopted Fusion policy**

**Status:** internal research inventory, for human review. **Author:** Policy Researcher, AI-assisted. **As of:** 17 October 2026 AEDT. Sources are the preserved files linked below, not an assertion of direct Sanity access.

## Findings and reconciliation

The authorised endpoints are [policies](https://vic.fusionparty.org.au/api/policies.json) and [research](https://vic.fusionparty.org.au/api/research.json), with lowercase `/api/`. Sanity remains the source of truth; this audit accessed only its public website exports. Existing material was reused from [PR #2](https://github.com/Fusion-Party-Aus/policy-research/pull/2); its state and exact head/base were checked through GitHub and retained in [origin-pr.json](origin-pr.json). The local import is a fast-forward to its existing commit, preserving its seven files byte-for-byte.

| Population / check | Result | Audit artifact |
| --- | --- | --- |
| Policy objects / root declared policy count | 41 / 41 | proposal-register.csv |
| Research objects / declared count | 25 / no count field | research-register.csv |
| Original manifest title coverage | 66/66 | audit-summary.json; original MANIFEST.md |
| Matrix policy title coverage | 41/41 | audit-summary.json; original evidence-matrix.md |
| Original key points represented verbatim | 149/149 | key-point-register.csv |
| Duplicate IDs, slugs or canonical URLs within each collection | 0 | audit_corpus.py assertions |
| Policy → research links | 34, from 23 policies | cross-references.csv |
| Research → policy links | 34, all reciprocal | cross-references.csv |
| Unresolved exported policy/research links | 0 | cross-references.csv |
| Policies with no linked research | 18 | proposal-register.csv |
| Research with no incoming policy link | 3 | research-register.csv |
| Research source entries / distinct cited URLs | 92 / 79 | citation-instances.csv |
| Exported downloads | 0 across 25 research resources | research-register.csv |
| Records excluded or missing from preserved arrays/registers | 0 / 0 within these 66 records | registers + original JSON pointers |
| Independently assessed policy/research records | 0/41 and 0/25 | coverage-ledger.csv |

The three unlinked research IDs are `research-victoria-transport-governance-branding`, `research-srl-delivery-vago-2026`, and `research-policy-evidence-methodology`. They remain in the register; governance informs C4, SRL informs C2 alternatives, and methodology supports every batch. An unlinked resource is not excluded evidence. All 92 source instances remain distinct, including 13 additional uses of the same URLs; URL deduplication for reachability checks never deletes citation provenance. URL identity is not work identity: this audit does not merge different editions or alternate URLs into inferred single studies.

Every register row identifies the original file and JSON pointer. Record SHA-256 uses UTF-8 JSON with sorted keys, no whitespace separators and `ensure_ascii=False`; it is distinct from a raw response hash. Point IDs concatenate the original policy ID and original `_key`. Slugs and titles are aliases, not replacements for original IDs. Research provenance dates/commit references are preserved as the export's claims; the original omnibus Git history was not separately audited.

## Snapshots and timestamps

The original retrieval log reports 2026-10-16T14:16:29Z. Its policy export generated at 14:16:18.431Z and research export at 14:16:18.954Z. Raw original byte lengths and SHA-256 match exactly:

| File | Bytes | Original SHA-256 |
| --- | --- | --- |
| policies.json | 289580 | `717057699d69ece07f90afd1e58d9473f5b35c2275a2a63a3ecb4f43169e32bf` |
| research.json | 228262 | `df30a305755ffdb09e8bc07eea8ec3be7c04cebcd7da70283b5e778de11d8482` |

Fresh GETs completed at 2026-10-16T14:49:37.948209Z and 14:49:38.104933Z (17 October locally), both HTTP 200 without authentication. They generated at 14:49:36.093Z and 14:49:38.057Z respectively. Exact fresh hashes are:

- policies: `0c01ad0171c441905b82129a435187ddc8c24024f0423812643b6a8be2d768a6`
- research: `a0171102d93ba22b7cb7002c7237397ee33ac623037575c480484cc162b829d7`

The complete object comparisons differ **only** at root `generated_at`: no added, removed or changed policy/research records, no other root changes. Platform update remains `2026-10-12T07:14:15Z`; research collection update remains `2026-10-08T10:57:54Z`. [snapshot-comparison.json](snapshot-comparison.json) also records canonical array hashes. Cache headers allow caching (300 seconds browser/900 seconds shared); this establishes equality between observed responses, not an uncached real-time CMS assertion. The earlier retrieval timestamp is inherited metadata; this audit did not witness the original request.

## Status, authorship and access

All 41 policy objects say `status: adopted`, `authority.status: current policy`, `authority.adopted_policy: true`. Preserve this as **export-declared adopted**, not independently verified formal adoption. These documents contain proposed interventions; their presence does not create 41 newly drafted policies. All 25 research resources say research/evidence with `adopted_policy: false`. Their versions, publisher, published/updated dates and provenance are in the register. No separate draft proposal object is exposed by either endpoint. Unpublished proposals cannot be counted as zero merely because none were returned.

Policy objects have publisher attribution but no explicit author or licence field. Twenty-four research resources export author `Fusion Party Victoria` and licence `CC-BY-4.0`. The accessibility resource (`research-accessible-public-transport-victoria`) has empty authors and null licence. Publisher remains supplied. Do not infer a licence for that item, the policies, or external sources from other records. The repository README also says no project-wide licence has been chosen. These are recorded permission limits for redistribution; the internal audit preserves the already imported material and claims no new unrestricted reuse rights.

All research `downloads` and `related_research` arrays are empty; `external_project_url`, `repository_url` and `doi` are null. All policy `references` arrays and `additional_content_text` strings are empty. There is no policy attachment field. No file download is explicitly exposed, so no attachments were silently discarded from the returned metadata. Embedded citations and provenance include external links; those are inventoried, not recursively imported as documents. The organisation's manifesto URL and canonical collections are pointers to material outside these two arrays, not separately retrieved documents. No third-party restricted full text was copied and no paywall or access control was bypassed.

## Link audit and explicit exceptions

One GET per 150 distinct record-content URLs (337 occurrences), six concurrent requests, 12-second timeout, first 1024 bytes only; checked 16 October UTC/17 October AEDT. All 66 canonical record pages returned 200. Across all 150: **131 HTTP 200, 15 HTTP 403, two HTTP 404, one HTTP 202 and one HTTP 203**. Of the 79 distinct cited URLs: 61 returned 200, 15 returned 403, one 404, one 202, one 203. All results and redirects are retained in [link-checks.csv](link-checks.csv).

The two 404s are the cited `https://www.vic.gov.au/victorias-bus-plan` and a GitHub provenance deep link to `04-homes-and-stations-code.md` in the `state-budget` repository. These are HTTP observations, not proof the works do not exist. No replacement URL was verified in this audit. All failures, affected record IDs and follow-up actions are in [exceptions.csv](exceptions.csv). A 403 may reflect anti-bot controls, access restrictions or other server rules; it is not proof of a broken citation or paywall. The 202/203 responses also need content/identity checks. A 200 can serve a home page, challenge or wrong edition; it proves neither source identity nor claim support. External PDFs, author/year metadata, DOI resolution, retractions and reported numerical results were not comprehensively verified.

## Export omissions and limits of completeness

Neither response exposes page size, cursor, next-page URL, total Sanity document count or draft count. `latest_changes` contains 20 summaries drawn from the policy records, not 20 extra proposals. No pagination is visible; no evidence establishes all CMS documents are exported. Reconciliation is complete **relative to the two observed response arrays** only. Historical versions, unpublished drafts, structured rich-text blocks, images, CMS attachment assets, adoption records, private notes, and upstream research not linked by these exports remain unknown or outside scope. The existing Victorian README explicitly points to a broader omnibus covering other domains; the API is not proof those domains have never been researched. Independent Victorian problem prioritisation belongs to F-112, not this corpus-led gap inventory.

The previous matrix/gap register is useful for locating fields and planning questions. Its “Strong” labels, absence claims and costing observations cannot be treated as independent validation. In particular “no environment/energy policy” overstates the export's coverage boundary: the data-centre policy directly includes energy, water and environmental requirements, and other policies intersect climate and social housing. “Health, education and environment/energy are the three largest expenditure areas” lacks a verified Victorian budget comparison here. Both assertions should be withheld from later evidence synthesis unless separately supported. The prior artifacts are preserved; [methods-and-review.md](methods-and-review.md) records the critique separately.
