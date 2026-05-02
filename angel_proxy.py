from flask import Flask, request, jsonify
from flask_cors import CORS
from SmartApi import SmartConnect
import pyotp, os

app = Flask(__name__)
CORS(app)
session_data = {}

@app.route('/ping')
def ping():
    return jsonify({"alive": True})

@app.route('/login', methods=['POST'])
def login():
    d = request.json
    try:
        obj = SmartConnect(api_key=d['apiKey'])
        totp = pyotp.TOTP(d['totpSecret']).now()
        data = obj.generateSession(d['clientId'], d['password'], totp)
        if data['status']:
            session_data['obj'] = obj
            return jsonify({"ok": True})
        return jsonify({"ok": False, "error": data['message']})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)})

@app.route('/candles', methods=['POST'])
def candles():
    d = request.json
    try:
        obj = session_data['obj']
        data = obj.getCandleData({"exchange":"NSE","symboltoken":d['token'],"interval":d['interval'],"fromdate":d['fromdate'],"todate":d['todate']})
        if data['status']:
            return jsonify({"ok": True, "data": data['data']})
        return jsonify({"ok": False, "error": data['message']})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5050)))
