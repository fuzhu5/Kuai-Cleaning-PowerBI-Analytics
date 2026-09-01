#!/usr/bin/env python3
"""Check the public portfolio data before it is committed or shared."""

from __future__ import annotations

import csv
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Dict, List


# Find the generated public-data folder.
DATA_DIR = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[1] / "data" / "sample"
errors: List[str] = []


# List the minimum fields required by the Power BI model.
required: Dict[str, List[str]] = {
    "work_items.csv": [
        "Work Item Key",
        "Work Item Type",
        "Service Date",
        "Client",
        "Approved Client Price",
        "Business Income",
    ],
    "manual_entries.csv": ["Manual Entry Key", "Service Date", "Allocation", "Business Income"],
    "property_periods.csv": ["Property Key", "Billing Period Start", "Job Count", "Quoted Client Price"],
}


# Look for common personal or operational details that must not be public.
sensitive_patterns = {
    "URL": re.compile(r"https?://", re.I),
    "email": re.compile(r"[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}", re.I),
    "Australian mobile": re.compile(r"(?:\+?61|0)4\d{8}"),
    "likely street address": re.compile(r"\b\d{1,5}\s+(?:[A-Za-z]+\s+){0,4}(?:Street|St|Road|Rd|Lane|Ln|Avenue|Ave|Drive|Dr|Way|Parade|Pde)\b", re.I),
    "known worker name": re.compile(r"Watts|Wayne|Andy|Ethan|Ada|Vincent|Yen-Hung|Chieh-yu|An-ting|Yunchao|Jingyao|Ding Zhang", re.I),
}


# Read one public CSV as a list of dictionaries.
def read_csv(path: Path) -> List[Dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


# Check file presence, columns, rows and privacy patterns.
for filename, columns in required.items():
    path = DATA_DIR / filename
    if not path.exists():
        errors.append(f"Missing {filename}")
        continue
    rows = read_csv(path)
    headers = list(rows[0]) if rows else []
    missing = [column for column in columns if column not in headers]
    if missing:
        errors.append(f"{filename} missing columns: {', '.join(missing)}")
    if not rows:
        errors.append(f"{filename} has no rows")
    text = path.read_text(encoding="utf-8")
    for label, pattern in sensitive_patterns.items():
        if pattern.search(text):
            errors.append(f"{filename} contains {label}")


# Check that public Work Item keys are unique.
work_items = read_csv(DATA_DIR / "work_items.csv")
manual_entries = read_csv(DATA_DIR / "manual_entries.csv")
key_counts = Counter(row["Work Item Key"] for row in work_items)
duplicate_keys = [key for key, count in key_counts.items() if count > 1]
if duplicate_keys:
    errors.append(f"Duplicate Work Item Keys: {len(duplicate_keys)}")


# Confirm that the business model contains exactly the three agreed Clients.
client_labels = sorted({row["Client"] for row in work_items})
if client_labels != ["Client 1", "Client 2", "Client 3"]:
    errors.append(f"Unexpected Client labels: {', '.join(client_labels)}")


# Recalculate the accounting identity for every public financial row.
financial_rows = work_items + manual_entries
reconciliation_failures = 0
for row in financial_rows:
    variance = (
        float(row["Approved Client Price"])
        - float(row["Approved Worker Price"])
        - float(row["Cost"])
        - float(row["Business Income"])
    )
    if abs(variance) > 0.01:
        reconciliation_failures += 1
if reconciliation_failures:
    errors.append(f"Financial reconciliation failures: {reconciliation_failures}")


# Stop the release when any check fails.
if errors:
    print("\n".join(errors), file=sys.stderr)
    raise SystemExit(1)

print("PASS: public data has the expected shape, balances financially and passed the privacy scan.")
