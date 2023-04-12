from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/area_breakdown')
def area_breakdown():
    return render_template('area_breakdown.html')

@app.route('/area_data', methods=['GET'])
def area_data():
    with open('sample_data.json', 'r') as file:
        data = json.load(file)
    return jsonify(data)

@app.route('/area_breakdown')
def area_breakdown():
    return render_template('area_breakdown.html')


if __name__ == '__main__':
    app.run(debug=True)
