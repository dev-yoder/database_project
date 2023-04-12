import json
from flask import Flask, render_template, jsonify

from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/area_breakdown')
def area_breakdown():
    return render_template('area_breakdown.html')

if __name__ == '__main__':
    app.run(debug=True)

    @app.route("/area-data")
def area_data():
    with open("sample_data.json", "r") as f:
        data = json.load(f)
    return jsonify(data)

