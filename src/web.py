"""Web chat UI for the café agent (Flask). Run with `py -m src.web`."""
import os
import uuid

from flask import Flask, jsonify, render_template, request, session

from src.agent import CafeAgent

app = Flask(__name__)
app.secret_key = os.urandom(24)

_agents: dict[str, CafeAgent] = {}  # session_id -> CafeAgent (server-side, in-memory)


def _get_agent() -> CafeAgent:
    if "session_id" not in session:
        session["session_id"] = str(uuid.uuid4())
    session_id = session["session_id"]
    if session_id not in _agents:
        _agents[session_id] = CafeAgent()
    return _agents[session_id]


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/chat", methods=["POST"])
def api_chat():
    message = (request.get_json(silent=True) or {}).get("message", "").strip()
    if not message:
        return jsonify({"error": "message is required"}), 400

    tool_calls = []

    def on_tool_call(name, arguments_json, result):
        tool_calls.append({"name": name, "arguments": arguments_json, "result": result})

    agent = _get_agent()
    agent.on_tool_call = on_tool_call
    reply = agent.run(message)

    return jsonify({"reply": reply, "tool_calls": tool_calls})


@app.route("/api/reset", methods=["POST"])
def api_reset():
    session_id = session.get("session_id")
    if session_id in _agents:
        del _agents[session_id]
    return jsonify({"ok": True})


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
