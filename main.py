import time
import requests
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

API_URL = "https://draw.ar-lottery01.com/TrxWinGo/TrxWinGo_1M/GetHistoryIssuePage.json"

@app.route('/api/fetch', methods=['GET'])
def fetch_live_data():
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        # Live API ကို တိုက်ရိုက်ခေါ်မည်
        res = requests.get(f"{API_URL}?ts={int(time.time()*1000)}", headers=headers, timeout=10)
        
        if res.status_code != 200:
            return jsonify({"status": "error", "message": f"API HTTP Error {res.status_code}"}), 502

        raw_data = res.json()
        items = raw_data.get("data", {}).get("list", [])
        
        if not items:
            return jsonify({"status": "error", "message": "API returned empty list"}), 500

        formatted_history = []
        for item in items:
            issue = str(item.get("issueNumber", ""))
            num = int(item.get("number", 0))
            if issue:
                bs = "BIG" if num >= 5 else "SMALL"
                formatted_history.append({
                    "issue": issue,
                    "number": num,
                    "bs": bs,
                    "time": time.strftime("%H:%M:%S", time.localtime())
                })

        return jsonify({
            "status": "success",
            "total": len(formatted_history),
            "data": formatted_history
        })

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# Vercel Serverless အတွက် app ကို တိုက်ရိုက် Export လုပ်သည် (app.run မသုံးပါ)
if __name__ == '__main__':
    app.run()
