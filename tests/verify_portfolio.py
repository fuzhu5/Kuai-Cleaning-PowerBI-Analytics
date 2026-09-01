#!/usr/bin/env python3
"""Run simple checks across the whole GitHub portfolio project."""

from __future__ import annotations

import csv
import json
import re
import sys
from pathlib import Path
from typing import Dict, List


# Find the repository and collect all failures in one run.
ROOT = Path(__file__).resolve().parents[1]
errors: List[str] = []


# Confirm that each part of the project has a file a reviewer can open.
required_files = [
    "README.md",
    "data/sample/work_items.csv",
    "data/sample/manual_entries.csv",
    "data/sample/property_periods.csv",
    "data/sample/data_profile.json",
    "data/sample/business_insights.json",
    "power-query/public-model/FactWorkItem.pq",
    "power-query/public-model/DimClient.pq",
    "power-query/private-pipeline/fnTransformWorkItem.pq",
    "dax/measures.dax",
    "dax/semantic-tests.dax",
    "dax/time-grain-parameter.dax",
    "docs/model-design.md",
    "docs/report-specification.md",
    "powerbi/BUILD_IN_POWER_BI.md",
    "images/executive-overview-preview.svg",
    "images/monthly-performance-preview.svg",
    "images/worker-performance-preview.svg",
    "images/client-analysis-preview.svg",
    "images/property-analysis-preview.svg",
]
for relative_path in required_files:
    if not (ROOT / relative_path).exists():
        errors.append(f"Missing required file: {relative_path}")


# Keep the implementation language consistent with the Python portfolio claim.
ruby_files = list(ROOT.rglob("*.rb"))
if ruby_files:
    errors.append(f"Ruby files remain in the project: {len(ruby_files)}")


# Compare the CSV totals with the published data profile.
profile_path = ROOT / "data" / "sample" / "data_profile.json"
if profile_path.exists():
    profile = json.loads(profile_path.read_text(encoding="utf-8"))
    financial_rows = []
    for filename in ("work_items.csv", "manual_entries.csv"):
        with (ROOT / "data" / "sample" / filename).open("r", encoding="utf-8-sig", newline="") as handle:
            financial_rows.extend(dict(row) for row in csv.DictReader(handle))
    columns: Dict[str, str] = {
        "approved_client_price": "Approved Client Price",
        "approved_worker_price": "Approved Worker Price",
        "cost": "Cost",
        "business_income": "Business Income",
    }
    for profile_key, column in columns.items():
        actual = round(sum(float(row[column]) for row in financial_rows), 2)
        expected = round(float(profile["financial_totals_aud"][profile_key]), 2)
        if actual != expected:
            errors.append(f"Profile mismatch for {column}: {actual} != {expected}")


# Require a comment marker in every code or configuration file.
comment_patterns = {
    ".py": re.compile(r"^\s*#", re.M),
    ".pq": re.compile(r"^\s*//", re.M),
    ".dax": re.compile(r"^\s*//", re.M),
    ".svg": re.compile(r"<!--"),
    ".json": re.compile(r'"_comment"'),
}
for folder in ("scripts", "tests", "power-query", "dax", "powerbi", "images"):
    for path in (ROOT / folder).rglob("*"):
        if path.is_file() and path.suffix in comment_patterns:
            text = path.read_text(encoding="utf-8")
            if not comment_patterns[path.suffix].search(text):
                errors.append(f"Missing block comment marker: {path.relative_to(ROOT)}")


# Catch duplicate DAX measure names before they reach Power BI Desktop.
measure_path = ROOT / "dax" / "measures.dax"
if measure_path.exists():
    measure_names = re.findall(r"^MEASURE\s+'Measures'\[([^\]]+)\]", measure_path.read_text(encoding="utf-8"), re.M)
    duplicate_measures = sorted({name for name in measure_names if measure_names.count(name) > 1})
    if duplicate_measures:
        errors.append(f"Duplicate DAX measures: {', '.join(duplicate_measures)}")


# Check that local links in the main README point to real files.
readme_path = ROOT / "README.md"
if readme_path.exists():
    readme = readme_path.read_text(encoding="utf-8")
    for target in re.findall(r"\[[^\]]+\]\((?!https?:|#)([^)]+)\)", readme):
        clean_target = target.split("#", 1)[0]
        if not (ROOT / clean_target).exists():
            errors.append(f"Broken README link: {target}")


# Stop the release when any project-level check fails.
if errors:
    print("\n".join(errors), file=sys.stderr)
    raise SystemExit(1)

print("PASS: project files, totals, comments and README links are valid.")
