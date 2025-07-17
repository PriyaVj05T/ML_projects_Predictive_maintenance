from pipeline.training_pipeline import run_training
from flask import Flask, request, jsonify
import pandas as pd
from pipeline.prediction_pipeline import run_prediction

app = Flask(__name__)

@app.route("/train", methods=["POST"])
def train():
    run_training()
    return jsonify({"message": "Training completed successfully."})

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        df = pd.DataFrame(data)
        failure_flags, failure_types = run_prediction(df)
        return jsonify({
            "failure_flags": failure_flags.tolist(),
            "failure_types": failure_types
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True)

