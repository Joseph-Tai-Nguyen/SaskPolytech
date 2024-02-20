from flask import jsonify
from app import app

@app.route('/')
@app.route('/index')
def index():
    return "Hello from my AWS ECS Container"

@app.route('/api/data', methods=['GET'])
def get_data():
    data = {'message': 'This is your API data.'}
    return jsonify(data)