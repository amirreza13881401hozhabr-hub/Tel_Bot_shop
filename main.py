import os
import asyncio
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, ContextTypes, filters

TOKEN = os.environ.get("TOKEN")
ADMIN_ID = int(os.environ.get("ADMIN_ID", 0))
PORT = int(os.environ.get("PORT", 8000))

# وب‌سرور برای زنده نگه داشتن ربات در رندر
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

# منوی اصلی ربات
def get_main_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🛒 خرید کانفیگ پرسرعت", callback_data="buy_menu")],
        [InlineKeyboardButton("🧑‍💻 پشتیبانی و ارتباط با ما", callback_data="support")]
    ])

# منوی انتخاب پکیج‌ها (پنجره اول)
def get_packages_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("💎 پکیج ۵ گیگابایت", callback_data="pkg_5g")],
        [InlineKeyboardButton("💎 پکیج ۱۰ گیگابایت", callback_data="pkg_10g")],
        [InlineKeyboardButton("💎 پکیج ۲۰ گیگابایت", callback_data="pkg_20g")],
        [InlineKeyboardButton("🔙 بازگشت به منوی اصلی", callback_data="back_to_main")]
    ])

# دستور استارت
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message:
        user_name = update.message.from_user.first_name or "دوست من"
        await update.message.reply_text(
            f"سلام {user_name} عزیز! خیلی خوش اومدی دست‌گلت درد نکنه ❤️\n"
            "با این ربات می‌تونی راحت کانفیگ‌های پرسرعت بخری یا با پشتیبانی در ارتباط باشی. 👇",
            reply_markup=get_main_menu()
        )

# مدیریت کلیک روی دکمه‌ها
async def button_click_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    
    # رفتن به منوی خرید (لیست پکیج‌ها)
    if q.data == "buy_menu":
        await q.edit_message_text(
            "لطفاً حجم مورد نظرت رو از بین پکیج‌های زیر انتخاب کن عزیزم: ✨",
            reply_markup=get_packages_menu()
        )
        
    # بازگشت به منوی اصلی
    elif q.data == "back_to_main":
        await q.edit_message_text(
            "به منوی اصلی برگشتیم. در خدمتت هستم: 👇",
            reply_markup=get_main_menu()
        )
        
    # درخواست پشتیبانی
    elif q.data == "support":
        context.user_data["support"] = True
        await q.message.reply_text(
            "جانم! مشکلی پیش اومده؟ یا سوالی داری؟ ❤️\n"
            "پیامت رو همین‌جا بنویس و بفرست، من سریع بررسی می‌کنم و بهت جواب می‌دم. 🌹"
        )
        
    # جزئیات پکیج ۵ گیگ
    elif q.data == "pkg_5g":
        text = (
            "🎯 **پکیج انتخابی شما: ۵ گیگابایت**\n"
            "📅 **مدت زمان:** یک‌ماهه با بالاترین سرعت\n"
            "💰 **قیمت:** ۸۰ هزار تومان\n\n"
            "💳 **شماره کارت جهت واریز:**\n"
            "`6104338644728640`\n"
            "👤 **به نام:** امیررضا هژبر\n\n"
            "لطفاً بعد از واریز وجه، **عکس رسیدت رو همین‌جا برام بفرست** تا اکانتت رو در سریع‌ترین زمان ممکن تحویلت بدم. دم شما گرم! 🙏❤️"
        )
        await q.edit_message_text(text, parse_mode="Markdown")
        
    # جزئیات پکیج ۱۰ گیگ
    elif q.data == "pkg_10g":
        text = (
            "🎯 **پکیج انتخابی شما: ۱۰ گیگابایت**\n"
            "📅 **مدت زمان:** یک‌ماهه با بالاترین سرعت\n"
            "💰 **قیمت:** ۱۲۰ هزار تومان\n\n"
            "💳 **شماره کارت جهت واریز:**\n"
            "`6104338644728640`\n"
            "👤 **به نام:** امیررضا هژبر\n\n"
            "لطفاً بعد از واریز وجه، **عکس رسیدت رو همین‌جا برام بفرست** تا اکانتت رو در سریع‌ترین زمان ممکن تحویلت بدم. دم شما گرم! 🙏❤️"
        )
        await q.edit_message_text(text, parse_mode="Markdown")
        
    # جزئیات پکیج ۲۰ گیگ
    elif q.data == "pkg_20g":
        text = (
            "🎯 **پکیج انتخابی شما: ۲۰ گیگابایت**\n"
            "📅 **مدت زمان:** یک‌ماهه با بالاترین سرعت\n"
            "💰 **قیمت:** ۲۰۰ هزار تومان\n\n"
            "💳 **شماره کارت جهت واریز:**\n"
            "`6104338644728640`\n"
            "👤 **به نام:** امیررضا هژبر\n\n"
            "لطفاً بعد از واریز وجه، **عکس رسیدت رو همین‌جا برام بفرست** تا اکانتت رو در سریع‌ترین زمان ممکن تحویلت بدم. دم شما گرم! 🙏❤️"
        )
        await q.edit_message_text(text, parse_mode="Markdown")

