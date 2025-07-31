import os
from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Load BLIP model
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

# Function to generate caption from image
def describe_image(image_path: str) -> str:
    try:
        image = Image.open(image_path).convert('RGB')
        inputs = processor(image, return_tensors="pt")
        out = model.generate(**inputs)
        return processor.decode(out[0], skip_special_tokens=True)
    except Exception as e:
        return f"Error generating caption: {e}"

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Hello! Send me a photo and I will describe it for you.\nUse /help to see available commands."
    )

# /help command
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🛠 Available commands:\n"
        "/start - Welcome message\n"
        "/help - Show this help message\n"
        "Just send an image and I’ll describe it!"
    )

# Handle incoming photo
async def handle_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        photo = await update.message.photo[-1].get_file()
        path = "temp.jpg"
        await photo.download_to_drive(path)

        caption = describe_image(path)
        await update.message.reply_text(f"🖼 Description: {caption}")

        os.remove(path)  # Clean up
    except Exception as e:
        await update.message.reply_text(f"⚠️ Failed to process the image: {e}")

# Setup and run bot
app = ApplicationBuilder().token("8340044756:AAHd8b00dc6C_gfWDL4sY7aUOz70RTMWxlI").build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_command))
app.add_handler(MessageHandler(filters.PHOTO, handle_image))

app.run_polling()
