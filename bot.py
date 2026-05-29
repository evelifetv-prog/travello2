import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import CommandStart

TOKEN = "8055096666:AAG3fes7eHM9AsGyrEssTvbw6Xry4SF4W-U"
ADMIN_ID = 1013483245

bot = Bot(token=TOKEN)
dp = Dispatcher()

# -------------------
# КНОПКИ
# -------------------

start_kb = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Старт")]],
    resize_keyboard=True
)

yes_kb = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Да, хочу 🚀")]],
    resize_keyboard=True
)

card_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Visa 💳"), KeyboardButton(text="MasterCard 💳")]
    ],
    resize_keyboard=True
)

# -------------------
# ДАННЫЕ ПОЛЬЗОВАТЕЛЕЙ
# -------------------
user_data = {}

# -------------------
# /start
# -------------------
@dp.message(CommandStart())
async def start(message: types.Message):
    await message.answer(
        "✨ *Travello*\n\n"
        "💳 Выпуск зарубежных карт\n"
        "🌍 Оплата по всему миру\n\n"
        "Нажми «Старт» 🚀",
        parse_mode="Markdown",
        reply_markup=start_kb
    )

# -------------------
# СТАРТ
# -------------------
@dp.message(lambda m: m.text == "Старт")
async def handle_start(message: types.Message):
    await message.answer(
        "Хочешь оформить зарубежную карту? 💳",
        reply_markup=yes_kb
    )

# -------------------
# НАЧАЛО АНКЕТЫ
# -------------------
@dp.message(lambda m: m.text == "Да, хочу 🚀")
async def start_form(message: types.Message):
    user_data[message.from_user.id] = {}
    await message.answer("Как тебя зовут?")

# -------------------
# АНКЕТА
# -------------------
@dp.message()
async def handle_form(message: types.Message):
    user_id = message.from_user.id

    if user_id not in user_data:
        return

    data = user_data[user_id]

    # ШАГ 1 — ИМЯ
    if "name" not in data:
        data["name"] = message.text
        await message.answer("Из какой ты страны? 🌍")
        return

    # ШАГ 2 — СТРАНА
    if "country" not in data:
        data["country"] = message.text
        await message.answer("Выбери тип карты 💳", reply_markup=card_kb)
        return

    # ШАГ 3 — КАРТА
    if "card" not in data:
        if message.text not in ["Visa 💳", "MasterCard 💳"]:
            await message.answer("Пожалуйста, выбери кнопку ниже 👇")
            return

        data["card"] = message.text

        # -------------------
        # USERNAME / ИМЯ
        # -------------------
        username = message.from_user.username
        user_tag = f"@{username}" if username else message.from_user.full_name

        # -------------------
        # ОТПРАВКА АДМИНУ
        # -------------------
        text = (
            "🔥 *Новая заявка!*\n\n"
            f"👤 Имя: {data['name']}\n"
            f"🌍 Страна: {data['country']}\n"
            f"💳 Карта: {data['card']}\n"
            f"👤 Пользователь: {user_tag}"
        )

        await bot.send_message(ADMIN_ID, text, parse_mode="Markdown")

        await message.answer("✅ Заявка принята! Скоро с тобой свяжутся.")

        del user_data[user_id]

# -------------------
# ЗАПУСК
# -------------------
async def main():
    print("Бот запущен...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())