from flask import Flask, request, jsonify, send_from_directory
from pathlib import Path
try:
    from backend import util  # run from repo root
except Exception:
    import util  # run from backend/ directly

app = Flask(__name__)
frontend_dir = (Path(__file__).resolve().parents[1] / "frontend").resolve()


@app.route("/", methods=["GET"])
def index():
    return send_from_directory(frontend_dir, "index.html")


@app.route("/<path:filename>", methods=["GET"])
def frontend_static(filename: str):
    return send_from_directory(frontend_dir, filename)

@app.route('/get_location_names', methods=['GET'])
def get_location_names():
    response = jsonify({
        'locations': util.get_location_names()
    })
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response

@app.route('/predict_home_price', methods=['GET', 'POST'])
def predict_home_price():
    total_sqft = float(request.form['total_sqft'])
    location = request.form['location']
    bhk = int(request.form['bhk'])
    bath = int(request.form['bath'])

    response = jsonify({
        'estimated_price': util.get_estimated_price(location,total_sqft,bhk,bath)
    })
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response

if __name__ == "__main__":
    print("Starting Python Flask Server For Home Price Prediction...")
    util.load_saved_artifacts()
    app.run()