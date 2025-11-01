import asyncio
from telegram import Bot

async def main():
    bot = Bot("8237285591:AAElQBpguevUsmDG18jr_IEHZJlK0k53RI4")  # ⬅️ اینجا توکن واقعی‌تو بذار
    me = await bot.get_me()
    print(f"🤖 اتصال برقرار شد! ربات: {me.first_name} (username: @{me.username})")

asyncio.run(main())
