from telegram.ext import Updater, CommandHandler
import requests
import json


token = ""
endpoint = "http://localhost:1880/api/room/{}"

def get_handler(update, context):
    # print(update, context)
    argv = context.args
    room = None
    try:
        room = int(argv[0])
    except:
        update.message.reply_text("invalid arguments\nget [room id]")
        return

    data = requests.get(endpoint.format(argv[0]))
    j_data = json.loads(data.text)

    resp = " ".join([f"{key}: {val}" for key, val in j_data.items()])
    update.message.reply_text(resp)

if __name__ == "__main__":
    updater = Updater(token)
    updater.dispatcher.add_handler(CommandHandler("get", get_handler))
    updater.start_polling()
    updater.idle()