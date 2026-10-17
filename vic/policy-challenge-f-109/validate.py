"""Offline validation test suite for F-109 policy challenge evidence pack. Standard library only."""
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
        "README.md", "brief.md", "cross-examination.md",
        "critique-policy-led.md", "critique-problem-led.md",
        "corpus-contradictions.md", "severity-register.csv",
        "challenge-matrix.csv", "rating-corrections.csv",
        "sources.md", "next-tranche.md", "LEARNINGS.md"
    ]
    all_files_exist = all((HERE / f).exists() and (HERE / f).stat().st_size > 0 for f in core_files)
    record_check("all_core_files_exist_and_non_empty", all_files_exist, f"{len(core_files)} files checked")

    # 2. Severity register schema, counts, and contents
    severity_rows = read_csv("severity-register.csv")
    record_check("severity_register_count_at_least_25", len(severity_rows) >= 25, f"Found {len(severity_rows)} findings")
    fids = {r["finding_id"] for r in severity_rows}
    record_check("finding_ids_unique", len(fids) == len(severity_rows), f"{len(fids)} unique IDs")
    
    allowed_severities = {"CRITICAL", "MAJOR", "MINOR", "NONE"}
    record_check("severity_values_valid", all(r["severity"] in allowed_severities for r in severity_rows))
    
    critical_count = sum(1 for r in severity_rows if r["severity"] == "CRITICAL")
    major_count = sum(1 for r in severity_rows if r["severity"] == "MAJOR")
    none_count = sum(1 for r in severity_rows if r["severity"] == "NONE")
    record_check("has_critical_findings", critical_count >= 2, f"Found {critical_count} CRITICAL")
    record_check("has_major_findings", major_count >= 10, f"Found {major_count} MAJOR")
    record_check("has_verified_strengths_no_material_weakness", none_count >= 2, f"Found {none_count} verified strengths")

    # 3. Challenge matrix schema and counts
    matrix_rows = read_csv("challenge-matrix.csv")
    record_check("challenge_matrix_count_at_least_20", len(matrix_rows) >= 20, f"Found {len(matrix_rows)} items")
    mids = {r["matrix_id"] for r in matrix_rows}
    record_check("matrix_ids_unique", len(mids) == len(matrix_rows), f"{len(mids)} unique IDs")

    # 4. Rating corrections schema and counts
    rating_rows = read_csv("rating-corrections.csv")
    record_check("rating_corrections_count_at_least_10", len(rating_rows) >= 10, f"Found {len(rating_rows)} corrections")
    rids = {r["item_id"] for r in rating_rows}
    record_check("rating_item_ids_unique", len(rids) == len(rating_rows), f"{len(rids)} unique IDs")

    # 5. Source appraisals in sources.md
    sources_text = (HERE / "sources.md").read_text(encoding="utf-8")
    source_headers = set(re.findall(r"^### (S\d{2})$", sources_text, re.M))
    record_check("sources_md_contains_20_sources", len(source_headers) == 20, f"Found {len(source_headers)} headers")
    expected_sids = {f"S{i:02d}" for i in range(1, 21)}
    record_check("source_ids_match_S01_to_S20", source_headers == expected_sids, f"Matched {len(source_headers & expected_sids)}/20")

    # 6. Prominent label check in all Markdown files
    label = "Research — not adopted Fusion policy"
    md_files = list(HERE.glob("*.md"))
    record_check("markdown_files_count_at_least_7", len(md_files) >= 7, f"Found {len(md_files)} files")
    all_labeled = all(label in p.read_text(encoding="utf-8") for p in md_files)
    record_check("all_markdown_files_prominently_labeled", all_labeled, f"{len(md_files)} files checked")

    # 7. Local relative link checks and absence of runtime paths
    broken_links = []
    abs_links = []
    for p in md_files:
        text = p.read_text(encoding="utf-8")
        if "/home/ethan/" in text or "file://" in text:
            abs_links.append(p.name)
        for target in re.findall(r"\]\(([^)]+)\)", text):
            if target.startswith(("http://", "https://", "mailto:", "#", "mention://")):
                continue
            clean_target = target.split("#")[0]
            if clean_target in ("validation.json", ""):
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
            "severity_findings": len(severity_rows),
            "critical_findings": critical_count,
            "major_findings": major_count,
            "verified_strengths": none_count,
            "challenge_matrix_entries": len(matrix_rows),
            "rating_corrections": len(rating_rows),
            "sources_appraised": len(source_headers),
            "markdown_files_checked": len(md_files)
        }
    }
    (HERE / "validation.json").write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": receipt["status"], "passed": receipt["passed_checks"], "total": receipt["total_checks"]}, indent=2))
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())
