#!/usr/bin/env python3
"""Build privacy-safe portfolio data from private cleaning-business exports."""

from __future__ import annotations

import csv
import hashlib
import json
import re
import sys
from collections import defaultdict
from datetime import date
from pathlib import Path
from typing import Dict, Iterable, List, Sequence


# Keep private input and public output locations separate.
SOURCE_DIR = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd() / "data" / "private"
OUTPUT_DIR = Path(sys.argv[2]) if len(sys.argv) > 2 else Path(__file__).resolve().parents[1] / "data" / "sample"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# Create repeatable public keys without publishing source identifiers.
def stable_key(prefix: str, value: object) -> str:
    if value is None or str(value) == "":
        return ""
    digest = hashlib.sha256(str(value).encode("utf-8")).hexdigest()[:8].upper()
    return f"{prefix}-{digest}" if prefix else digest


# Normalise source Boolean values for portable CSV output.
def bool_text(value: object) -> str:
    return "true" if str(value).lower() == "true" else "false"


# Format all financial values to two decimal places.
def amount(value: object) -> str:
    return f"{float(value or 0):.2f}"


# Keep real dates and timestamps while removing the identifying fields around them.
def source_value(value: object) -> str:
    return "" if value is None else str(value)


# Keep the real financial values from each source row.
def source_financials(row: Dict[str, str]) -> Sequence[float]:
    client = round(float(row.get("approved_client_price") or 0), 2)
    worker = round(float(row.get("approved_worker_price") or 0), 2)
    cost = round(float(row.get("cost") or 0), 2)
    business = round(float(row.get("business_income") or 0), 2)
    return client, worker, cost, business


# Turn private descriptions into broad, safe work categories.
def work_category(description: object, record_type: str) -> str:
    text = str(description or "").lower()
    if re.search(r"clean|清洁|深清|清房|退房|打扫|浴室|阳台", text):
        return "Cleaning"
    if re.search(r"key|钥匙|锁盒|fob|遥控器", text):
        return "Key handling"
    if re.search(r"deliver|delivery|邮寄|送|取|带到|拿到", text):
        return "Delivery or collection"
    if re.search(r"inspect|inspection|检查|查房|照片", text):
        return "Inspection"
    if re.search(r"repair|maintenance|维修|更换|坏|问题", text):
        return "Maintenance"
    return "Standard service" if record_type == "Job" else "Other task"


