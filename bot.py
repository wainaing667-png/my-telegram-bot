import os
import base64
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from openai import OpenAI

# Telegram Bot Token နဲ့ OpenAI API Key
TELEGRAM_TOKEN = "9214748447:AAGI9Cj2zh7eylAgVvQ3fuwbcov3ZO-Hx9Q"
OPENAI_API_KEY = "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"

client = OpenAI(api_key=OPENAI_API_KEY)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("မင်္ဂလာပါ။ တိရစ္ဆာန်ပုံ ပို့ပေးပါ၊ ဘာသတ္တဝါလဲ မြန်မာလို ရှင်းပြပါမယ်။")

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("ဓာတ်ပုံကို စစ်ဆေးနေပါသည်...")
    
    try:
        photo_file = await update.message.photo[-1].get_file()
        image_bytes = await photo_file.download_as_bytearray()
        encoded_image = base64.b64encode(image_bytes).decode('utf-8')
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "ဒီပုံထဲက တိရစ္ဆာန်က ဘာလဲဆိုတာ မြန်မာဘာသာဖြင့် ရှင်းပြပေးပါ။"},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{encoded_image}"}}
                    ]
                }
            ],
            max_tokens=300
        )
        
        reply_text = response.choices[0].message.content
        await update.message.reply_text(reply_text)

    except Exception as e:
        await update.message.reply_text(f"အမှားဖြစ်ပေါ်ခဲ့သည်: {str(e)}")

def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))

    print("Bot စတင်အလုပ်လုပ်နေပါပြီ...")
    app.run_polling()

if __name__ == '__main__':
    main()
  
