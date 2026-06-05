import os
import asyncio
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, ContextTypes, filters

TOKEN = os.environ.get("TOKEN")
ADMIN_ID = int(os.environ.get("ADMIN_ID", 0))
PORT = int(os.environ.get("PORT", 8000))

# وب‌سرور هلت‌چک
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(b"OK")
    def log_message(self, format, *args):
        return

def run_health_server():
    try:
        server = HTTPServer(('0.0.0.0', PORT), HealthCheckHandler)
        server.serve_forever()
    except Exception as e:
        print(f"Web server error: {e}")

def get_main_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🛒 خرید کانفیگ پرسرعت", callback_data="buy_menu")],
        [InlineKeyboardButton("🧑‍💻 پشتیبانی و ارتباط با ما", callback_data="support")]
    ])

def get_packages_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("💎 پکیج ۵ گیگابایت", callback_data="pkg_5g")],
        [InlineKeyboardButton("💎 پکیج ۱۰ گیگابایت", callback_data="pkg_10g")],
        [InlineKeyboardButton("💎 پکیج ۲۰ گیگابایت", callback_data="pkg_20g")],
        [InlineKeyboardButton("🔙 بازگشت به منوی اصلی", callback_data="back_to_main")]
    ])

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message:
        user_name = update.message.from_user.first_name or "دوست من"
        await update.message.reply_text(
            f"سلام {user_name} عزیز! خیلی خوش اومدی دست‌گلت درد نکنه ❤️\n"
            "با این ربات می‌تونی راحت کانفیگ‌های پرسرعت بخری یا با پشتیبانی در ارتباط باشی. 👇",
            reply_markup=get_main_menu()
        )

async def button_click_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    
    if q.data == "buy_menu":
        await q.edit_message_text("لطفاً حجم مورد نظرت رو از بین پکیج‌های زیر انتخاب کن عزیزم: ✨", reply_markup=get_packages_menu())
    elif q.data == "back_to_main":
        await q.edit_message_text("به منوی اصلی برگشتیم. در خدمتت هستم: 👇", reply_markup=get_main_menu())
    elif q.data == "support":
        context.user_data["support"] = True
        await q.message.reply_text("جانم! مشکلی پیش اومده؟ یا سوالی داری؟ ❤️\nپیامت رو همین‌جا بنویس و بفرست، من سریع بررسی می‌کنم و بهت جواب می‌دم. 🌹")
    elif q.data == "pkg_5g":
        text = "🎯 **پکیج انتخابی شما: ۵ گیگابایت**\n📅 **مدت زمان:** یک‌ماهه با بالاترین سرعت\n💰 **قیمت:** ۸۰ هزار تومان\n\n💳 **شماره کارت جهت واریز:**\n`6104338644728640`\n👤 **به نام:** امیررضا هژبر\n\nلطفاً بعد از واریز وجه، **عکس رسیدت رو همین‌جا برام بفرست** تا اکانتت رو در سریع‌ترین زمان ممکن تحویلت بدم. دم شما گرم! 🙏❤️"
        await q.edit_message_text(text, parse_mode="Markdown")
    elif q.data == "pkg_10g":
        text = "🎯 **پکیج انتخابی شما: ۱۰ گیگابایت**\n📅 **مدت زمان:** یک‌ماهه با بالاترین سرعت\n💰 **قیمت:** ۱۲۰ هزار تومان\n\n💳 **شماره کارت جهت واریز:**\n`6104338644728640`\n👤 **به نام:** امیررضا هژبر\n\nلطفاً بعد از واریز وجه، **عکس رسیدت رو همین‌جا برام بفرست** تا اکانتت رو در سریع‌ترین زمان ممکن تحویلت بدم. دم شما گرم! 🙏❤️"
        await q.edit_message_text(text, parse_mode="Markdown")
    elif q.data == "pkg_20g":
        text = "🎯 **پکیج انتخابی شما: ۲۰ گیگابایت**\n📅 **مدت زمان:** یک‌ماهه با بالاترین سرعت\n💰 **قیمت:** ۲۰۰ هزار تومان\n\n💳 **شماره کارت جهت واریز:**\n`6104338644728640`\n👤 **به نام:** امیررضا هژبر\n\nلطفاً بعد از واریز وجه، **عکس رسیدت رو همین‌جا برام بفرست** تا اکانتت رو در سریع‌ترین زمان ممکن تحویلت بدم. دم شما گرم! 🙏❤️"
        await q.edit_message_text(text, parse_mode="Markdown")

async def global_message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return
    user_id = update.message.chat_id
    user_name = update.message.from_user.first_name or "کاربر"

    if user_id == ADMIN_ID:
        if update.message.reply_to_message:
            try:
                target_text = update.message.reply_to_message.caption or update.message.reply_to_message.text
                if target_text and "User ID:" in target_text:
                    target_user_id = int(target_text.split("User ID:")[1].strip())
                    await context.bot.copy_message(chat_id=target_user_id, from_chat_id=ADMIN_ID, message_id=update.message.message_id)
                    await update.message.reply_text("✅ پیامت با موفقیت و محبت به دست مشتری رسید!")
                else:
                    await update.message.reply_text("❌ خطا: این پیام اطلاعات کاربر (User ID) رو نداره.")
            except Exception as e:
                await update.message.reply_text(f"❌ خطا در ارسال پیام به مشتری: {e}")
        return

    if update.message.photo:
        await update.message.reply_text("خیلی ممنونم از اعتمادت دوست من! ❤️ رسیدت دریافت شد.\nدر حال بررسیش هستم و تا چند دقیقه دیگه اکانتت رو برات می‌فرستم. صبوری گلت رو قربون! ✨")
        if ADMIN_ID:
            await context.bot.send_photo(chat_id=ADMIN_ID, photo=update.message.photo[-1].file_id, caption=f"📥 **رسید پرداخت جدید**\n👤 فرستنده: {user_name}\nUser ID: {user_id}")
        return

    if context.user_data.get("support"):
        context.user_data["support"] = False
        await update.message.reply_text("پیامت رو گرفتم عزیز دلم! 🌹 به ادمین منتقلش کردم، به زودی همین‌جا بهت جواب میده.")
        if ADMIN_ID and update.message.text:
            await context.bot.send_message(chat_id=ADMIN_ID, text=f"📩 **پیام پشتیبانی جدید**\n👤 از طرف: {user_name}\n💬 متن پیام:\n{update.message.text}\n\nUser ID: {user_id}")

# 🛠️ بازنویسی متد اجرا بدون تداخل با باگ لوپ پایتون ۳.۱۴
async def run_bot_safe():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CallbackQueryHandler(button_click_handler))
    app.add_handler(MessageHandler(filters.TEXT | filters.PHOTO | filters.Document, global_message_handler))

    await app.initialize()
    await app.start()
    
    # استفاده از لوپ دستی به جای متدهای خراب کتابخانه
    updater = app.updater
    await updater.start_polling(drop_pending_updates=True)
    print("Bot is fully running safely now...")
    
    while True:
        await asyncio.sleep(3600)

if __name__ == "__main__":
    threading.Thread(target=run_health_server, daemon=True).start()
    print(f"Web Health Check Server started on port {PORT}")
    
    # دور زدن ارور runners.py پایتون ۳.۱۴ با ساخت مستقیم لوپ
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(run_bot_safe())
    except (KeyboardInterrupt, SystemExit):
        print("Bot stopped.")
