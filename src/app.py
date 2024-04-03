from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import logging
logging.basicConfig(level=logging.DEBUG)


app = Flask(__name__)
CORS(app)


@app.route('/hello', methods=['GET'])
def hello():
    response = jsonify({'message': 'Hello World!'})
    return response

@app.route('/search', methods=['POST'])
def search():

    data = request.get_json()

    table = data.get('table', None)
    field = data.get('field', None)
    value:str = data.get('value', None)

    if field is None or value is None or table is None:
        response = jsonify({'message': 'Invalid request'})
        
        response.status_code = 400
        return response
    
    with open('data/data.json') as json_file:
        db_data = json.load(json_file)
    
    result = []
    for item in db_data[table]:
        if str(item[field]).lower().startswith(value.lower()):
            result.append(item)    
    
    response = jsonify({'result': result})
    return response







    


if __name__ == '__main__':
    app.run(debug=True)