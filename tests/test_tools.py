"""Tool tests. No LLM needed.
Run one group:  python -m pytest tests -k get_medications
"""
from src.tools.calculator import calculate


# ---- Already done ----
def test_calculate_ok():
    assert calculate("3 * 4500 * 0.9")["result"] == 12150.0


def test_calculate_error_has_hint():
    assert "error" in calculate("import os")


# ---- Data store ----
def test_data_store_roundtrip():
    from src.tools import data_store
    data = data_store.load("stock")
    data["혈압약"] = 99
    data_store.save("stock", data)
    assert data_store.load("stock")["혈압약"] == 99


# ---- get_medications ----
def test_get_medications_all():
    from src.tools.medication_tools import get_medications
    assert len(get_medications()["items"]) == 6


def test_get_medications_time_slot():
    from src.tools.medication_tools import get_medications
    items = get_medications("점심")["items"]
    assert {i["name"] for i in items} == {"당뇨약"}


def test_get_medications_bad_time_slot():
    from src.tools.medication_tools import get_medications
    assert "error" in get_medications("밤")


def test_get_medications_condition():
    from src.tools.medication_tools import get_medications
    items = get_medications(condition="고혈압")["items"]
    assert {i["name"] for i in items} == {"혈압약"}
    assert items[0]["duration_days"] == 30 and items[0]["price"] == 150


def test_get_medications_bad_condition():
    from src.tools.medication_tools import get_medications
    assert "error" in get_medications(condition="감기")


# ---- add_medication ----
def test_add_medication_ok():
    from src.tools.medication_tools import add_medication
    r = add_medication(
        name="오메가3", condition="고지혈증", dose_per_time=1, times=["아침"],
        instructions="식후", duration_days=30, price=200, initial_stock=30,
    )
    assert r == {"name": "오메가3", "condition": "고지혈증", "quantity": 30}


def test_add_medication_already_exists():
    from src.tools.medication_tools import add_medication
    r = add_medication(
        name="혈압약", condition="고혈압", dose_per_time=1, times=["아침"],
        instructions="식후", duration_days=30, price=150,
    )
    assert "error" in r


def test_add_medication_bad_condition():
    from src.tools.medication_tools import add_medication
    r = add_medication(
        name="새약", condition="감기", dose_per_time=1, times=["아침"],
        instructions="식후", duration_days=30, price=100,
    )
    assert "error" in r


def test_add_medication_bad_times():
    from src.tools.medication_tools import add_medication
    r = add_medication(
        name="새약", condition="고혈압", dose_per_time=1, times=["밤"],
        instructions="식후", duration_days=30, price=100,
    )
    assert "error" in r


# ---- check_medication_stock ----
def test_check_medication_stock_ok():
    from src.tools.stock_tools import check_medication_stock
    assert check_medication_stock("혈압약") == {"medication": "혈압약", "quantity": 14}


def test_check_medication_stock_not_found_hint():
    from src.tools.stock_tools import check_medication_stock
    assert "get_medications" in check_medication_stock("두통약")["error"]


# ---- refill_medication ----
def test_refill_medication_ok():
    from src.tools.stock_tools import refill_medication
    assert refill_medication("관절염약", 30) == {"medication": "관절염약", "added": 30, "quantity": 30}


def test_refill_medication_not_found():
    from src.tools.stock_tools import refill_medication
    assert "get_medications" in refill_medication("두통약", 5)["error"]


def test_refill_medication_bad_qty():
    from src.tools.stock_tools import refill_medication
    assert "error" in refill_medication("혈압약", 0)


# ---- record_dose / get_dose_report ----
def test_record_dose_ok():
    from src.tools.dose_tools import record_dose
    r = record_dose("혈압약", "저녁")
    assert r == {"medication": "혈압약", "time_slot": "저녁", "taken": True, "remaining_stock": 13}


def test_record_dose_missed_does_not_reduce_stock():
    from src.tools.dose_tools import record_dose
    r = record_dose("혈압약", "저녁", taken=False)
    assert r["taken"] is False and r["remaining_stock"] == 14


def test_record_dose_not_found():
    from src.tools.dose_tools import record_dose
    assert "get_medications" in record_dose("두통약", "아침")["error"]


def test_record_dose_bad_time_slot():
    from src.tools.dose_tools import record_dose
    assert "error" in record_dose("혈압약", "밤")


def test_record_dose_no_stock():
    from src.tools.dose_tools import record_dose
    assert "error" in record_dose("관절염약", "아침")


def test_dose_report_summary():
    from src.tools.dose_tools import record_dose, get_dose_report
    record_dose("혈압약", "아침")
    record_dose("당뇨약", "점심", taken=False)
    r = get_dose_report()
    assert r["taken"] == 1 and r["missed"] == 1
    assert r["missed_list"] == [{"medication": "당뇨약", "time_slot": "점심"}]


def test_dose_report_empty():
    from src.tools.dose_tools import get_dose_report
    r = get_dose_report()
    assert r["taken"] == 0 and r["missed"] == 0 and r["missed_list"] == []


# ---- find_next_refill_date (my tool) ----
def test_find_next_refill_date_ok():
    from src.tools.dose_tools import find_next_refill_date
    r = find_next_refill_date("혈압약")
    assert r["daily_usage"] == 2 and r["days_left"] == 7


def test_find_next_refill_date_zero_stock():
    from src.tools.dose_tools import find_next_refill_date
    r = find_next_refill_date("관절염약")
    assert r["days_left"] == 0


def test_find_next_refill_date_not_found():
    from src.tools.dose_tools import find_next_refill_date
    assert "get_medications" in find_next_refill_date("두통약")["error"]


# ---- Registry check ----
def test_registry_consistent():
    from src.tools import TOOL_FUNCTIONS, TOOL_SCHEMAS
    names = {s["function"]["name"] for s in TOOL_SCHEMAS}
    assert names == set(TOOL_FUNCTIONS)
    assert len(names) >= 7
