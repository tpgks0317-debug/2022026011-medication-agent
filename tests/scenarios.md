# Test Scenarios

Run `python -m src.main` and type each prompt. Compare the tool calls with the expected ones.
The exact order may vary slightly; what matters is that the agent uses tools instead of guessing.

| # | Prompt | Expected tool calls | What to check |
|---|---|---|---|
| A | 혈압약 몇 개 남았고, 다음 처방은 언제 받아야 해? | `check_medication_stock` → `find_next_refill_date` | 14개 남음, 하루 2번 복용 → 7일 뒤 날짜 |
| B | 오늘 저녁 혈압약 드셨어. 기록해 줘. | (확인 요청) → `record_dose` | "예" 확인 뒤에만 기록되고 재고가 1 줄어듦 |
| C | 오늘 약 잘 챙겨 드셨어? | `get_dose_report` | 오늘 기록된 복용/누락 개수 요약 |
| D | 두통약 몇 개 남았어? (존재하지 않는 약) | `check_medication_stock` → error → `get_medications` | 회복하고 두통약은 목록에 없다고 설명 |
| E | 관절염약 처방받아서 30개 받아왔어. 지금 몇 개야? | (확인 요청) → `refill_medication` | 확인 후 재고 0 → 30으로 갱신 |
| F | 대화를 15턴 이상 나눈 뒤 "내가 처음에 뭐라고 물었지?" | — | 죽지 않음. 트리밍 후 에이전트가 처음 질문을 잊는지 관찰 |
| G | 고지혈증 때문에 오메가3 새로 먹기 시작했어. 아침에 1정, 식후, 30일치, 정당 200원, 지금 30개 있어. 추가해 줘. | (확인 요청) → `add_medication` | 확인 후 새 약이 목록에 추가되고 재고 30으로 생성 |
| H | 고혈압 관련 약만 보여줘. 가격도 알려줘. | `get_medications(condition="고혈압")` | 혈압약만 나오고 price=150, duration_days=30 포함 |

> E 테스트 후 데이터 초기화: `data/stock.json`의 `관절염약`을 0으로, `data/doses.json`의 `records`를 `[]`로 되돌린다.
> G 테스트 후 데이터 초기화: `data/medications.json`과 `data/stock.json`에서 `오메가3` 항목을 삭제한다.

## My scenario (대표 질문)
| Prompt | Expected tool calls | What to check |
|---|---|---|
| 오늘 저녁 약 드셨는지 기록해 줘. 다음 처방은 언제 받아야 해? | (어떤 약인지 되묻거나 확인) → `record_dose` → `find_next_refill_date` | 기록 전 확인, 기록 후 남은 재고 기준으로 다음 처방일 계산 |
