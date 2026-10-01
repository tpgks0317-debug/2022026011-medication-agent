"""Medication reference tools."""
from src.tools.data_store import load

VALID_TIME_SLOTS = {"아침", "점심", "저녁"}


def get_medications(time_slot: str | None = None) -> dict:
    """Get all medications with dosage, time slots, and instructions, optionally filtered by time slot."""
    if time_slot is not None and time_slot not in VALID_TIME_SLOTS:
        return {"error": f"Unknown time_slot '{time_slot}'. Valid: 아침, 점심, 저녁."}

    medications = load("medications")
    items = [
        {"name": name, "dose_per_time": info["dose_per_time"], "times": info["times"], "instructions": info["instructions"]}
        for name, info in medications.items()
        if time_slot is None or time_slot in info["times"]
    ]
    return {"items": items}


GET_MEDICATIONS_SCHEMA = {
    "type": "function",
    "function": {
        "name": "get_medications",
        "description": "Get all medications with dosage, time slots, and instructions.",
        "parameters": {
            "type": "object",
            "properties": {
                "time_slot": {
                    "type": "string",
                    "description": "Filter by '아침', '점심', or '저녁'.",
                }
            },
            "required": [],
        },
    },
}
