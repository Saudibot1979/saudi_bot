import yfinance as yf, requests, time, os
from flask import Flask

app = Flask(__name__)
BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

def send_tg(msg):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        requests.post(url, json={"chat_id": CHAT_ID, "text": msg})
    except: pass

def check_stock(symbol):
    try:
        df = yf.download(f"{symbol}.SR", period="3mo", interval="1h", progress=False)
        if len(df) < 25: return None
        df['PVT'] = (df['Close'].pct_change() * df['Volume']).cumsum()
        price_pct = float((df['Close'].iloc[-1] / df['Close'].iloc[-20] -1)*100)
        pvt_pct = float((df['PVT'].iloc[-1] / df['PVT'].iloc[-20] -1)*100)
        prev_high = float(df['High'].iloc[-2]); curr_low = float(df['Low'].iloc[-1])
        gap = (prev_high, curr_low) if curr_low > prev_high*1.002 else None
        if pvt_pct > price_pct + 3:
            return {"symbol":symbol,"price_pct":round(price_pct,2),"pvt_pct":round(pvt_pct,2),"gap":gap,"price":round(float(df['Close'].iloc[-1]),2)}
    except: return None
    return None

def loop():
    stocks = ["MBSC","OCPH","ARAMCO","STC","ALRAJHI","MAADEN","JAHEZ","LUMI"]
    while True:
        for s in stocks:
            r = check_stock(s)
            if r:
                gap_txt = f"\nفجوة {r['gap'][0]:.2f} -> امر {r['gap'][0]*1.003:.2f}" if r['gap'] else ""
                msg = f"🔥 {r['symbol']} بطريقتنا\nسعر {r['price']} ({r['price_pct']}%)\nPVT {r['pvt_pct']}%{gap_txt}"
                send_tg(msg)
        time.sleep(3600)

import threading
threading.Thread(target=loop, daemon=True).start()

@app.route("/")
def home(): return "Bot Running OK"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
