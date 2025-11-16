"""
Webhook server for payment callbacks
"""
from flask import Flask, request, jsonify
from payment_callback import webhook_payment_callback
from config import PANEL_PORT, PANEL_SECRET_KEY
import logging

app = Flask(__name__)
app.secret_key = PANEL_SECRET_KEY

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.route('/payment/callback', methods=['POST', 'GET'])
def payment_callback():
    """Handle payment callback from Zarinpal"""
    try:
        if request.method == 'GET':
            # Zarinpal sends callback as GET with query parameters
            data = request.args.to_dict()
        else:
            data = request.get_json() or {}
        
        logger.info(f"Payment callback received: {data}")
        
        # Process callback
        # Note: We need bot context here, so this might need to be adjusted
        # For now, we'll just log and return success
        result = {'success': True, 'message': 'Callback received'}
        
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error processing payment callback: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'ok'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PANEL_PORT, debug=False)

