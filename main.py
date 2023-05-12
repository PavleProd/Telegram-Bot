import os
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = "6127757477:AAGeY1acFoXGB2MDdUcA46PIkFi9IKvLPcI"


# Commands
async def startCommand(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hi, send me an image URL and I'll send the image back to you!")


def isImageURL(url: str) -> bool:
    if url.startswith("http") and (url.endswith(".jpg") or url.endswith(".png") or url.endswith(".jpeg")):
        return True
    return False


async def downloadImage(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    try:
        response = requests.get(text)
        with open("image.jpg", "wb") as f:
            f.write(response.content)
        await context.bot.send_photo(chat_id=update.effective_chat.id, photo=open("image.jpg", "rb"))
    except Exception as e:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Sorry, there was an error: {e}")
    finally:
        os.remove("image.jpg")


async def messageHandler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.chat.id
    messageText = update.message.text

    # Log user input
    print(f'User ({user}): "{messageText}"')

    if isImageURL(messageText):
        await downloadImage(update, context)
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text="URL was invalid. Please send URL ending with .jpg, .png, or .jpeg.")


def errorHandler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')


def main():
    print("Bot initialization...")
    bot = Application.builder().token(TOKEN).build()

    # Commands
    bot.add_handler(CommandHandler('start', startCommand))

    # Messages
    bot.add_handler(MessageHandler(filters.TEXT, messageHandler))

    # Errors
    bot.add_error_handler(errorHandler)

    # Polling
    print("Bot started polling...")
    bot.run_polling()


if __name__ == '__main__':
    main()
