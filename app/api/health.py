from flask import jsonify
from app.api import bp
from app import db

@bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    try:
        # Test database connection
        db.session.execute('SELECT 1')
        db_status = 'healthy'
    except Exception:
        db_status = 'unhealthy'
    
    return jsonify({
        'status': 'ok',
        'database': db_status,
        'timestamp': '2024-01-01T00:00:00Z'  # You can use datetime.utcnow().isoformat()
    }) 