# 💊 Parent Medication Manager Agent

An AI assistant for an adult child (caregiver) who tracks a parent's medication —
it uses **tools** (medication list, stock, dose log, calculator, refill-date calculator)
to answer questions and take actions on local JSON data.

Example: "오늘 저녁 약 드셨는지 기록해 줘. 다음 처방은 언제 받아야 해?"

## Setup
```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env             # then put your API key in .env
```

## Run
```bash
python -m src.main               # chat with the agent (CLI)
python -m src.web                # chat with the agent (web UI, http://127.0.0.1:5000)
python -m pytest tests           # test tools (no LLM needed)
```

> **Windows note:** `agent.py` logs each tool call with an emoji (🔧). If your console
> codepage isn't UTF-8 (default on Korean Windows: cp949), `python -m src.web` crashes
> with `UnicodeEncodeError` on the first tool call. Fix by setting UTF-8 I/O before
> running: `set PYTHONUTF8=1` (cmd) or `$env:PYTHONUTF8=1` (PowerShell).

## How to work on this project (vibe coding)
1. Open `docs/04_tasks.md` and pick the next unchecked task.
2. Ask your AI coding assistant:
   > Read AGENTS.md. Then do Task N from docs/04_tasks.md using docs/03_tool_spec.md. Only touch the files needed.
3. Verify: run the tests and try the matching prompt in `tests/scenarios.md`.
4. Understand the code before moving on. You will be asked to explain it.

## Where is the "context"?
| For the coding assistant | For the agent (runtime) |
|---|---|
| `AGENTS.md`, `docs/` | `prompts/system_prompt.md`, tool descriptions, tool results, message history |

## Tools
| Tool | Type | What it does |
|---|---|---|
| `get_medications` | read | List medications with dosage, time slots, instructions |
| `check_medication_stock` | read | How many units of a medication are left |
| `record_dose` | write | Record whether a dose was taken/missed today (confirm first) |
| `get_dose_report` | read | Today's dose summary: taken, missed, missed list |
| `refill_medication` | write | Add stock after picking up a new prescription (confirm first) |
| `find_next_refill_date` | read | Days left and date the next prescription refill is needed |
| `calculate` | compute | Arithmetic for dosages/totals |

Built from the café-agent skeleton (same `config.py` / `llm_client.py` / `agent.py` / `main.py` / `data_store.py`), with the domain swapped for a medication caregiver use case.
