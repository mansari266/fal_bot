from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import logging

# فعال کردن لاگ‌ها برای دیدن خطاهای احتمالی
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# فرمان start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "به بات فال روزانه خوش آمدید 🌙\n\n"
        "برای شروع تاریخ تولد خودتون رو با فرمت زیر وارد کنید:\nمثلاً: ۱۳۸۰/۰۱/۳۱"
    )

# گرفتن تاریخ تولد
async def get_birthdate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    if "/" not in text or len(text) < 8:
        await update.message.reply_text("فرمت تاریخ تولد اشتباهه 😅 لطفاً مثل نمونه وارد کنید: ۱۳۸۰/۰۱/۳۱")
        return

    context.user_data["birthdate"] = text
    keyboard = [["🔮 فال تاروت", "☀️ فال روزانه"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text("تاریخ تولد شما ثبت شد 🎉\nیکی از گزینه‌های زیر رو انتخاب کنید:", reply_markup=reply_markup)

# پاسخ به انتخاب‌ها
async def handle_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    choice = update.message.text
    if choice == "🔮 فال تاروت":
        await update.message.reply_text("کارت‌های تاروت شما در حال آماده شدن هستن... 🔮✨")
    elif choice == "☀️ فال روزانه":
        await update.message.reply_text("امروز روز فوق‌العاده‌ای برات پیش‌بینی شده ☀️🌸")
    else:
        await update.message.reply_text("گزینه‌ی نامعتبر. لطفاً از دکمه‌ها استفاده کنید 🙂")

def main():
    app = ApplicationBuilder().token("8237285591:AAElQBpguevUsmDG18jr_IEHZJlK0k53RI4").build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.Regex(r"^\d{4}/\d{2}/\d{2}$"), get_birthdate))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_choice))

    print("✅ ربات در حال اجراست... (Ctrl + C برای توقف)")
    app.run_polling()

if __name__ == "__main__":
    main()
