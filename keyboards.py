from telebot.types import KeyboardButton,ReplyKeyboardMarkup,InlineKeyboardButton,InlineKeyboardMarkup




start = InlineKeyboardMarkup()

start.add(InlineKeyboardButton("🔴YouTube",callback_data="YouTube"),InlineKeyboardButton("🟣pinterst",callback_data="Pin"))
start.add(InlineKeyboardButton("👻instagram",callback_data="instagram"))
start.add(InlineKeyboardButton("👩‍💻support",callback_data="support"))