# مدیریت پیام‌ها و رسیدها
async def global_message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return
    user_id = update.message.chat_id
    user_name = update.message.from_user.first_name or "کاربر"

    # بخش اول: اگر پیام از طرف تو (ادمین) باشد و روی پیام مشتری ریپلای کرده باشی
    if user_id == ADMIN_ID:
        if update.message.reply_to_message:
            try:
                # پیدا کردن آیدی کاربر از روی متنی که قبلاً ربات به ادمین فرستاده بود
                target_text = update.message.reply_to_message.caption or update.message.reply_to_message.text
                if target_text and "User ID:" in target_text:
                    target_user_id = int(target_text.split("User ID:")[1].strip())
                    
                    # کپی یا ارسال پیام ادمین برای مشتری
                    await context.bot.copy_message(
                        chat_id=target_user_id,
                        from_chat_id=ADMIN_ID,
                        message_id=update.message.message_id
                    )
                    await update.message.reply_text("✅ پیامت با موفقیت و محبت به دست مشتری رسید!")
                else:
                    await update.message.reply_text("❌ خطا: این پیام اطلاعات کاربر (User ID) رو نداره، نمی‌تونم براش بفرستم.")
            except Exception as e:
                await update.message.reply_text(f"❌ خطا در ارسال پیام به مشتری: {e}")
        return

    # بخش دوم: دریافت عکس رسید از مشتری
    if update.message.photo:
        await update.message.reply_text(
            "خیلی ممنونم از اعتمادت دوست من! ❤️ رسیدت دریافت شد.\n"
            "در حال بررسیش هستم و تا چند دقیقه دیگه اکانتت رو برات می‌فرستم. صبوری گلت رو قربون! ✨"
        )
        if ADMIN_ID:
            await context.bot.send_photo(
                chat_id=ADMIN_ID,
                photo=update.message.photo[-1].file_id,
                caption=f"📥 **رسید پرداخت جدید**\n👤 فرستنده: {user_name}\nUser ID: {user_id}"
            )
        return

    # بخش سوم: دریافت پیام پشتیبانی متنی از مشتری
    if context.user_data.get("support"):
        context.user_data["support"] = False
        await update.message.reply_text("پیامت رو گرفتم عزیز دلم! 🌹 به ادمین منتقلش کردم، به زودی همین‌جا بهت جواب میده.")
        if ADMIN_ID and update.message.text:
            await context.bot.send_message(
                chat_id=ADMIN_ID,
                text=f"📩 **پیام پشتیبانی جدید**\n👤 از طرف: {user_name}\n💬 متن پیام:\n{update.message.text}\n\nUser ID: {user_id}"
            )

# راه‌اندازی اصلی ربات
async def start_bot():
    if not TOKEN:
        print("Error: TOKEN is missing!")
        return

    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CallbackQueryHandler(button_click_handler))
    app.add_handler(MessageHandler(filters.TEXT | filters.PHOTO | filters.Document, global_message_handler))

    print("Telegram bot is starting...")
    await app.initialize()
    await app.start()
    await app.updater.start_polling(drop_pending_updates=True)
    
    while True:
        await asyncio.sleep(3600)

if __name__ == "__main__":
    # اجرای وب‌سرور هلت‌چک رندر
    threading.Thread(target=run_health_server, daemon=True).start()
    print(f"Web Health Check Server started on port {PORT}")
    
    # اجرای حلقه ناهمگام ربات کاملاً سازگار با لینوکس و پایتون جدید
    try:
        asyncio.run(start_bot())
    except (KeyboardInterrupt, SystemExit):
        print("Bot stopped.")
