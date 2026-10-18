from flask import Flask, request, jsonify
from flask_cors import CORS
import logging

from modules.risk_prediction import load_risk_model, predict_risk
from modules.anomaly_detection import load_anomaly_model, detect_anomaly

app = Flask(__name__)
CORS(app)

logging.basicConfig(level=logging.INFO)

risk_model = None
anomaly_model = None


def load_models():
    global risk_model, anomaly_model

    if risk_model is None:
        risk_model = load_risk_model()

    if anomaly_model is None:
        anomaly_model = load_anomaly_model()


@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({
        "status": "healthy",
        "service": "SecurePulse ML API"
    })


@app.route("/api/predict", methods=["POST"])
def predict():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "message": "Send patient data as JSON."
        }), 400

    required_fields = [
        "age",
        "systolic_bp",
        "diastolic_bp",
        "cholesterol",
        "glucose",
        "bmi",
        "smoking",
        "family_history"
    ]

    missing = [
        field for field in required_fields
        if field not in data
    ]

    if missing:
        return jsonify({
            "message": "Missing required fields.",
            "missing_fields": missing
        }), 400

    try:
        load_models()

        patient = {
            "age": float(data["age"]),
            "systolic_bp": float(data["systolic_bp"]),
            "diastolic_bp": float(data["diastolic_bp"]),
            "cholesterol": float(data["cholesterol"]),
            "glucose": float(data["glucose"]),
            "bmi": float(data["bmi"]),
            "smoking": int(data["smoking"]),
            "family_history": int(data["family_history"])
        }

        risk_result = predict_risk(patient, model=risk_model)
        anomaly_result = detect_anomaly(patient, model=anomaly_model)

        if not isinstance(risk_result, dict):
            risk_result = {"prediction": risk_result}

        if not isinstance(anomaly_result, dict):
            anomaly_result = {"is_anomaly": bool(anomaly_result)}

        return jsonify({
            "risk_band": risk_result.get(
                "risk_band",
                risk_result.get("risk_level", "Unknown")
            ),
            "risk_probability": risk_result.get(
                "risk_probability",
                risk_result.get("probability")
            ),
            "is_anomaly": anomaly_result.get("is_anomaly", False),
            "anomaly_score": anomaly_result.get("anomaly_score"),
            "message": "Demo prediction completed. Not a medical diagnosis."
        })

    except (ValueError, TypeError) as error:
        return jsonify({"message": str(error)}), 400

    except Exception:
        app.logger.exception("Prediction failed")
        return jsonify({
            "message": "Prediction failed. Check the backend terminal for details."
        }), 500


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8001, debug=False, use_reloader=False)