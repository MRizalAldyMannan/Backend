from flask import jsonify
from werkzeug.http import HTTP_STATUS_CODES
from app.errors import bp

def error_response(status_code, message=None):
    """Generate error response"""
    payload = {'error': HTTP_STATUS_CODES.get(status_code, 'Unknown error')}
    if message:
        payload['message'] = message
    response = jsonify(payload)
    response.status_code = status_code
    return response

def bad_request(message):
    """400 Bad Request"""
    return error_response(400, message)

@bp.app_errorhandler(404)
def not_found_error(error):
    """404 Not Found"""
    return error_response(404, 'Resource not found')

@bp.app_errorhandler(500)
def internal_error(error):
    """500 Internal Server Error"""
    return error_response(500, 'Internal server error')

@bp.app_errorhandler(400)
def bad_request_error(error):
    """400 Bad Request"""
    return error_response(400, 'Bad request')

@bp.app_errorhandler(405)
def method_not_allowed_error(error):
    """405 Method Not Allowed"""
    return error_response(405, 'Method not allowed') 