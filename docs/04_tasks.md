# Tasks

Do ONE task at a time. After each task: run tests, try the scenario, and make sure you understand the code.

Prompt for your AI assistant:
> Read AGENTS.md. Then do Task N from docs/04_tasks.md using docs/03_tool_spec.md. Only touch the files needed.

## Part 1 — Foundation (재사용 — 카페 에이전트와 동일, 수정 없음)
- [x] **1. Config & LLM client.** `src/config.py`, `src/llm_client.py` — 그대로 재사용.
- [x] **2. Data store.** `src/tools/data_store.py` — 그대로 재사용 (파일 이름만 다른 JSON을 읽고 씀).

## Part 2 — First tool & the agent loop
- [x] **3. get_medications.** `medication_tools.py`에 구현, `tools/__init__.py`에 등록. Check: `pytest -k get_medications`.
- [x] **4. Agent loop.** `src/agent.py`, `src/main.py` — 그대로 재사용.

## Part 3 — Many tools
- [x] **5. check_medication_stock + calculate.** Check: `pytest -k "medication_stock or calculate"`, Scenario A.
- [x] **6. record_dose + get_dose_report.** Check: `pytest -k "dose"`, Scenarios B, C.
- [x] **7. Make the agent visible.** `agent.py`의 도구 호출 로그 출력 — 그대로 재사용.

## Part 4 — Context engineering
- [x] **8. Robustness.** Scenario D (존재하지 않는 약 이름)로 오류 회복 확인.
- [x] **9. History trimming.** `MAX_HISTORY_MESSAGES` 트리밍 — 그대로 재사용. Check: Scenario F.
- [ ] **10. Description experiment (선택).** `check_medication_stock`의 description을 "does stuff"로 바꿔보고 Scenario A를 실행, 관찰 후 복원.

## Part 5 — Your own tool
- [x] **11. Design find_next_refill_date.** `docs/03_tool_spec.md`에 명세 작성 완료.
- [x] **12. Build it.** `refill_medication` + `find_next_refill_date` 구현, 등록, 테스트. 대표 시나리오: "오늘 저녁 약 드셨는지 기록해 줘. 다음 처방은 언제 받아야 해?"
