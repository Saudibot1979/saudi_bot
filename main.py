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

NAMES = {
"MCRO":"ماكرو جروب","OCPH":"اكتوبر فارما","MBSC":"مصر للاسمنت بني سويف",
"MTIE":"ام ام جروب","PRCL:"شيني ","SKPC":"سيدي كرير",
"EGAL":"مصر للالومنيوم","EGAS":"جاس مصر","ADIB":"مصرف ابوظبي الاسلامي",
"RREI":"اليكو","SCEM":"اسمنت سيناء","ISMQ":المناجم"

EGX_HALAL = list(NAMES.keys())

def check_stock(symbol):
    try:
        df = yf.download(f"{symbol}.CA", period="3mo", progress=False)
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
    for s in EGX_HALAL:
        r=check_stock(s)
        if r: found.append(r)
    if not found:
        send_tg("📊 لا توجد فرص قوية اليوم في اسهمك الـ 12 الحلال")
        return "No signals"
    msg="📈 *توصيات اليوم - بورصة مصر حلال*\n\n"
    for x in found[:12]:
        name = NAMES.get(x['symbol'], x['symbol'])
        msg+=f"🟢 {name} ({x['symbol']}) - {x['price']:.2f} ج.م\n"
    msg+="\n⚠️ ليست نصيحة استثمارية - قرارك مسئوليتك"
    send_tg(msg)
    return msg

if __name__=="__main__":
    app.run(host="0.0.0.0",port=8080)
