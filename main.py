import yfinance as yf, requests, os
from flask import Flask
app = Flask(__name__)
BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
def send_tg(msg):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        requests.post(url, json={"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"})
    except: pass
HALAL_38 = ["2222","2010","2020","2030","2050","2060","2080","2100","2110","2150","2160","2170","2180","2190","2200","2210","2230","2240","2250","2260","2280","2300","2310","2320","2350","2360","2380","4001","4002","4003","4005","4006","4011","4013","4020","4030","4040","4050"]
def check_stock(symbol):
    try:
        df = yf.download(f"{symbol}.SR", period="3mo", progress=False)
        if len(df) < 25: return None
        df['PVT'] = (df['Close'].pct_change() * df['Volume']).cumsum()
        price_now = float(df['Close'].iloc[-1])
        price_prev = float(df['Close'].iloc[-2])
        price_pct = ((price_now - price_prev)/price_prev)*100
        pvt_pct = float((df['PVT'].iloc[-1] - df['PVT'].iloc[-2])/abs(df['PVT'].iloc[-2])*100) if df['PVT'].iloc[-2]!=0 else 0
        if pvt_pct > price_pct + 3:
            return {"symbol":symbol,"price":price_now}
    except: return None
    return None
@app.route("/")
def run():
    found=[]
    for s in HALAL_38:
        r=check_stock(s)
        if r: found.append(r)
    if not found:
        send_tg("📊 لا توجد فرص قوية اليوم في الـ 38 سهم النقي")
        return "No signals"
    msg="📈 *توصيات اليوم - 38 سهم نقي حلال*\n\n"
    for x in found[:10]:
        msg+=f"🟢 {x['symbol']} - {x['price']:.2f}\n"
    msg+="\n⚠️ ليست نصيحة استثمارية"
    send_tg(msg)
    return msg
if __name__=="__main__":
    app.run(host="0.0.0.0",port=8080)
