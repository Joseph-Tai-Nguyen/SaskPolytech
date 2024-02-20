from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World! This is your Flask API.'

@app.route('/api/data', methods=['GET'])
def get_data():
    data = {'message': 'This is your API data.'}
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
