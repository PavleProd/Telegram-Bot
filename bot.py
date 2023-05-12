import os
import requests
from telegram import Update, InputMediaDocument
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import yt_dlp

TOKEN = "6127757477:AAGeY1acFoXGB2MDdUcA46PIkFi9IKvLPcI"
allowedImageFormats = ("jpg", "png", "jpeg", "gif", "webp")
allowedVideoFormats = ("mp4", "mov")


# Commands
async def startCommand(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hi, send me an image URL and I'll send the image back to you!")


def isImageURL(url: str) -> bool:
    return any(url.endswith(extension) for extension in allowedImageFormats)


def isVideoURL(url: str) -> bool:
    return any(url.endswith(extension) for extension in allowedVideoFormats)


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


async def downloadVideo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    messageText = update.message.text
    chat_id = update.message.chat_id

    ydl_opts = {'outtmpl': 'video.mp4', 'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([messageText])

    # Upload the video to Telegram
    with open('video.mp4', 'rb') as f:
        await context.bot.send_media_group(chat_id=chat_id, media=[InputMediaDocument(media=f, filename='video.mp4')])

    # Remove the downloaded video file
    os.remove('video.mp4')


async def messageHandler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.chat.id
    messageText = update.message.text

    # Log user input
    print(f'User ({user}): "{messageText}"')

    if isImageURL(messageText):
        await downloadImage(update, context)
    elif isVideoURL(messageText):
        await downloadVideo(update, context)
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="URL for image/video was invalid")


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
