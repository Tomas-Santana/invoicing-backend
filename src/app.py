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

@app.route('/createClient', methods=['POST'])
def create_client():
    data = request.get_json()

    name = data.get('name', None)
    surname = data.get('surname', None)
    dir = data.get('dir', None)
    pid = data.get('pid', None)
    pid_prefix = data.get('pid_prefix', None)

    logging.debug(data)
    if name is None or surname is None or dir is None or pid is None or pid_prefix is None:
        response = jsonify({'message': 'Invalid request'})
        response.status_code = 400
        return response

    try:
        result = db.create_client(name, surname, dir, pid, pid_prefix)
    except Exception as e:
        logging.error(e)
        response = jsonify({'message': 'Invalid request', 'result': []})
        response.status_code = 400
        return response

    return jsonify({'result': result})

@app.route('/createInvoice', methods=['POST'])
def create_invoice():
    invoice = request.get_json()
    
    prettyData = json.dumps(invoice, indent=4)
    logging.debug(prettyData)
    
    if invoice is None:
        response = jsonify({'message': 'Invalid request'})
        response.status_code = 400
        return response
    
    # validate that invoice has all required fields (client, products, payments)
    
    if 'client' not in invoice or 'products' not in invoice or 'payments' not in invoice:
        logging.debug('missing fields')
        response = jsonify({'message': 'Invalid request'})
        response.status_code = 400
        return response
    
    # validate that client has all required fields (name, surname, dir, pid, pid_prefix)
    
    if 'name' not in invoice['client'] or 'surname' not in invoice['client'] or 'dir' not in invoice['client'] or 'pid' not in invoice['client'] or 'pid_prefix' not in invoice['client']:
        logging.debug('missing client fields')
        response = jsonify({'message': 'Invalid request'})
        response.status_code = 400
        return response
    
    # validate that products has all required fields (name, code, quantity)
    
    for product in invoice['products']:
        if 'name' not in product or 'code' not in product or 'quantity' not in product:
            logging.debug('missing product fields')
            response = jsonify({'message': 'Invalid request'})
            response.status_code = 400
            return response
    
    # validate that payments has all required fields (method, amount)
    
    for payment in invoice['payments']:
        if 'method' not in payment or 'amount' not in payment:
            logging.debug('missing payment fields')
            response = jsonify({'message': 'Invalid request'})
            response.status_code = 400
            return response
    
    try:
        result = db.create_invoice(invoice)
    except Exception as e:
        logging.error("Error creating", e)
        response = jsonify({'message': 'Invalid request', 'result': []})
        response.status_code = 400
        return response
    
    return jsonify({'result': result})

@app.route('/getInvoice', methods=['POST', 'GET'])
def get_invoice():
    if request.method == 'GET':
        response = jsonify({'result': db.get_invoice(100)})
        return response
    
    data = request.get_json()
    invoice_id = int(data.get('invoice_id', None))
    
    if invoice_id is None:
        response = jsonify({'message': 'Invalid request'})
        response.status_code = 400
        return response
    
    try:
        result = db.get_invoice(invoice_id)
    except Exception as e:
        logging.error(e)
        response = jsonify({'message': 'Invalid request', 'result': []})
        response.status_code = 400
        return response
    
    return jsonify({'result': result})


@app.route('/searchInvoice', methods=['POST', 'GET'])
def search_invoice():
    if request.method == 'GET':
        response = jsonify({'result': db.search_invoice('name', 'Tomas')})
        return response
    
    data = request.get_json()
    field = data.get('field', None)
    value = data.get('value', None)
    
    valid_fields = ["name", "pid", "invoice_id", "date"]
    
    if field is None or value is None or field not in valid_fields:
        response = jsonify({'message': 'Invalid request'})
        response.status_code = 400
        return response
    
    try:
        result = db.search_invoice(field, value)
    except Exception as e:
        logging.error(e)
        response = jsonify({'message': 'Invalid request', 'result': []})
        response.status_code = 400
        return response
    
    return jsonify({'result': result})

@app.route('/getClosingStatement', methods=['POST', 'GET'])
def get_closing_statement():
    if request.method == 'GET':
        response = jsonify({'result': db.get_closing_statement('2024-04-09')})
        return response
    
    date = request.get_json().get('date', None)
    
    if date is None:
        logging.debug('missing date')
        response = jsonify({'message': 'Invalid request'})
        response.status_code = 400
        return response
    
    try:
        result = db.get_closing_statement(date)
    except Exception as e:
        logging.error("other Error", e)
        response = jsonify({'message': 'Invalid request', 'result': []})
        response.status_code = 400
        return response
    
    return jsonify({'result': result})
    
    
        

if __name__ == '__main__':
    app.run(debug=True)