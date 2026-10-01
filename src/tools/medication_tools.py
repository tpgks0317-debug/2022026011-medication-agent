"""Medication reference tools."""
from src.tools.data_store import load, save

VALID_TIME_SLOTS = {"아침", "점심", "저녁"}
VALID_CONDITIONS = {
    "고혈압", "당뇨병", "고지혈증", "골관절염", "골다공증",
    "불면증", "전립선비대증", "치매", "파킨슨병", "변비",
}


def get_medications(time_slot: str | None = None, condition: str | None = None) -> dict:
    """Get all medications with condition, dosage, time slots, duration, price, and instructions."""
    if time_slot is not None and time_slot not in VALID_TIME_SLOTS:
        return {"error": f"Unknown time_slot '{time_slot}'. Valid: {', '.join(sorted(VALID_TIME_SLOTS))}."}
    if condition is not None and condition not in VALID_CONDITIONS:
        return {"error": f"Unknown condition '{condition}'. Valid: {', '.join(sorted(VALID_CONDITIONS))}."}

    medications = load("medications")
    items = [
        {
            "name": name,
            "condition": info["condition"],
            "dose_per_time": info["dose_per_time"],
            "times": info["times"],
            "instructions": info["instructions"],
            "duration_days": info["duration_days"],
            "price": info["price"],
        }
        for name, info in medications.items()
        if (time_slot is None or time_slot in info["times"])
        and (condition is None or info["condition"] == condition)
    ]
    return {"items": items}


GET_MEDICATIONS_SCHEMA = {
    "type": "function",
    "function": {
        "name": "get_medications",
        "description": "Get all medications with their condition, dosage, time slots, prescription duration, price, and instructions.",
        "parameters": {
            "type": "object",
            "properties": {
                "time_slot": {
                    "type": "string",
                    "description": "Filter by '아침', '점심', or '저녁'.",
                },
                "condition": {
                    "type": "string",
                    "description": "Filter by condition, e.g. '고혈압'.",
                },
            },
            "required": [],
        },
    },
}


def add_medication(
    name: str,
    condition: str,
    dose_per_time: int,
    times: list,
    instructions: str,
    duration_days: int,
    price: int,
    initial_stock: int = 0,
) -> dict:
    """Add a new medication the parent is currently taking."""
    medications = load("medications")
    if name in medications:
        return {"error": f"Medication '{name}' already exists. Call refill_medication to add stock, or check_medication_stock to see quantity."}

    if condition not in VALID_CONDITIONS:
        return {"error": f"Unknown condition '{condition}'. Valid: {', '.join(sorted(VALID_CONDITIONS))}."}
    if not times or any(t not in VALID_TIME_SLOTS for t in times):
        return {"error": f"times must be one or more of {', '.join(sorted(VALID_TIME_SLOTS))}."}
    if dose_per_time < 1:
        return {"error": "dose_per_time must be at least 1."}
    if duration_days < 1:
        return {"error": "duration_days must be at least 1."}
    if price < 0:
        return {"error": "price must be 0 or more."}
    if initial_stock < 0:
        return {"error": "initial_stock must be 0 or more."}

    medications[name] = {
        "condition": condition,
        "dose_per_time": dose_per_time,
        "times": times,
        "instructions": instructions,
        "duration_days": duration_days,
        "price": price,
    }
    save("medications", medications)

    stock = load("stock")
    stock[name] = initial_stock
    save("stock", stock)

    return {"name": name, "condition": condition, "quantity": initial_stock}


ADD_MEDICATION_SCHEMA = {
    "type": "function",
    "function": {
        "name": "add_medication",
        "description": "Add a new medication the parent is currently taking, with its condition, dosage, prescription duration, and price. Only call after the user confirms.",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {"type": "string", "description": "Medication name, e.g. '오메가3'"},
                "condition": {"type": "string", "description": "Associated condition, e.g. '고지혈증'"},
                "dose_per_time": {"type": "integer", "description": "Units per dose, must be >= 1"},
                "times": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "One or more of '아침', '점심', '저녁'",
                },
                "instructions": {"type": "string", "description": "e.g. '식후 30분'"},
                "duration_days": {"type": "integer", "description": "Typical prescription length in days, must be >= 1"},
                "price": {"type": "integer", "description": "Price per unit in KRW, must be >= 0"},
                "initial_stock": {"type": "integer", "description": "Units currently on hand. Defaults to 0."},
            },
            "required": ["name", "condition", "dose_per_time", "times", "instructions", "duration_days", "price"],
        },
    },
}
