# برج/ماه‌های ایرانی بر اساس عدد ماه شمسی (فقط ماه، بدون بررسی روز)
def get_persian_zodiac(birthdate):
    """
    ورودی: birthdate به صورت 'YYYY/MM/DD' (مثلاً '۱۳۸۵/۰۳/۱۹' یا '1385/03/19')
    خروجی: یک رشته شامل نام ماه شمسی و نماد (مثلاً 'خرداد ♊️')
    اگر فرمت اشتباه باشد، 'نامشخص' برگردانده می‌شود.
    """
    try:
        parts = birthdate.split("/")
        if len(parts) != 3:
            return "نامشخص"
        month = int(parts[1])
        zodiac_map = {
            1: "فروردین ♈️",
            2: "اردیبهشت ♉️",
            3: "خرداد ♊️",
            4: "تیر ♋️",
            5: "مرداد ♌️",
            6: "شهریور ♍️",
            7: "مهر ♎️",
            8: "آبان ♏️",
            9: "آذر ♐️",
            10: "دی ♑️",
            11: "بهمن ♒️",
            12: "اسفند ♓️"
        }
        return zodiac_map.get(month, "نامشخص")
    except Exception:
        return "نامشخص"
import re
import random
import google.generativeai as genai
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# 🔑 کلید Gemini
genai.configure(api_key="AIzaSyBy8FiqRNsfgKHBkUu-mFKgNV_aSWdy4e4")

# 🌙 برج‌ها بر اساس تقویم شمسی
def get_persian_zodiac(birthdate):
    try:
        month, day = map(int, birthdate.split("/")[1:])
        if (month == 1 and day >= 1) or (month == 2 and day <= 19):
            return "فروردین ♈️"
        elif (month == 2 and day >= 20) or (month == 3 and day <= 20):
            return "اردیبهشت ♉️"
        elif (month == 3 and day >= 21) or (month == 4 and day <= 20):
            return "خرداد ♊️"
        elif (month == 4 and day >= 21) or (month == 5 and day <= 21):
            return "تیر ♋️"
        elif (month == 5 and day >= 22) or (month == 6 and day <= 22):
            return "مرداد ♌️"
        elif (month == 6 and day >= 23) or (month == 7 and day <= 22):
            return "شهریور ♍️"
        elif (month == 7 and day >= 23) or (month == 8 and day <= 22):
            return "مهر ♎️"
        elif (month == 8 and day >= 23) or (month == 9 and day <= 22):
            return "آبان ♏️"
        elif (month == 9 and day >= 23) or (month == 10 and day <= 22):
            return "آذر ♐️"
        elif (month == 10 and day >= 23) or (month == 11 and day <= 22):
            return "دی ♑️"
        elif (month == 11 and day >= 23) or (month == 12 and day <= 22):
            return "بهمن ♒️"
        elif (month == 12 and day >= 23) or (month == 1 and day <= 20):
            return "اسفند ♓️"
        else:
            return "نامشخص"
    except:
        return "نامشخص"

# 🌟 پرامپت داینامیک با حالت تصادفی
def generate_prompt(zodiac, fal_type):
    mood = random.choice(["مثبت و امیدبخش", "مرموز و عجیب", "هشداردهنده و تلخ", "عاشقانه و شاعرانه", "آرامش‌بخش و معنوی"])
    if fal_type == "روزانه":
        return f"""برای متولد برج {zodiac} یک فال روزانه بنویس.
فال باید {mood} باشد، کمی غیرقابل پیش‌بینی و انسانی.
به احساسات روز، روابط و انرژی سیارات اشاره کن.
فال باید نهایتاً ۴ جمله باشد. زبان فارسی روان و صمیمی داشته باشد."""
    elif fal_type == "تاروت":
        return f"""فرض کن کارت تاروتی برای متولد برج {zodiac} کشیده‌ای.
یک فال تاروت کوتاه و {mood} بنویس.
به نماد کارت و انرژی آن اشاره کن، در نهایت فال باید حداکثر ۴ جمله باشد."""
    else:
        return f"برای متولد {zodiac} یک پیام کوتاه و {mood} بنویس به فارسی."

# 🔮 گرفتن فال از Gemini
def get_fal_from_gemini(zodiac, fal_type):
    model = genai.GenerativeModel("models/gemini-2.0-flash")
    prompt = generate_prompt(zodiac, fal_type)
    response = model.generate_content(
        prompt,
        generation_config={"max_output_tokens": 300}  # سرعت بیشتر، پاسخ کوتاه‌تر
    )
    return response.text.strip()

# 🧭 Telegram handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "✨ به بات فال روزانه خوش اومدی!\n\n"
        "برای شروع تاریخ تولدت رو به شمسی وارد کن (مثلاً ۱۳۸۰/۰۱/۳۱):"
    )

async def get_birthdate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    if not re.match(r"^\d{4}/\d{2}/\d{2}$", text):
        await update.message.reply_text("فرمت تاریخ اشتباهه 😅 لطفاً مثل نمونه بفرست: ۱۳۸۰/۰۱/۳۱")
        return

    context.user_data["birthdate"] = text
    zodiac = get_persian_zodiac(text)
    context.user_data["zodiac"] = zodiac

    keyboard = [["🔮 فال تاروت", "☀️ فال روزانه"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text(f"برج تولد شما: {zodiac} 🌙\nحالا یکی از گزینه‌های زیر رو انتخاب کن:", reply_markup=reply_markup)

async def handle_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    choice = update.message.text
    zodiac = context.user_data.get("zodiac", "نامشخص")

    if "تاروت" in choice:
        fal_text = get_fal_from_gemini(zodiac, "تاروت")
    elif "روزانه" in choice:
        fal_text = get_fal_from_gemini(zodiac, "روزانه")
    else:
        fal_text = "گزینه‌ی نامعتبر انتخاب شد 😅"

    await update.message.reply_text(f"🔮 فال امروز برای متولد {zodiac}:\n\n{fal_text}")

# 🚀 اجرای ربات
def main():
    app = ApplicationBuilder().token("8237285591:AAElQBpguevUsmDG18jr_IEHZJlK0k53RI4").build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.Regex(r"^\d{4}/\d{2}/\d{2}$"), get_birthdate))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_choice))

    print("✅ ربات فال سریع و کوتاه آماده‌ست...")
    app.run_polling()

if __name__ == "__main__":
    main()
