from flask import Flask, render_template
import json

app = Flask(__name__, static_url_path='/static')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/area_breakdown')
def area_breakdown_page():  # <-- change this line
    return render_template('area_breakdown.html')

if __name__ == '__main__':
    app.run(debug=True)
