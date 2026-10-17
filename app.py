from flask import Flask, jsonify, request, render_template

from flask_cors import CORS
app = Flask(__name__)
CORS(app)

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")


@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy", "service": "SecurePulse API"})

@app.route("/api/predict", methods=["POST"])
def predict():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"error": "Send a valid JSON object"}), 400

    try:
        heart_rate = float(data["heart_rate"])
        temperature = float(data["temperature"])
    except (KeyError, TypeError, ValueError):
        return jsonify({"error": "Provide numeric heart_rate and temperature"}), 400

    if not 20 <= heart_rate <= 250:
        return jsonify({"error": "Heart rate is outside the demo input range"}), 400
    if not 30 <= temperature <= 45:
        return jsonify({"error": "Temperature is outside the demo input range"}), 400

    # Illustrative demo rules only; this is NOT a trained medical model.
    if heart_rate >= 120 or temperature >= 39:
        risk_level = "High"
    elif heart_rate >= 100 or temperature >= 38:
        risk_level = "Medium"
    else:
        risk_level = "Low"

    return jsonify({
        "demo_only": True,
        "heart_rate": heart_rate,
        "temperature": temperature,
        "risk_level": risk_level,
        "message": "Illustrative result only. Not a medical diagnosis."
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)

