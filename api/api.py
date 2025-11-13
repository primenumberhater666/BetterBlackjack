
from engine import * 
from flask import Flask, request, jsonify
from calculations import *

app = Flask(__name__)

@app.post("/sim")
def simulate():
    d = request.get_json(force=True) or {}
    result = run(
        num_sims=int(d.get("num_sims", 100)),
        starting_bankroll=int(d.get("starting_bankroll", 250000)),
        decks_used=int(d.get("decks_used", 2)),
        penetration_cards=int(d.get("penetration_cards", 26)),
        spread=d.get("spread", []),
        players=int(d.get("players", 1)),
        two_hands_tc=int(d.get("two_hands_tc", 999)),
        rounds_per_hour=int(d.get("rounds_per_hour", 100)),
    )
    return jsonify(result), 200


if __name__ == "__main__":
    app.run(debug=True)

@app.get("/health")
def health():
    return "ok", 200