# Read UTF-8 CSV files and allow a file to contain no header or rows.
def read_csv(path: Path) -> List[Dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames:
            return []
        return [dict(row) for row in reader]


# Write columns in a stable order for Power Query.
def write_csv(path: Path, fieldnames: Sequence[str], rows: Iterable[Dict[str, object]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


# Find each family of private exports.
job_paths = sorted(SOURCE_DIR.glob("kuai_jobs_*.csv"))
task_paths = sorted(SOURCE_DIR.glob("kuai_tasks_*.csv"))
manual_paths = sorted(SOURCE_DIR.glob("kuai_manual_entries_*.csv"))
property_paths = sorted(SOURCE_DIR.glob("kuai_properties_*.csv"))
if any(not paths for paths in (job_paths, task_paths, manual_paths, property_paths)):
    raise FileNotFoundError("Expected Jobs, Tasks, Manual Entries and Properties CSV files")


# Replace real filenames with safe period labels.
source_file_map: Dict[str, str] = {}
for family, paths in {
    "jobs": job_paths,
    "tasks": task_paths,
    "manual_entries": manual_paths,
    "properties": property_paths,
}.items():
    for index, path in enumerate(paths, start=1):
        source_file_map[path.name] = f"{family}_period_{index:02d}.csv"


# Map the three private source accounts directly to the three public Clients.
source_work_rows = [row for path in job_paths + task_paths for row in read_csv(path)]
account_values = sorted({row.get("account", "") for row in source_work_rows if row.get("account")})
client_map = {value: f"Client {index + 1}" for index, value in enumerate(account_values)}
if len(client_map) != 3:
    raise ValueError(f"Expected exactly three Clients, found {len(client_map)}")
worker_name_to_id = {
    row["completed_by"]: row["completed_by_id"]
    for row in source_work_rows
    if row.get("completed_by") and row.get("completed_by_id")
}


# Combine Jobs and Tasks at one work-item level.
work_items: List[Dict[str, object]] = []
sequence = 0
for paths, record_type in ((job_paths, "Job"), (task_paths, "Task")):
    for path in paths:
        for row in read_csv(path):
            sequence += 1
            client, worker, cost, business = source_financials(row)
            work_items.append(
                {
                    "Billing Period Start": source_value(row["billing_term_start"]),
                    "Billing Period End": source_value(row["billing_term_end"]),
                    "Work Item Key": f"WI-{sequence:04d}",
                    "Work Item Type": record_type,
                    "Service Date": source_value(row["service_date"]),
                    "Property Key": stable_key("PROP", row["property_id"]),
                    "Client": client_map.get(row.get("account", ""), "Unknown Client"),
                    "Work Category": work_category(row.get("description"), record_type),
                    "Worker Key": stable_key("WRK", row.get("completed_by_id")),
                    "Default Worker Key": stable_key("WRK", worker_name_to_id.get(row.get("default_worker", ""))),
                    "Assignment Overridden": bool_text(row.get("worker_assignment_overridden")),
                    "Approved Client Price": amount(client),
                    "Approved Worker Price": amount(worker),
                    "Cost": amount(cost),
                    "Business Income": amount(business),
                    "Pricing Status": row.get("pricing_status", ""),
                    "Price Approved At": source_value(row.get("price_approved_at")),
                    "Worker Price Overridden": bool_text(row.get("worker_price_overridden")),
                    "Ready For Billing": bool_text(row.get("ready_for_billing")),
                    "No Payment": bool_text(row.get("no_payment")),
                    "Public Holiday Flag": "false" if not row.get("public_holiday") else "true",
                    "Source File": source_file_map[path.name],
                }
            )


# Transform manual adjustments without keeping their descriptions.
manual_entries: List[Dict[str, object]] = []
for path in manual_paths:
    for row in read_csv(path):
        client, worker, cost, business = source_financials(row)
        manual_entries.append(
            {
                "Billing Period Start": source_value(row["billing_term_start"]),
                "Billing Period End": source_value(row["billing_term_end"]),
                "Manual Entry Key": stable_key("ADJ", row["manual_entry_id"]),
                "Service Date": source_value(row["service_date"]),
                "Adjustment Category": "Negative adjustment" if business < 0 else "Positive adjustment",
                "Allocation": row.get("allocation", ""),
                "Worker Key": stable_key("WRK", row.get("completed_by_id")),
                "Approved Client Price": amount(client),
                "Approved Worker Price": amount(worker),
                "Cost": amount(cost),
                "Business Income": amount(business),
                "Status": row.get("status", ""),
                "Approved Or Updated At": source_value(row.get("approved_or_updated_at")),
                "Source File": source_file_map[path.name],
            }
        )


# Keep property activity by period while removing addresses and names.
property_periods: List[Dict[str, object]] = []
for path in property_paths:
    for row in read_csv(path):
        property_periods.append(
            {
                "Billing Period Start": source_value(row["billing_term_start"]),
                "Billing Period End": source_value(row["billing_term_end"]),
                "Property Key": stable_key("PROP", row["property_id"]),
                "Property Label": f"Property {stable_key('', row['property_id'])[:6]}",
                "Job Count": int(row.get("job_count") or 0),
                "Task Count": int(row.get("task_count") or 0),
                "Bedrooms": row.get("bedrooms", ""),
                "Bathrooms": row.get("bathrooms", ""),
                "Quoted Client Price": amount(row.get("quoted_client_price") or 0),
                "Quoted Worker Price": amount(row.get("quoted_worker_price") or 0),
                "Quote Start": source_value(row.get("quote_start")),
                "Quote End": source_value(row.get("quote_end")),
                "Source File": source_file_map[path.name],
            }
        )


# Publish the three tables used by the public Power BI model.
write_csv(OUTPUT_DIR / "work_items.csv", list(work_items[0]), work_items)
write_csv(OUTPUT_DIR / "manual_entries.csv", list(manual_entries[0]), manual_entries)
write_csv(OUTPUT_DIR / "property_periods.csv", list(property_periods[0]), property_periods)


# Calculate a simple machine-readable profile for release checks.
financial_rows = work_items + manual_entries


def total(column: str) -> float:
    return round(sum(float(row[column]) for row in financial_rows), 2)


periods = sorted({str(row["Billing Period Start"]) for row in financial_rows})
profile = {
    "_comment": "This profile keeps real source dates and amounts while using anonymous public identities.",
    "evidence_maturity": "Anonymised local portfolio data with real source dates and financial values",
    "source_period_start": periods[0],
    "source_period_end": max(str(row["Billing Period End"]) for row in financial_rows),
    "billing_periods": len(periods),
    "row_counts": {
        "work_items": len(work_items),
        "jobs": sum(row["Work Item Type"] == "Job" for row in work_items),
        "tasks": sum(row["Work Item Type"] == "Task" for row in work_items),
        "manual_entries": len(manual_entries),
        "property_period_snapshots": len(property_periods),
        "distinct_properties": len({row["Property Key"] for row in property_periods}),
    },
    "financial_totals_aud": {
        "approved_client_price": total("Approved Client Price"),
        "approved_worker_price": total("Approved Worker Price"),
        "cost": total("Cost"),
        "business_income": total("Business Income"),
    },
    "quality_observations": {
        "financial_reconciliation_failures": sum(
            abs(
                float(row["Approved Client Price"])
                - float(row["Approved Worker Price"])
                - float(row["Cost"])
                - float(row["Business Income"])
            )
            > 0.01
            for row in financial_rows
        ),
        "negative_financial_records": sum(
            any(float(row[column]) < 0 for column in ("Approved Client Price", "Approved Worker Price", "Cost", "Business Income"))
            for row in financial_rows
        ),
        "assignment_overrides": sum(row["Assignment Overridden"] == "true" for row in work_items),
        "price_overrides": sum(row["Worker Price Overridden"] == "true" for row in work_items),
        "empty_manual_entry_files": sum(not read_csv(path) for path in manual_paths),
        "client_count": len(client_map),
    },
}


# Build plain-language business summaries for the README and dashboard notes.
period_rows: Dict[str, List[Dict[str, object]]] = defaultdict(list)
for row in financial_rows:
    period_rows[str(row["Billing Period Start"])].append(row)
latest_period, previous_period = periods[-1], periods[-2]


def period_metrics(period: str) -> Dict[str, float]:
    rows = period_rows[period]
    work_rows = [row for row in work_items if row["Billing Period Start"] == period]
    manual_rows = [row for row in manual_entries if row["Billing Period Start"] == period]
    revenue = round(sum(float(row["Approved Client Price"]) for row in rows), 2)
    income = round(sum(float(row["Business Income"]) for row in rows), 2)
    work_revenue = round(sum(float(row["Approved Client Price"]) for row in work_rows), 2)
    work_income = round(sum(float(row["Business Income"]) for row in work_rows), 2)
    return {
        "revenue": revenue,
        "business_income": income,
        "margin_pct": round(income / revenue * 100, 1) if revenue else 0.0,
        "work_items": len(work_rows),
        "work_item_revenue": work_revenue,
        "work_item_business_income": work_income,
        "manual_business_income": round(sum(float(row["Business Income"]) for row in manual_rows), 2),
        "average_revenue_per_work_item": round(work_revenue / len(work_rows), 2) if work_rows else 0.0,
        "average_business_income_per_work_item": round(work_income / len(work_rows), 2) if work_rows else 0.0,
    }


latest = period_metrics(latest_period)
previous = period_metrics(previous_period)
worker_keys = sorted({str(row["Worker Key"]) for row in financial_rows if row.get("Worker Key")})
worker_labels = {key: f"Worker {index:02d}" for index, key in enumerate(worker_keys, start=1)}
worker_details = []
for worker_key in worker_keys:
    rows = [row for row in work_items if row["Worker Key"] == worker_key]
    if not rows:
        continue
    revenue = round(sum(float(row["Approved Client Price"]) for row in rows), 2)
    payout = round(sum(float(row["Approved Worker Price"]) for row in rows), 2)
    income = round(sum(float(row["Business Income"]) for row in rows), 2)
    latest_count = sum(row["Billing Period Start"] == latest_period for row in rows)
    previous_count = sum(row["Billing Period Start"] == previous_period for row in rows)
    worker_details.append(
        {
            "worker": worker_labels[worker_key],
            "work_items": len(rows),
            "jobs": sum(row["Work Item Type"] == "Job" for row in rows),
            "tasks": sum(row["Work Item Type"] == "Task" for row in rows),
            "client_revenue": revenue,
            "worker_payout": payout,
            "business_income": income,
            "average_revenue_per_work_item": round(revenue / len(rows), 2),
            "average_payout_per_work_item": round(payout / len(rows), 2),
            "workload_vs_team_average_pct": round((len(rows) / (len(work_items) / len(worker_keys)) - 1) * 100, 1),
            "latest_period_work_items": latest_count,
            "previous_period_work_items": previous_count,
            "work_item_change_pct": round((latest_count / previous_count - 1) * 100, 1) if previous_count else None,
        }
    )


client_details = []
for client_label in sorted({str(row["Client"]) for row in work_items}):
    rows = [row for row in work_items if row["Client"] == client_label]
    latest_rows = [row for row in rows if row["Billing Period Start"] == latest_period]
    previous_rows = [row for row in rows if row["Billing Period Start"] == previous_period]
    revenue = round(sum(float(row["Approved Client Price"]) for row in rows), 2)
    income = round(sum(float(row["Business Income"]) for row in rows), 2)
    latest_revenue = round(sum(float(row["Approved Client Price"]) for row in latest_rows), 2)
    previous_revenue = round(sum(float(row["Approved Client Price"]) for row in previous_rows), 2)
    client_details.append(
        {
            "client": client_label,
            "work_items": len(rows),
            "properties": len({str(row["Property Key"]) for row in rows}),
            "client_revenue": revenue,
            "revenue_share_pct": round(revenue / sum(float(row["Approved Client Price"]) for row in work_items) * 100, 1),
            "business_income": income,
            "margin_pct": round(income / revenue * 100, 1) if revenue else 0.0,
            "latest_period_revenue": latest_revenue,
            "previous_period_revenue": previous_revenue,
            "revenue_change_pct": round((latest_revenue / previous_revenue - 1) * 100, 1) if previous_revenue else None,
        }
    )


# Summarise real monthly results and flag the two edge months as partial.
month_rows: Dict[str, List[Dict[str, object]]] = defaultdict(list)
month_work_rows: Dict[str, List[Dict[str, object]]] = defaultdict(list)
for row in financial_rows:
    month_rows[str(row["Service Date"])[:7]].append(row)
for row in work_items:
    month_work_rows[str(row["Service Date"])[:7]].append(row)

source_start = date.fromisoformat(min(str(row["Service Date"])[:10] for row in financial_rows))
source_end = date.fromisoformat(max(str(row["Service Date"])[:10] for row in financial_rows))
month_details = []
previous_month_revenue = None
for month_key in sorted(month_rows):
    rows = month_rows[month_key]
    work_rows = month_work_rows[month_key]
    revenue = round(sum(float(row["Approved Client Price"]) for row in rows), 2)
    payout = round(sum(float(row["Approved Worker Price"]) for row in rows), 2)
    cost = round(sum(float(row["Cost"]) for row in rows), 2)
    income = round(sum(float(row["Business Income"]) for row in rows), 2)
    year_value, month_value = (int(part) for part in month_key.split("-"))
    coverage = "Partial" if (year_value, month_value) in {
        (source_start.year, source_start.month),
        (source_end.year, source_end.month),
    } else "Full"
    month_details.append(
        {
            "month": month_key,
            "coverage": coverage,
            "work_items": len(work_rows),
            "client_revenue": revenue,
            "worker_payout": payout,
            "cost": cost,
            "business_income": income,
            "margin_pct": round(income / revenue * 100, 1) if revenue else 0.0,
            "average_revenue_per_work_item": round(
                sum(float(row["Approved Client Price"]) for row in work_rows) / len(work_rows), 2
            ) if work_rows else 0.0,
            "revenue_change_pct": round((revenue / previous_month_revenue - 1) * 100, 1)
            if previous_month_revenue else None,
        }
    )
    previous_month_revenue = revenue


# Rank Properties by real Work Item revenue for the Property dashboard.
property_details = []
for property_key in sorted({str(row["Property Key"]) for row in work_items}):
    rows = [row for row in work_items if row["Property Key"] == property_key]
    revenue = round(sum(float(row["Approved Client Price"]) for row in rows), 2)
    income = round(sum(float(row["Business Income"]) for row in rows), 2)
    property_details.append(
        {
            "property": f"Property {property_key.replace('PROP-', '')[:6]}",
            "client": str(rows[0]["Client"]),
            "work_items": len(rows),
            "client_revenue": revenue,
            "business_income": income,
            "margin_pct": round(income / revenue * 100, 1) if revenue else 0.0,
        }
    )
property_details.sort(key=lambda item: item["client_revenue"], reverse=True)


insights = {
    "_comment": "Plain-language facts calculated from anonymous data with real source dates and amounts.",
    "time_view": {
        "default": "Billing Period",
        "optional": "Month",
        "note": "March and August are partial months, so the dashboard defaults to the closed 14-day Billing Period.",
    },
    "overall": {
        "business_margin_pct": round(total("Business Income") / total("Approved Client Price") * 100, 1),
        "active_workers": len(worker_details),
        "average_work_items_per_worker": round(len(work_items) / len(worker_details), 1),
        "clients": len(client_map),
    },
    "latest_vs_previous_billing_period": {
        "latest_period": latest_period,
        "previous_period": previous_period,
        "latest": latest,
        "previous": previous,
        "revenue_change_pct": round((latest["revenue"] / previous["revenue"] - 1) * 100, 1),
        "business_income_change_pct": round((latest["business_income"] / previous["business_income"] - 1) * 100, 1),
        "margin_change_percentage_points": round(latest["margin_pct"] - previous["margin_pct"], 1),
        "work_item_change_pct": round((latest["work_items"] / previous["work_items"] - 1) * 100, 1),
    },
    "months": month_details,
    "workers": worker_details,
    "clients": client_details,
    "top_properties": property_details[:10],
}


# Save release metadata and show the profile in the build log.
(OUTPUT_DIR / "data_profile.json").write_text(json.dumps(profile, indent=2) + "\n", encoding="utf-8")
(OUTPUT_DIR / "business_insights.json").write_text(json.dumps(insights, indent=2) + "\n", encoding="utf-8")
print(json.dumps(profile, indent=2))
