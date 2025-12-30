import telebot
import json
import datetime
import os

# Токен через переменную окружения (безопаснее для деплоя)
TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

DATA_FILE = "data.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def safe_send(msg, text):
    """Отправка сообщения без зависимости от reply_to"""
    bot.send_message(msg.chat.id, text)

@bot.message_handler(commands=['start'])
def start(msg):
    data = load_data()
    uid = str(msg.from_user.id)
    if uid not in data:
        data[uid] = {"name": msg.from_user.first_name, "status": "out", "log": []}
        save_data(data)
    safe_send(msg, "Вы зарегистрированы. Используйте /in чтобы отметить приход, /out — уход.")

@bot.message_handler(commands=['in'])
def come(msg):
    data = load_data()
    uid = str(msg.from_user.id)
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data[uid]["status"] = "in"
    data[uid]["log"].append(f"Приход: {now}")
    save_data(data)
    safe_send(msg, f"Отмечено! Пришли в {now}")

@bot.message_handler(commands=['out'])
def leave(msg):
    data = load_data()
    uid = str(msg.from_user.id)
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data[uid]["status"] = "out"
    data[uid]["log"].append(f"Уход: {now}")
    save_data(data)
    safe_send(msg, f"Ушли в {now}")

@bot.message_handler(commands=['who'])
def who(msg):
    data = load_data()
    online = [v["name"] for v in data.values() if v["status"] == "in"]
    if not online:
        safe_send(msg, "На месте никого нет.")
    else:
        safe_send(msg, "Сейчас на работе:\n" + "\n".join(online))

@bot.message_handler(commands=['report'])
def report(msg):
    data = load_data()
    uid = str(msg.from_user.id)
    if uid not in data:
        safe_send(msg, "Вы не зарегистрированы")
        return
    log = "\n".join(data[uid]["log"])
    safe_send(msg, f"Ваш отчёт:\n\n{log}")

bot.polling(none_stop=True)