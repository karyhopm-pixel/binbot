import telebot
import requests
import os

TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TOKEN, parse_mode="HTML")

# ===== MEMORY STORAGE =====
history = {}

# ===== FLAG FUNCTION =====
def get_flag(country_code):
    if not country_code:
        return ""
    return ''.join(chr(127397 + ord(c)) for c in country_code.upper())

# ===== START =====
@bot.message_handler(commands=['start'])
def start(message):
    markup = telebot.types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        telebot.types.InlineKeyboardButton("🔎 Lookup Guide", callback_data="help"),
        telebot.types.InlineKeyboardButton("📜 My History", callback_data="history")
    )

    bot.send_message(
        message.chat.id,
        "─────────── <b>GLASS BIN BOT</b> ───────────\n\n"
        "Use command:\n"
        "<code>/bin 457173</code>\n\n"
        "Minimal • Fast • Premium",
        reply_markup=markup
    )

# ===== HELP BUTTON =====
@bot.callback_query_handler(func=lambda call: call.data == "help")
def help_callback(call):
    bot.answer_callback_query(call.id)
    bot.send_message(
        call.message.chat.id,
        "To lookup a BIN use:\n\n<code>/bin 457173</code>"
    )

# ===== HISTORY BUTTON =====
@bot.callback_query_handler(func=lambda call: call.data == "history")
def history_callback(call):
    bot.answer_callback_query(call.id)
    user_id = call.from_user.id

    if user_id not in history or not history[user_id]:
        bot.send_message(call.message.chat.id, "No history yet.")
        return

    text = "─────────── <b>YOUR HISTORY</b> ───────────\n\n"
    for b in history[user_id][-5:]:
        text += f"• <code>{b}</code>\n"

    bot.send_message(call.message.chat.id, text)

# ===== BIN COMMAND =====
@bot.message_handler(commands=['bin'])
def bin_lookup(message):
    try:
        bin_number = message.text.split()[1]
    except:
        bot.reply_to(message, "Usage:\n<code>/bin 457173</code>")
        return

    if not bin_number.isdigit() or len(bin_number) != 6:
        bot.reply_to(message, "❌ BIN must be 6 digits.")
        return

    loading = bot.reply_to(message, "🔎 Searching BIN...")

    try:
        r = requests.get(f"https://lookup.binlist.net/{bin_number}")
        if r.status_code != 200:
            bot.edit_message_text(
                "❌ BIN not found.",
                message.chat.id,
                loading.message_id
            )
            return

        data = r.json()

        scheme = data.get("scheme", "N/A")
        type_card = data.get("type", "N/A")
        bank = data.get("bank", {}).get("name", "N/A")
        country = data.get("country", {}).get("name", "N/A")
        country_code = data.get("country", {}).get("alpha2", "")

        flag = get_flag(country_code)

        # Save history
        history.setdefault(message.from_user.id, []).append(bin_number)

        reply = f"""
─────────── <b>BIN INFO</b> ───────────

<code>{bin_number}</code>

<b>{scheme.upper()}</b> • {type_card.upper()}
{bank}
{country} {flag}

────────── <i>VERIFIED</i> ──────────
"""

        bot.edit_message_text(
            reply,
            message.chat.id,
            loading.message_id
        )

    except:
        bot.edit_message_text(
            "⚠️ Error fetching BIN data.",
            message.chat.id,
            loading.message_id
        )

bot.infinity_polling()
