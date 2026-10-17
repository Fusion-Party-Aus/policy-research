"""Offline validation test suite for F-113 tenancy sustainment evidence pack. Standard library only."""
import csv
import json
from pathlib import Path
import re
import sys

HERE = Path(__file__).resolve().parent

def read_csv(filename):
    with (HERE / filename).open(encoding="utf-8") as f:
        return list(csv.DictReader(f))

def main():
    checks = []
    def record_check(name, passed, detail=""):
        checks.append({"check": name, "passed": bool(passed), "detail": str(detail)})
        if not passed:
            print(f"[FAIL] {name}: {detail}", file=sys.stderr)

    # 1. Core file existence
    core_files = [
        "README.md", "brief.md", "sources.md", "candidate-ledger.csv",
        "screening-log.csv", "screening-results.json", "search-discovery.json",
        "evidence-matrix.csv", "implementation.md", "review.md",
        "coverage-ledger.csv", "next-tranche.md"
    ]
    all_files_exist = all((HERE / f).exists() and (HERE / f).stat().st_size > 0 for f in core_files)
    record_check("all_core_files_exist_and_non_empty", all_files_exist, f"{len(core_files)} files checked")

    # 2. Candidate ledger caps and counts
    candidates = read_csv("candidate-ledger.csv")
    record_check("candidate_ledger_count_equals_80", len(candidates) == 80, f"Found {len(candidates)}")
    cids = {r["candidate_id"] for r in candidates}
    record_check("candidate_ids_unique", len(cids) == 80, f"{len(cids)} unique IDs")

    deeply_appraised = [r for r in candidates if r["appraisal_state"] == "deeply_appraised"]
    screened_out = [r for r in candidates if r["appraisal_state"] == "screened_out"]
    record_check("exactly_30_deeply_appraised_documents", len(deeply_appraised) == 30, f"Found {len(deeply_appraised)}")
    record_check("exactly_50_screened_out_records", len(screened_out) == 50, f"Found {len(screened_out)}")

    # 3. Source appraisals in sources.md
    sources_text = (HERE / "sources.md").read_text(encoding="utf-8")
    source_headers = set(re.findall(r"^### (S\d{2})$", sources_text, re.M))
    record_check("sources_md_contains_30_appraised_sources", len(source_headers) == 30, f"Found {len(source_headers)} headers")
    expected_sids = {f"S{i:02d}" for i in range(1, 31)}
    record_check("source_ids_match_S01_to_S30", source_headers == expected_sids, f"Matched {len(source_headers & expected_sids)}/30")

    # 4. Screening log and PRISMA consistency
    screening_log = read_csv("screening-log.csv")
    record_check("screening_log_count_equals_80", len(screening_log) == 80, f"Found {len(screening_log)}")
    results_json = json.loads((HERE / "screening-results.json").read_text(encoding="utf-8"))
    flow = results_json["prisma_2020_flow"]
    record_check("prisma_screened_equals_80", flow["identification"]["unique_records_screened"] == 80)
    record_check("prisma_included_equals_30", flow["included"]["studies_included_in_deep_appraisal"] == 30)
    record_check("prisma_excluded_reconciles", 
                 flow["screening"]["records_excluded_title_abstract"] + flow["full_text_eligibility"]["reports_excluded_at_full_text"] == 50)
    record_check("ordered_exclusion_codes_valid",
                 all(r["exclusion_code"] in ["none", "E1", "E2", "E3", "E4", "E5", "E6"] for r in candidates))

    # 5. Search discovery log
    search_json = json.loads((HERE / "search-discovery.json").read_text(encoding="utf-8"))
    record_check("five_search_queries_logged", len(search_json["queries"]) == 5, f"{len(search_json['queries'])} queries")
    record_check("raw_search_deduplication_equals_80", search_json["deduplication"]["unique_candidates_ledgered"] == 80)

    # 6. Evidence matrix and atomic assessments cap
    evidence = read_csv("evidence-matrix.csv")
    record_check("atomic_assessments_cap_satisfied", 1 <= len(evidence) <= 8, f"Found {len(evidence)} assessments")
    record_check("exactly_8_atomic_assessments", len(evidence) == 8, f"Found {len(evidence)}")
    a_ids = {r["assessment_id"] for r in evidence}
    record_check("assessment_ids_unique", len(a_ids) == len(evidence))

    allowed_verdicts = {
        "well supported", "right objective but weak mechanism",
        "unsubstantiated", "overlooked consequences",
        "better alternative", "insufficient evidence"
    }
    record_check("all_verdicts_are_allowed", all(r["verdict"] in allowed_verdicts for r in evidence),
                 f"Verdicts: {set(r['verdict'] for r in evidence)}")

    # 7. Citation join integrity
    all_cited_sources = set()
    for row in evidence:
        for sid in row["evidence_sources"].split(";"):
            all_cited_sources.add(sid.strip())
    record_check("all_cited_sources_exist_in_sources_md", all_cited_sources <= source_headers,
                 f"{len(all_cited_sources)} cited sources all resolve")

    # 8. Coverage ledger integrity
    coverage = read_csv("coverage-ledger.csv")
    record_check("coverage_ledger_has_12_problems", len(coverage) == 12, f"Found {len(coverage)}")
    expected_pids = {f"VP-{i:03d}" for i in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]}
    record_check("coverage_problem_ids_match_freeze", {r["problem_id"] for r in coverage} == expected_pids)
    vp001 = next(r for r in coverage if r["problem_id"] == "VP-001")
    record_check("vp001_marked_as_first_batch_completed", 
                 vp001["stage_2_status"] == "first_batch_completed_tenancy_sustainment" and int(vp001["atomic_assessments_completed"]) == 8)

    # 9. Prominent label check in all Markdown files
    label = "Research — not adopted Fusion policy"
    md_files = list(HERE.glob("*.md"))
    record_check("markdown_files_count_at_least_6", len(md_files) >= 6, f"Found {len(md_files)} files")
    all_labeled = all(label in p.read_text(encoding="utf-8") for p in md_files)
    record_check("all_markdown_files_prominently_labeled", all_labeled, f"{len(md_files)} files checked")

    # 10. Local link checks
    broken_links = []
    abs_links = []
    for p in md_files:
        text = p.read_text(encoding="utf-8")
        if "/home/ethan/" in text or "file://" in text:
            abs_links.append(p.name)
        for target in re.findall(r"\]\(([^)]+)\)", text):
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            clean_target = target.split("#")[0]
            if clean_target == "validation.json":
                continue
            if clean_target and not (p.parent / clean_target).exists():
                broken_links.append(f"{p.name} -> {target}")

    record_check("no_runtime_local_deliverable_links", len(abs_links) == 0, f"Found in: {abs_links}")
    record_check("all_relative_markdown_links_resolve", len(broken_links) == 0, f"Broken: {broken_links}")

    # Produce validation receipt
    all_passed = all(c["passed"] for c in checks)
    receipt = {
        "status": "passed" if all_passed else "failed",
        "passed_checks": sum(1 for c in checks if c["passed"]),
        "total_checks": len(checks),
        "failed_checks": [c for c in checks if not c["passed"]],
        "checks": checks,
        "counts": {
            "unique_candidate_records": len(candidates),
            "deeply_appraised_sources": len(deeply_appraised),
            "screened_out_records": len(screened_out),
            "atomic_assessments": len(evidence),
            "problems_in_coverage_ledger": len(coverage),
            "markdown_files_checked": len(md_files)
        }
    }
    (HERE / "validation.json").write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": receipt["status"], "passed": receipt["passed_checks"], "total": receipt["total_checks"]}, indent=2))
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())
