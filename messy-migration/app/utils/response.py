from flask import jsonify
from typing import Union, Dict, List

def success_response(data: Union[Dict, List] = None, message: str = None, status_code: int = 200):
    response = {
        'status': 'success',
        'message': message,
        'data': data
    }
    return jsonify(response), status_code

def error_response(message: str, status_code: int = 400):
    response = {
        'status': 'error',
        'message': message
    }
    return jsonify(response), status_code
