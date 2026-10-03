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
"2222":"أرامكو","2010":"سابك","2020":"سابك للمغذيات","2030":"المصافي","2050":"سافكو","2060":"التصنيع","2080":"غازكو","2100":"فواز الحكير","2110":"الكهرباء","2150":"البابطين","2160":"اميانتيت","2170":"اللجين","2180":"فيبكو","2190":"سيسكو","2200":"أنابيب","2210":"نماء","2230":"الكيميائية","2240":"الزامل","2250":"المجموعة","2260":"الصحراء","2280":"المراعي","2300":"صناعة الورق","2310":"سبكيم","2320":"البابطين","2350":"كيان","2360":"الحكير","2380":"بترو رابغ","4001":"العثيم","4002":"المواساة","4003":"إكسترا","4005":"رعاية","4006":"أسواق المزرعة","4011":"دور","4013":"سليمان الحبيب","4020":"العقارية","4030":"البحري","4040":"سيرا","4050":"سيارات"
}

HALAL_38 = list(NAMES.keys())

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
        name = NAMES.get(x['symbol'], x['symbol'])
        msg+=f"🟢 {name} ({x['symbol']}) - {x['price']:.2f} ر.س\n"
    msg+="\n⚠️ ليست نصيحة استثمارية"
    send_tg(msg)
    return msg

if __name__=="__main__":
    app.run(host="0.0.0.0",port=8080)
