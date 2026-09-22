import os
import logging
from telebot import TeleBot, types

# --- Logging setup ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# --- Load token from environment ---
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN environment variable is not set!")

bot = TeleBot(BOT_TOKEN)

# --- Persistent reply keyboard ---
def main_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    keyboard.add(
        types.KeyboardButton("🔄 Reverse Text"),
        types.KeyboardButton("ℹ️ Help")
    )
    return keyboard

# --- /start command ---
@bot.message_handler(commands=["start"])
def send_welcome(message):
    text = (
        "👋 Welcome to Reverse Text Bot!\n\n"
        "Send me any text and I will flip it backwards instantly.\n\n"
        "Example: hello → olleh\n\n"
        "Use the buttons below or just type your text."
    )
    bot.send_message(message.chat.id, text, reply_markup=main_keyboard())

# --- /help command ---
@bot.message_handler(commands=["help"])
def send_help(message):
    text = (
        "ℹ️ How to use this bot:\n\n"
        "1. Type or paste any text.\n"
        "2. The bot will reply with the text reversed.\n\n"
        "Example:\n"
        "You send: Telegram\n"
        "Bot replies: margel eT\n\n"
        "No data is stored. No links. Just a simple text tool."
    )
    bot.send_message(message.chat.id, text, reply_markup=main_keyboard())

# --- /reverse command (explicit command version) ---
@bot.message_handler(commands=["reverse"])
def reverse_command(message):
    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        bot.send_message(
            message.chat.id,
            "Please provide text to reverse.\nExample: /reverse hello"
        )
        return
    reversed_text = parts[1][::-1]
    bot.send_message(message.chat.id, f"🔄 {reversed_text}")

# --- Handle button taps ---
@bot.message_handler(func=lambda msg: msg.text == "🔄 Reverse Text")
def prompt_reverse(message):
    bot.send_message(
        message.chat.id,
        "Send me the text you want to reverse."
    )

@bot.message_handler(func=lambda msg: msg.text == "ℹ️ Help")
def help_button(message):
    send_help(message)

# --- Main text handler: reverses any text ---
@bot.message_handler(func=lambda msg: True, content_types=["text"])
def reverse_text(message):
    user_text = message.text

    # Skip very long messages to avoid spam
    if len(user_text) > 1000:
        bot.send_message(
            message.chat.id,
            "⚠️ Text is too long. Please send up to 1000 characters."
        )
        return

    reversed_text = user_text[::-1]
    bot.send_message(message.chat.id, f"🔄 {reversed_text}")

# --- Fallback for non-text messages ---
@bot.message_handler(content_types=["photo", "video", "sticker", "document", "audio", "voice"])
def unsupported(message):
    bot.send_message(
        message.chat.id,
        "⚠️ Please send text only. I can only reverse text messages."
    )

# --- Start polling ---
if __name__ == "__main__":
    logger.info("Reverse Text Bot is starting...")
    bot.infinity_polling(skip_pending=True)
