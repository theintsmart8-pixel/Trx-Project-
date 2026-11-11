import os
import json
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
        # Live API ကို တိုက်ရိုက်လှမ်းခေါ်မည် (Cache ရှောင်ရန် ts ထည့်ထားသည်)
        res = requests.get(f"{API_URL}?ts={int(time.time()*1000)}", timeout=8)
        
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
        # API ချိတ်ဆက်မှု မရပါက Error သက်သက်သာ ပြန်မည် (Offline Data လုံးဝမသုံးပါ)
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
