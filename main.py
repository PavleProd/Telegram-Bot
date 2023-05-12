import os
import requests
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

TOKEN = "6127757477:AAGeY1acFoXGB2MDdUcA46PIkFi9IKvLPcI"


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Hi, send me an image URL and I'll download and send it back to you!")


def download_image(update, context):
    text = update.message.text
    if text.startswith("http") and (text.endswith(".jpg") or text.endswith(".png") or text.endswith(".jpeg")):
        try:
            response = requests.get(text)
            with open("image.jpg", "wb") as f:
                f.write(response.content)
            context.bot.send_photo(chat_id=update.effective_chat.id, photo=open("image.jpg", "rb"))
        except Exception as e:
            context.bot.send_message(chat_id=update.effective_chat.id, text=f"Sorry, there was an error: {e}")
        finally:
            os.remove("image.jpg")
    else:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Sorry, please send a valid image URL ending with .jpg, .png, or .jpeg.")


def main():
    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    download_image_handler = MessageHandler(Filters.text & (~Filters.command), download_image)

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(download_image_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
