import telebot
import json
import datetime
import os

TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(8518611841:AAHZADDJ9jFEj_ciBE0Gl4SoWmQ21vxz8Fs)

DATA_FILE = "data.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

@bot.message_handler(commands=['start'])
def start(msg):
    data = load_data()
    uid = str(msg.from_user.id)
    if uid not in data:
        data[uid] = {"name": msg.from_user.first_name, "status": "out", "log": []}
        save_data(data)
    bot.reply_to(msg, "Вы зарегистрированы. Используйте /in чтобы отметить приход, /out — уход.")

@bot.message_handler(commands=['in'])
def come(msg):
    data = load_data()
    uid = str(msg.from_user.id)
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data[uid]["status"] = "in"
    data[uid]["log"].append(f"Приход: {now}")
    save_data(data)
    bot.reply_to(msg, f"Отмечено! Пришли в {now}")

@bot.message_handler(commands=['out'])
def leave(msg):
    data = load_data()
    uid = str(msg.from_user.id)
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data[uid]["status"] = "out"
    data[uid]["log"].append(f"Уход: {now}")
    save_data(data)
    bot.reply_to(msg, f"Ушли в {now}")

@bot.message_handler(commands=['who'])
def who(msg):
    data = load_data()
    online = [v["name"] for v in data.values() if v["status"] == "in"]
    if not online:
        bot.reply_to(msg, "На месте никого нет.")
    else:
        bot.reply_to(msg, "Сейчас на работе:\n" + "\n".join(online))

@bot.message_handler(commands=['report'])
def report(msg):
    data = load_data()
    uid = str(msg.from_user.id)
    if uid not in data:
        bot.reply_to(msg, "Вы не зарегистрированы")
        return

    log = "\n".join(data[uid]["log"])
    bot.reply_to(msg, f"Ваш отчёт:\n\n{log}")

bot.polling(none_stop=True)
