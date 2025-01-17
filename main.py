import os
while 1:
    try:
        from telebot.async_telebot import AsyncTeleBot
        from telebot.types import Message,CallbackQuery
        from pysondb.db import JsonDatabase
        import config as cf
        from jdatetime import datetime
        import asyncio,keyboards,logging,traceback,telebot,re
        from pytubefix import YouTube
        break
    except ModuleNotFoundError as e:
        os.system(f"pip install {str(e).split("'")[1]}")

# ------------------------------------------
# ------------------------------------------
_logger = logging.getLogger("AcceptBotLog")
_logger.setLevel(logging.DEBUG)
formatter = logging.Formatter(f'{datetime.now().strftime("%Y-%M-%d %H:%M:%S")} - %(name)s - %(levelname)s - %(message)s\n{"-"*40}')
# --------------file handler----------------
file_handler = logging.FileHandler("bot.log")
file_handler.setFormatter(formatter)
# ------------------------------------------
# ---Outputs debug messages to console------
console_logger = logging.StreamHandler()
console_logger.setFormatter(formatter)
# ------------------------------------------

_logger.addHandler(file_handler)
_logger.addHandler(console_logger)

# -------ignore deafult telebot logs--------
telebot.logger.setLevel(logging.CRITICAL)

class MyExceptionHandler(telebot.ExceptionHandler):
    def handle(exception):
        _logger.error(traceback.format_exc())


bot = AsyncTeleBot(token=cf.token,exception_handler=MyExceptionHandler)

database_path = "database.json"
database_name = {"db":"main"}

database = JsonDatabase(database_path)


# 0----create database if doesnt exist----0
if database.getByQuery(database_name) == []:
    database.add({
        "db":"main",
        "users":{}
        
})

# -----save data in database-----
def save(json) -> None:
    database.updateByQuery(database_name,json)


PARSE = "MarkdownV2"



@bot.message_handler(["start"])
async def messageHandler(message:Message):
    await bot.reply_to(message,cf.startMSG,parse_mode=PARSE,reply_markup=keyboards.start)

@bot.message_handler()
async def messageHandler(message:Message):
    link = re.findall(r"https?://[^\s]+",message.text)[0]

    if "youtube" in link.lower():
        await bot.send_message(message.chat.id,"⏳")
        print(link)
        yt = YouTube(link)
        print(yt.streams.first())
        # await bot.reply_to(message,str())
        print(1)
        

@bot.callback_query_handler()
async def callbackQueryHandler(call:CallbackQuery):
    db:dict = database.getByQuery(database_name)[0]
    message = call.message
    userID = str(call.from_user.id)
    

    if call.data == "YouTube":
        await bot.reply_to(message,cf.YouTube)


while 1:
    try:
        asyncio.run(bot.infinity_polling())
    except KeyboardInterrupt:
        print("Bye Bye")
        break
    except:
        traceback.print_exc()