# Tool Specifications

Write the spec BEFORE implementing a tool. The "Purpose" line becomes the tool description the LLM reads.

## Template
```
## Tool: <name>
- File: src/tools/<file>.py
- Purpose: <one clear sentence — this is what the LLM sees>
- Type: read | write | compute
- Parameters: <name> (<type>, required|optional) — <description>
- Returns: <example JSON>
- Errors: <when> → <example error JSON with a hint>
- Example request: "<a user sentence that should trigger this tool>"
```

---

## Tool: get_medications
- File: src/tools/medication_tools.py
- Purpose: Get all medications with their condition, dosage, time slots, prescription duration, price, and instructions.
- Type: read
- Parameters: time_slot (string, optional) — filter by "아침", "점심", or "저녁"; condition (string, optional) — filter by condition, e.g. "고혈압"
- Returns: `{"items": [{"name": "혈압약", "condition": "고혈압", "dose_per_time": 1, "times": ["아침", "저녁"], "instructions": "식후 30분", "duration_days": 30, "price": 150}]}`
- Errors:
  - unknown time_slot → `{"error": "Unknown time_slot '밤'. Valid: 아침, 점심, 저녁."}`
  - unknown condition → `{"error": "Unknown condition '감기'. Valid: 고혈압, 당뇨병, 고지혈증, 골관절염, 골다공증, 불면증, 전립선비대증, 치매, 파킨슨병, 변비."}`
- Example request: "저녁에 드셔야 하는 약이 뭐야?"

## Tool: add_medication
- File: src/tools/medication_tools.py
- Purpose: Add a new medication the parent is currently taking, with its condition, dosage, prescription duration, and price. Only call after the user confirms.
- Type: write
- Parameters:
  - name (string, required) — medication name, e.g. "오메가3"
  - condition (string, required) — associated condition, e.g. "고지혈증"
  - dose_per_time (integer, required) — units per dose, must be ≥ 1
  - times (array of string, required) — one or more of "아침", "점심", "저녁"
  - instructions (string, required) — e.g. "식후 30분"
  - duration_days (integer, required) — typical prescription length in days, must be ≥ 1
  - price (integer, required) — price per unit in KRW, must be ≥ 0
  - initial_stock (integer, optional, default 0) — units currently on hand
- Returns: `{"name": "오메가3", "condition": "고지혈증", "quantity": 30}`
- Errors:
  - already exists → `{"error": "Medication '혈압약' already exists. Call refill_medication to add stock, or check_medication_stock to see quantity."}`
  - unknown condition → `{"error": "Unknown condition '감기'. Valid: 고혈압, 당뇨병, 고지혈증, 골관절염, 골다공증, 불면증, 전립선비대증, 치매, 파킨슨병, 변비."}`
  - invalid times → `{"error": "times must be one or more of 아침, 점심, 저녁."}`
  - dose_per_time / duration_days < 1 → `{"error": "dose_per_time must be at least 1."}`
  - price < 0 → `{"error": "price must be 0 or more."}`
- Example request: "오메가3 새로 추가해줘. 고지혈증약이고 아침에 1정, 식후 30분, 30일치, 정당 200원, 지금 30개 있어."

## Tool: check_medication_stock
- File: src/tools/stock_tools.py
- Purpose: Check how many units of a medication are left in stock.
- Type: read
- Parameters: medication (string, required) — exact medication name, e.g. "혈압약"
- Returns: `{"medication": "혈압약", "quantity": 14}`
- Errors: medication not found → `{"error": "Medication '두통약' not found. Call get_medications to see valid medication names."}`
- Example request: "혈압약 몇 개 남았어?"

## Tool: refill_medication
- File: src/tools/stock_tools.py
- Purpose: Add units to a medication's stock after picking up a new prescription. Only call after the user confirms.
- Type: write
- Parameters: medication (string, required) — exact medication name; qty (integer, required) — units added, must be ≥ 1
- Returns: `{"medication": "혈압약", "added": 30, "quantity": 44}`
- Errors:
  - medication not found → `{"error": "Medication '두통약' not found. Call get_medications to see valid medication names."}`
  - qty < 1 → `{"error": "qty must be at least 1."}`
- Example request: "혈압약 처방받아서 30개 더 받아왔어."

## Tool: record_dose
- File: src/tools/dose_tools.py
- Purpose: Record whether a medication was taken at a given time slot today. Reduces stock by one dose if taken. Only call after the user confirms.
- Type: write
- Parameters: medication (string, required); time_slot (string, required) — "아침", "점심", or "저녁"; taken (boolean, optional, default true) — false means the dose was missed/skipped
- Returns: `{"medication": "혈압약", "time_slot": "저녁", "taken": true, "remaining_stock": 13}`
- Errors:
  - medication not found → `{"error": "Medication '두통약' not found. Call get_medications to see valid medication names."}`
  - invalid time_slot → `{"error": "Unknown time_slot '밤'. Valid: 아침, 점심, 저녁."}`
  - taken but no stock left → `{"error": "혈압약 재고가 없습니다. Call refill_medication after picking up the prescription."}`
- Example request: "오늘 저녁 혈압약 드셨어. 기록해 줘."

## Tool: get_dose_report
- File: src/tools/dose_tools.py
- Purpose: Get a summary of today's medication doses: how many were taken, how many were missed, and which ones were missed.
- Type: read
- Parameters: none
- Returns: `{"date": "2026-10-01", "taken": 2, "missed": 1, "missed_list": [{"medication": "당뇨약", "time_slot": "점심"}]}`
- Errors: no records yet → return zeros and an empty `missed_list` (not an error)
- Example request: "오늘 약 잘 챙겨 드셨어?"

## Tool: find_next_refill_date
- File: src/tools/dose_tools.py
- Purpose: Calculate the date by which the next prescription refill is needed, based on remaining stock and daily dose amount.
- Type: read
- Parameters: medication (string, required) — exact medication name
- Returns: `{"medication": "혈압약", "remaining": 14, "daily_usage": 2, "days_left": 7, "next_refill_date": "2026-10-08"}`
- Errors: medication not found → `{"error": "Medication '두통약' not found. Call get_medications to see valid medication names."}`
- Example request: "혈압약 다음 처방은 언제 받아야 해?"

> Note: return a SUMMARY, not every record. Big tool results waste context.
