"""Tool registry: the single place where tools are connected to the agent.

TOOL_SCHEMAS   -> sent to the LLM (what the model can SEE)
TOOL_FUNCTIONS -> used by agent.py (what actually RUNS)

When you add a tool: import its function and schema, then add both below.
"""
from src.tools.calculator import CALCULATE_SCHEMA, calculate
from src.tools.dose_tools import (
    FIND_NEXT_REFILL_DATE_SCHEMA,
    GET_DOSE_REPORT_SCHEMA,
    RECORD_DOSE_SCHEMA,
    find_next_refill_date,
    get_dose_report,
    record_dose,
)
from src.tools.medication_tools import (
    ADD_MEDICATION_SCHEMA,
    GET_MEDICATIONS_SCHEMA,
    add_medication,
    get_medications,
)
from src.tools.stock_tools import (
    CHECK_MEDICATION_STOCK_SCHEMA,
    REFILL_MEDICATION_SCHEMA,
    check_medication_stock,
    refill_medication,
)

TOOL_SCHEMAS = [
    CALCULATE_SCHEMA,
    GET_MEDICATIONS_SCHEMA,
    ADD_MEDICATION_SCHEMA,
    CHECK_MEDICATION_STOCK_SCHEMA,
    RECORD_DOSE_SCHEMA,
    GET_DOSE_REPORT_SCHEMA,
    REFILL_MEDICATION_SCHEMA,
    FIND_NEXT_REFILL_DATE_SCHEMA,
]

TOOL_FUNCTIONS = {
    "calculate": calculate,
    "get_medications": get_medications,
    "add_medication": add_medication,
    "check_medication_stock": check_medication_stock,
    "record_dose": record_dose,
    "get_dose_report": get_dose_report,
    "refill_medication": refill_medication,
    "find_next_refill_date": find_next_refill_date,
}
