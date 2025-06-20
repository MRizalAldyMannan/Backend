from flask import jsonify
from app.api import bp

@bp.errorhandler(404)
def not_found_error(error):
    """404 Not Found for API"""
    return jsonify({'error': 'Resource not found'}), 404

@bp.errorhandler(500)
def internal_error(error):
    """500 Internal Server Error for API"""
    return jsonify({'error': 'Internal server error'}), 500 