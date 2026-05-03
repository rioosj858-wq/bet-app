from flask import Flask, jsonify, render_template
import random

app = Flask(__name__)

# =========================
# PARTIDOS LIVE (SIMULADO)
# =========================
def live_matches():
    return [
        {"home":"Barcelona","away":"Madrid","hg":2,"ag":1,"type":"LIVE"},
        {"home":"Real Betis","away":"Sevilla","hg":1,"ag":1,"type":"LIVE"}
    ]

# =========================
# META BET (VIRTUAL)
# =========================
def virtual_matches():
    return [
        {"home":"MetaBet A","away":"MetaBet B","hg":random.randint(0,4),"ag":random.randint(0,4),"type":"VIRTUAL"},
        {"home":"MetaBet C","away":"MetaBet D","hg":random.randint(0,4),"ag":random.randint(0,4),"type":"VIRTUAL"}
    ]

# =========================
# PROBABILIDAD SIMPLE IA
# =========================
def probability(hg, ag):
    if hg > ag:
        return 0.62
    elif ag > hg:
        return 0.38
    return 0.50

# =========================
# VALUE BET
# =========================
def value(prob, cuota):
    v = prob - (1/cuota)
    return round(v,3) if v > 0.03 else None

# =========================
# API PANEL
# =========================
@app.route("/panel")
def panel():

    matches = live_matches() + virtual_matches()

    data = []

    for m in matches:

        p = probability(m["hg"], m["ag"])

        cuota = 1.85 if m["type"] == "LIVE" else 2.10

        v = value(p, cuota)

        data.append({
            "match": f'{m["home"]} vs {m["away"]}',
            "score": f'{m["hg"]}-{m["ag"]}',
            "type": m["type"],
            "prob": round(p*100,2),
            "cuota": cuota,
            "value": v,
            "status": "🔥 VALUE BET" if v else "⚠️ SIN VALOR"
        })

    return jsonify(data)

# =========================
# PÁGINA PRINCIPAL
# =========================
@app.route("/")
def home():
    return render_template("index.html")

# =========================
# RUN SERVER
# =========================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
