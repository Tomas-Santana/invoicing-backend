from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import logging
logging.basicConfig(level=logging.DEBUG)
import database.functions as db

app = Flask(__name__)
CORS(app)


@app.route('/hello', methods=['GET'])
def hello():
    result = db.search_product('te')
    return jsonify({'result': "Hello World"})


@app.route('/search', methods=['POST'])
def search():

    data = request.get_json()

    table = data.get('table', None)
    field = data.get('field', None)
    value:str = str(data.get('value', None))

    if field is None or value is None or table is None:
        response = jsonify({'message': 'Invalid request'})
        
        response.status_code = 400
        return response
    try: 
        result = db.general_search(table, field, value)
    except Exception as e:
        logging.error(e)
        response = jsonify({'message': 'Invalid request', 'result': []})
        response.status_code = 400
        return response
    

    
    return jsonify({'result': result})


if __name__ == '__main__':
    app.run(debug=True)