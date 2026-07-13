import asyncio
import os
from aiohttp import web
from aiogram import Bot, Dispatcher, executor, types

# -----------------------------
# Telegram Bot Setup
# -----------------------------
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start(msg: types.Message):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add("🛒 خرید VPN", "📞 پشتیبانی")
    await msg.answer("سلام، به ربات فروش VPN خوش اومدی 🌐", reply_markup=kb)

@dp.message_handler(lambda m: m.text == "🛒 خرید VPN")
async def buy(msg: types.Message):
    text = (
        "پلن‌ها:\n"
        "1️⃣ یک ماهه — 100 تومن\n"
        "2️⃣ سه ماهه — 250 تومن\n\n"
        "برای خرید، مبلغ را کارت‌به‌کارت کنید:\n"
        "💳 شماره کارت: 6037-9917-1234-5678\n\n"
        "بعد از واریز، اسکرین‌شات را ارسال کنید."
    )
    await msg.answer(text)

@dp.message_handler(content_types=['photo'])
async def payment(msg: types.Message):
    await msg.forward(ADMIN_ID)
    await msg.answer("اسکرین‌شات ارسال شد. منتظر تایید ادمین باشید ✔️")

@dp.message_handler(lambda m: m.chat.id == ADMIN_ID and m.reply_to_message)
async def admin_confirm(msg: types.Message):
    if msg.text == "تایید":
        user_id = msg.reply_to_message.forward_from.id
        await bot.send_message(user_id, "پرداخت تایید شد 🎉\nاکانت VPN به زودی ارسال می‌شود.")
    elif msg.text == "رد":
        user_id = msg.reply_to_message.forward_from.id
        await bot.send_message(user_id, "پرداخت رد شد ❌ لطفاً دوباره تلاش کنید.")

@dp.message_handler(lambda m: m.text == "📞 پشتیبانی")
async def support(msg: types.Message):
    await msg.answer("برای پشتیبانی پیام بده: @YourSupportID")


# -----------------------------
# Fake Web Server (Render Trick)
# -----------------------------
async def handle(request):
    return web.Response(text="Bot is running")

app = web.Application()
app.router.add_get("/", handle)


# -----------------------------
# Run both bot + web server
# -----------------------------
async def main():
    loop = asyncio.get_event_loop()

    # Run Telegram bot
    loop.create_task(executor.start_polling(dp, skip_updates=True))

    # Run fake web server
    web.run_app(app, port=8000)


if __name__ == "__main__":
    asyncio.run(main())
