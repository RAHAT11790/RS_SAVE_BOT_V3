from flask import Flask, jsonify
import time
import os

app = Flask(__name__)

@app.route('/')
def health():
    return "✅ Bot is running!", 200

@app.route('/health')
def health_check():
    return jsonify({
        "status": "alive",
        "bot": "running",
        "timestamp": time.time()
    }), 200

@app.route('/ping')
def ping():
    return "pong", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port, debug=False)
