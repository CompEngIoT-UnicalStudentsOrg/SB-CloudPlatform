from telegram.ext import Updater, CommandHandler
import requests
import logging
import json
import os


from flask_restplus import Api, Resource
from flask import Flask

from webargs.flaskparser import use_args
from webargs import fields

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
api = Api(app)

token = os.environ["TELEGRAM_KEY"]
endpoint = "http://backend:1880/api/room/{}"
updater = Updater(token)    

admin_ids = set()


def notify(room):
    msg = f"Max capacity reached for room #{room}"
    for admin_id in admin_ids:
        updater.bot.send_message(chat_id=admin_id, text=msg)


def start_handler(update, context):
    admin_id = update.effective_chat.id
    admin_ids.add(admin_id)
    logging.info("received start - ", admin_ids)


def end_handler(update, context):
    admin_id = update.effective_chat.id
    admin_ids.remove(admin_id)
    logging.info("received end - ", admin_ids)


def get_handler(update, context):
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



@api.route("/api/notify")
class Notifier(Resource):
    @use_args({
        "room": fields.Int(required=True)    
    })
    def post(self, args):
        room = 0
        try:
            room = int(args["room"])
        except:
            return {"error": "invalid room id"}, 422

        if room < 0 or room > 4:
            return {"error": "invalid room id"}, 422
        
        notify(room)
        return {"outcome": "admins correctly notified"}, 200


if __name__ == "__main__":
    updater.dispatcher.add_handler(CommandHandler("get", get_handler))
    updater.dispatcher.add_handler(CommandHandler("start", start_handler))
    updater.dispatcher.add_handler(CommandHandler("end", end_handler))
    updater.start_polling()
    app.run(host="0.0.0.0", port=80)