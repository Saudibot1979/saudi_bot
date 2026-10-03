
import os, requests, random
BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
NAMES = {"TASI":"تاسي","ARAMCO":"ارامكو","ALRAJHI":"الراجحي","STC":"STC","MTIE":"ام جروب"}
def send_tg(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    try:
        requests.post(url, json={"chat_id": CHAT_ID, "text": msg}, timeout=10)
    except Exception as e:
        print(e)
msg = "📈 توصية اليوم\n\n"
for k,v in random.sample(list(NAMES.items()),3):
    msg += f"- {v} ({k}): {random.choice(['صعود','استقرار'])}\n"
msg += "\n⏰ 8 صباحا بتوقيت الرياض"
send_tg(msg)
print("Done")
