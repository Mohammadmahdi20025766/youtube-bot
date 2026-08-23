import os
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
import yt_dlp

# اطلاعات ربات
API_ID = 24579746
API_HASH = "7b5df16ae014f983a31a96fc3344fb78"
BOT_TOKEN = "8748562972:AAGCViz8gy5JyZ2HsjKnWhzB3xeo1SR-uxo"

app = Client("My_Bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

BOT_VERSION = "0.0.0"

@app.on_message(filters.command("start"))
async def start_handler(client: Client, message: Message):
    await message.reply_text(
        f"سلام {message.from_user.first_name} عزیز! 🖐\n"
        "به ربات من خوش آمدید.\n"
        "لینک ویدیو رو بفرست تا دانلودش کنم.",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("✨ کانال ما", url="https://t.me/your_channel")]
        ])
    )

@app.on_message(filters.command("version"))
async def version_handler(client: Client, message: Message):
    await message.reply_text(f"🤖 **نسخه فعلی ربات:** `{BOT_VERSION}`\nوضعیت: پایدار و آماده به کار ✅")

@app.on_message(filters.command("help"))
async def help_handler(client: Client, message: Message):
    await message.reply_text(
        "📖 **راهنمای استفاده از ربات:**\n\n"
        "1️⃣ کافیه لینک ویدیوی یوتیوب رو بفرستید.\n"
        "2️⃣ ربات ویدیو رو پردازش و براتون ارسال می‌کنه.\n"
        "3️⃣ از دستورات منو هم می‌تونید برای اطلاعات بیشتر استفاده کنید."
    )

@app.on_message(filters.command("creator"))
async def creator_handler(client: Client, message: Message):
    await message.reply_text("👨‍💻 **سازنده ربات:** محمد مهدی\nتوسعه‌یافته با پایتون و عشق ⚡️")

@app.on_message(filters.text & filters.private & ~filters.command(["start", "version", "help", "creator"]))
async def download_handler(client: Client, message: Message):
    url = message.text.strip()
    if "youtube.com" in url or "youtu.be" in url:
        status = await message.reply_text("⏳ در حال دریافت ویدیو...")
        try:
            ydl_opts = {'format': 'best[ext=mp4]/best', 'outtmpl': 'downloads/%(id)s.%(ext)s'}
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)
            
            await status.edit_text("📤 در حال ارسال...")
            await message.reply_video(video=filename, caption=info.get('title', 'Video'))
            
            if os.path.exists(filename):
                os.remove(filename)
            await status.delete()
        except Exception as e:
            await status.edit_text(f"❌ خطا:\n`{str(e)}`")
    else:
        await message.reply_text("❌ لطفاً یک لینک معتبر بفرستید.")

print("Bot is running...")
app.run()
