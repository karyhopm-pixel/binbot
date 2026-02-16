import telebot
import requests
import os

TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "6 digit BIN bhejo")

@bot.message_handler(func=lambda message: True)
def bin_lookup(message):
    bin_number = message.text.strip()

    if not bin_number.isdigit() or len(bin_number) != 6:
        bot.reply_to(message, "Sirf 6 digit BIN bhejo")
        return

    r = requests.get(f"https://lookup.binlist.net/{bin_number}")

    if r.status_code == 200:
        data = r.json()
        bank = data.get("bank", {}).get("name", "N/A")
        country = data.get("country", {}).get("name", "N/A")
        scheme = data.get("scheme", "N/A")
        card_type = data.get("type", "N/A")

        bot.reply_to(message,
            f"BIN: {bin_number}\n"
            f"Bank: {bank}\n"
            f"Country: {country}\n"
            f"Scheme: {scheme}\n"
            f"Type: {card_type}"
        )
    else:
        bot.reply_to(message, "Data nahi mila")

bot.polling()
