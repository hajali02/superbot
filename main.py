from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
import config
from modules import media_downloader, image, audio

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📥 دانلود ویدیو", callback_data="download")],
        [InlineKeyboardButton("🖼️ متن به تصویر", callback_data="text_image")],
        [InlineKeyboardButton("🔊 متن به صدا", callback_data="text_speech")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("سلام! یک گزینه انتخاب کن:", reply_markup=reply_markup)

async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    if data == "download":
        await query.message.reply_text("لینک ویدیوی یوتیوب یا منابع دیگه رو بفرست:")
        context.user_data["mode"] = "download"
    elif data == "text_image":
        await query.message.reply_text("متنت رو بفرست تا برات عکس بسازم:")
        context.user_data["mode"] = "text_image"
    elif data == "text_speech":
        await query.message.reply_text("متنت رو بفرست تا برات تبدیل به صدا کنم:")
        context.user_data["mode"] = "text_speech"

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mode = context.user_data.get("mode")
    if mode == "download":
        await media_downloader.download(update, context)
    elif mode == "text_image":
        await image.text_to_image(update, context)
    elif mode == "text_speech":
        await audio.text_to_speech(update, context)
    else:
        await update.message.reply_text("برای شروع /start رو بزن.")

if __name__ == "__main__":
    app = ApplicationBuilder().token(config.TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_click))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()
