# Delivery and validation

Status: internal draft for human review, 17 October 2026 AEDT. No public push, new PR, merge, adoption or later-stage promotion was performed.

## Repository state

Repository: `Fusion-Party-Aus/policy-research`; visibility confirmed **PUBLIC** with `gh repo view` before writing the new analysis. Base: `d0ecfac751d2a3d706b083ad753255475e520abf` on `main`; isolated local branch: `agent/policy-researcher/1235c8912a38`. Existing [PR #2](https://github.com/Fusion-Party-Aus/policy-research/pull/2) is open, from `agent/policy-researcher/50ea441694e9` to `main`, inspected at head `70a8128719610594d4e396ad809e169408cac1a3`. It owns the earlier corpus import and was not edited. No unrelated files were changed.

New draft political research requires human approval before public exposure. It is delivered through the internal issue attachment, with a reviewable Git patch. The absence of publication approval is the reason no new PR was opened. Git author identity is also absent; the attempted local commit refused, and no author identity was invented or changed. The independent freeze uses hashes plus a Git tree instead of a commit.

## Checks actually run

- `python3 vic/problem-agenda-f-112/validate_agenda.py`: **33/33 passed**. Includes frozen hashes/tree, rating arithmetic, sensitivity coverage, 18 source IDs, 20 evidence rows, 12 coverage entries, all 66 original corpus pointers/record hashes, 39 associated + 27 unassociated records, unconfirmed protocol, finite caps and local links.
- `python3 vic/problem-agenda-f-112/check_source_links.py`: one bounded request per 18 source URLs plus three access/identity checks. All 18 source URLs returned responses (one PDF); the Europe PMC XML endpoint returned 200, PubMed 203, and the VAHI exception returned 403. See `link-checks.csv` for timestamps, final URLs and sampled-response hashes. Response receipt is not substantive-content validation or evidence appraisal.
- `git diff --cached --check`: initially flagged CSV CRLF line endings as trailing whitespace. These are standard CSV record endings; the frozen source bytes were retained. `git -c core.whitespace=trailing-space,space-before-tab,cr-at-eol diff --cached --check` **passed**. This is a one-command whitespace setting, not a persistent repository configuration change.
- JSON and CSV parsing, local Markdown targets, absence of runtime-local deliverable links and unique identifiers are included in the validator. No code build/linter/test command is defined by this documentation repository; no software dependencies were installed.

The delivery archive additionally records every included file's SHA-256 and byte size. The patch was checked against an isolated copy of the recorded base before delivery. Structural checks do not substitute for human assessment of source adequacy, ranking values, domain coverage or the proposed screening protocol. Original corpus JSON is preserved unchanged; no restricted third-party full text is included.

## Reproduce locally after extracting the archive

From a checkout of the repository with the added folder, run `python3 vic/problem-agenda-f-112/validate_agenda.py`. The historical Git tree may not exist in another clone; that one check requires the original object. The delivery archive includes `independent-freeze.pack` so a reviewer can import the original tree with the documented command in the archive's start file. The SHA-256 checks themselves need no Git objects. Network checks are optional and change over time; rerunning the link script writes a new access record, so retain the delivered copy first.

Human acceptance should consider framing/weights, the unranked child-safety baseline, first-batch scope and protocol/config/pilot adequacy. Mika coordinates the next stage. No intervention-effectiveness conclusion is offered here.
