"""Medication stock tools."""
from src.tools.data_store import load, save


def check_medication_stock(medication: str) -> dict:
    """Check how many units of a medication are left in stock."""
    stock = load("stock")
    if medication not in stock:
        return {"error": f"Medication '{medication}' not found. Call get_medications to see valid medication names."}
    return {"medication": medication, "quantity": stock[medication]}


CHECK_MEDICATION_STOCK_SCHEMA = {
    "type": "function",
    "function": {
        "name": "check_medication_stock",
        "description": "Check how many units of a medication are left in stock.",
        "parameters": {
            "type": "object",
            "properties": {
                "medication": {"type": "string", "description": "Exact medication name, e.g. '혈압약'"}
            },
            "required": ["medication"],
        },
    },
}


def refill_medication(medication: str, qty: int) -> dict:
    """Add units to a medication's stock after picking up a new prescription."""
    if qty < 1:
        return {"error": "qty must be at least 1."}

    stock = load("stock")
    if medication not in stock:
        return {"error": f"Medication '{medication}' not found. Call get_medications to see valid medication names."}

    stock[medication] += qty
    save("stock", stock)
    return {"medication": medication, "added": qty, "quantity": stock[medication]}


REFILL_MEDICATION_SCHEMA = {
    "type": "function",
    "function": {
        "name": "refill_medication",
        "description": "Add units to a medication's stock after picking up a new prescription. Only call after the user confirms.",
        "parameters": {
            "type": "object",
            "properties": {
                "medication": {"type": "string", "description": "Exact medication name, e.g. '혈압약'"},
                "qty": {"type": "integer", "description": "Units added, must be >= 1"},
            },
            "required": ["medication", "qty"],
        },
    },
}
