"""Dose log tools."""
from datetime import date, timedelta

from src.tools.data_store import load, save
from src.tools.medication_tools import VALID_TIME_SLOTS


def record_dose(medication: str, time_slot: str, taken: bool = True) -> dict:
    """Record whether a medication was taken at a given time slot today; reduces stock if taken."""
    medications = load("medications")
    if medication not in medications:
        return {"error": f"Medication '{medication}' not found. Call get_medications to see valid medication names."}

    if time_slot not in VALID_TIME_SLOTS:
        return {"error": f"Unknown time_slot '{time_slot}'. Valid: 아침, 점심, 저녁."}

    stock = load("stock")
    if taken:
        current = stock.get(medication, 0)
        if current < 1:
            return {"error": f"{medication} 재고가 없습니다. Call refill_medication after picking up the prescription."}
        stock[medication] = current - 1
        save("stock", stock)

    doses = load("doses")
    doses["date"] = str(date.today())
    doses.setdefault("records", []).append({"medication": medication, "time_slot": time_slot, "taken": taken})
    save("doses", doses)

    return {"medication": medication, "time_slot": time_slot, "taken": taken, "remaining_stock": stock[medication]}


def get_dose_report() -> dict:
    """Return a SHORT summary of today's doses (not every record)."""
    doses = load("doses")
    records = doses.get("records", [])

    taken = sum(1 for r in records if r["taken"])
    missed_list = [{"medication": r["medication"], "time_slot": r["time_slot"]} for r in records if not r["taken"]]

    return {
        "date": str(date.today()),
        "taken": taken,
        "missed": len(missed_list),
        "missed_list": missed_list,
    }


def find_next_refill_date(medication: str) -> dict:
    """Calculate the date by which the next prescription refill is needed."""
    medications = load("medications")
    if medication not in medications:
        return {"error": f"Medication '{medication}' not found. Call get_medications to see valid medication names."}

    stock = load("stock")
    remaining = stock.get(medication, 0)
    info = medications[medication]
    daily_usage = info["dose_per_time"] * len(info["times"])

    days_left = remaining // daily_usage
    next_refill_date = date.today() + timedelta(days=days_left)

    return {
        "medication": medication,
        "remaining": remaining,
        "daily_usage": daily_usage,
        "days_left": days_left,
        "next_refill_date": str(next_refill_date),
    }


RECORD_DOSE_SCHEMA = {
    "type": "function",
    "function": {
        "name": "record_dose",
        "description": (
            "Record whether a medication was taken at a given time slot today. "
            "Reduces stock by one dose if taken. Only call after the user confirms."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "medication": {"type": "string", "description": "Exact medication name, e.g. '혈압약'"},
                "time_slot": {"type": "string", "description": "'아침', '점심', or '저녁'"},
                "taken": {"type": "boolean", "description": "False means the dose was missed/skipped. Defaults to true."},
            },
            "required": ["medication", "time_slot"],
        },
    },
}

GET_DOSE_REPORT_SCHEMA = {
    "type": "function",
    "function": {
        "name": "get_dose_report",
        "description": "Get a summary of today's medication doses: how many were taken, how many were missed, and which ones were missed.",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": [],
        },
    },
}

FIND_NEXT_REFILL_DATE_SCHEMA = {
    "type": "function",
    "function": {
        "name": "find_next_refill_date",
        "description": "Calculate the date by which the next prescription refill is needed, based on remaining stock and daily dose amount.",
        "parameters": {
            "type": "object",
            "properties": {
                "medication": {"type": "string", "description": "Exact medication name, e.g. '혈압약'"}
            },
            "required": ["medication"],
        },
    },
}
