import logging
import os
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InputFile, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters import Command
from keyboards import keyboard_main, pdf_choice_keyboard, payment_button, base_pdf_keyboard, pro_pdf_keyboard
from dotenv import load_dotenv

# === Загрузка токена ===
load_dotenv()
API_TOKEN = os.getenv("BOT_TOKEN")

# === Базовая настройка ===
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
logging.basicConfig(level=logging.INFO)

# === Пути ===
BASE_DIR = os.path.dirname(__file__)
IMAGE_DIR = os.path.join(BASE_DIR, "images")
PDF_DIR = os.path.join(BASE_DIR, "pdf_files")
FREE_PDF_DIR = os.path.join(PDF_DIR, "1Free")
BASE_PDF_DIR = os.path.join(PDF_DIR, "2Base")
PRO_PDF_DIR = os.path.join(PDF_DIR, "3Pro")
VIP_PDF_DIR = os.path.join(PDF_DIR, "4VIP")

# === Приветствие ===
@dp.message_handler(commands=["start"])
async def send_welcome(message: types.Message):
    photo = InputFile(os.path.join(IMAGE_DIR, "bot_help_response.png"))
    await bot.send_photo(
        message.chat.id,
        photo=photo,
        caption=(
            "Привет! 🤖\n\n"
            "Я — бот проекта «Бизнес по шаблону».
"
            "Выбери, что тебе интересно — разберёмся вместе:"
        ),
        reply_markup=keyboard_main
    )

# === Основной выбор PDF ===
@dp.message_handler(commands=["files"])
async def show_pdf_options(message: types.Message):
    await message.answer("Выбери PDF-документ:", reply_markup=pdf_choice_keyboard())

@dp.callback_query_handler(lambda c: c.data.startswith("base_"))
async def send_base_pdf(callback_query: types.CallbackQuery):
    path = os.path.join(BASE_PDF_DIR, f"{callback_query.data}.pdf")
    await bot.send_document(callback_query.from_user.id, InputFile(path))

@dp.callback_query_handler(lambda c: c.data.startswith("pro_"))
async def send_pro_pdf(callback_query: types.CallbackQuery):
    path = os.path.join(PRO_PDF_DIR, f"{callback_query.data}.pdf")
    await bot.send_document(callback_query.from_user.id, InputFile(path))

@dp.callback_query_handler(lambda c: c.data.startswith("free_"))
async def send_free_pdf(callback_query: types.CallbackQuery):
    filename = f"{callback_query.data[5:]}.pdf"
    path = os.path.join(FREE_PDF_DIR, filename)
    if os.path.exists(path):
        await bot.send_document(callback_query.from_user.id, InputFile(path))
    else:
        await bot.send_message(callback_query.from_user.id, "❌ Файл не найден.")

# === VIP-анкета ===
class VIPForm(StatesGroup):
    choosing_topics = State()
    waiting_for_note = State()

vip_topics = [
    "Исследование рынка в вашей нише",
    "Анализ конкурентов в вашем городе",
    "Анализ цен на аналогичные товары/услуги",
    "Выявление спроса (по регионам или ЦА)",
    "Оценка каналов продаж в вашем сегменте",
    "Анализ маркетинговых стратегий конкурентов",
    "Сравнительный анализ с западным рынком",
    "Поиск уникального позиционирования",
    "Рекомендации по стартовой стратегии",
    "Оценка рисков и слабых мест",
    "Анализ потенциальной прибыли",
    "Рекомендации по юридической структуре",
    "Подбор каналов рекламы",
    "Выбор подходящей бизнес-модели",
    "План действий на 90 дней"
]

def get_vip_keyboard(selected):
    buttons = []
    for i, topic in enumerate(vip_topics):
        prefix = "✅ " if i in selected else "➕ "
        buttons.append([InlineKeyboardButton(f"{prefix}{topic}", callback_data=f"vip_{i}")])
    buttons.append([InlineKeyboardButton("Готово", callback_data="vip_done")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

@dp.message_handler(commands=["vip"])
async def start_vip_form(message: types.Message, state: FSMContext):
    await state.update_data(selected=set())
    await VIPForm.choosing_topics.set()
    await message.answer("📋 Отметь темы, которые тебе важны:", reply_markup=get_vip_keyboard(set()))

@dp.callback_query_handler(lambda c: c.data.startswith("vip_"), state=VIPForm.choosing_topics)
async def handle_vip_selection(callback_query: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    selected = data.get("selected", set())

    if callback_query.data == "vip_done":
        count = len(selected)
        if count == 0:
            await callback_query.answer("Вы не выбрали ни одной темы.", show_alert=True)
            return

        # Градация цены
        if count == 1:
            price = "от 4.990 ₽"
        elif 2 <= count <= 4:
            price = "от 5.990 ₽"
        elif 5 <= count <= 7:
            price = "от 6.990 ₽"
        elif 8 <= count <= 10:
            price = "от 7.990 ₽"
        elif 11 <= count <= 13:
            price = "от 8.990 ₽"
        else:
            price = "до 9.990 ₽"

        await state.update_data(price=price)
        await bot.send_message(
            callback_query.from_user.id,
            f"📊 Вы выбрали {count} тем(ы). Примерная стоимость: *{price}*

"
            "✏️ Хочешь добавить что-то вручную? Напиши сейчас — я передам это вместе с анкетой.",
            parse_mode="Markdown"
        )
        await VIPForm.waiting_for_note.set()
        return

    topic_id = int(callback_query.data.split("_")[1])
    if topic_id in selected:
        selected.remove(topic_id)
    else:
        selected.add(topic_id)
    await state.update_data(selected=selected)
    await bot.edit_message_reply_markup(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        reply_markup=get_vip_keyboard(selected)
    )

@dp.message_handler(state=VIPForm.waiting_for_note)
async def handle_vip_note(message: types.Message, state: FSMContext):
    data = await state.get_data()
    selected = data.get("selected", set())
    price = data.get("price", "неизвестно")
    note = message.text

    summary = "📩 Анкета VIP от пользователя:

"
    summary += f"Выбранные темы:
"
    for i in selected:
        summary += f"— {vip_topics[i]}
"
    summary += f"
💬 Дополнительно: {note}
"
    summary += f"
💰 Оценка стоимости: {price}"

    await message.answer("✅ Спасибо! Мы получили твою анкету. Скоро свяжемся.")
    await bot.send_message(message.chat.id, summary)
    await state.finish()

# === Fallback ===
@dp.message_handler()
async def fallback(message: types.Message):
    await message.reply("Я пока не понял, что ты хочешь. Нажми кнопку ниже 👇", reply_markup=keyboard_main)

if __name__ == "__main__":
    print("✅ main.py запущен")
    executor.start_polling(dp, skip_updates=True)
