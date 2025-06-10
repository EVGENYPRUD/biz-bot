from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

# === Главное меню ===
keyboard_main = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_main.add(
    KeyboardButton("📦 Открыть витрину")
)
keyboard_main.add(
    KeyboardButton("💳 Оплатить"),
    KeyboardButton("❓ Помощь")
)
keyboard_main.add(
    KeyboardButton("ℹ️ О проекте")
)

# === Инлайн-клавиатура выбора PDF (Free уровень) ===
def pdf_choice_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton("📥 01. 5Ошибок", callback_data='free_01_5Ошибок'),
        InlineKeyboardButton("📄 02. Бизнес-план", callback_data='free_02_Бизнес_план'),
        InlineKeyboardButton("📄 03. Стратегия продаж", callback_data='free_03_Стратегия_продаж'),
        InlineKeyboardButton("📄 04. Как выбрать нишу", callback_data='free_04_Как_выбрать_нишу'),
        InlineKeyboardButton("📄 05. Аватар клиента", callback_data='free_05_Аватар_клиента'),
        InlineKeyboardButton("📄 06. Чек-лист запуска ТГ", callback_data='free_06_Чек_лист_запуска_ТГ')
    )
    keyboard.add(
        InlineKeyboardButton("🔁 Вернуться в меню", callback_data='go_start')
    )
    return keyboard

# === Инлайн-кнопки оплаты ===
def payment_button():
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton("💸 Оплатить Бизнес-план", url="https://t.me/BizPlanHubBot?start=pay_plan"),
        InlineKeyboardButton("💸 Оплатить Стратегию продаж", url="https://t.me/BizPlanHubBot?start=pay_sales")
    )
    return keyboard

# === Витрина BASE ===
def base_pdf_keyboard():
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton("📊 Кофейня (Base)", callback_data='base_coffee'),
        InlineKeyboardButton("📊 Онлайн-курсы (Base)", callback_data='base_courses')
    )
    keyboard.add(
        InlineKeyboardButton("📊 Телеграм-канал (Base)", callback_data='base_tg'),
        InlineKeyboardButton("📊 Маркетплейс (Base)", callback_data='base_marketplace')
    )
    keyboard.add(
        InlineKeyboardButton("📊 Студия дизайна (Base)", callback_data='base_design')
    )
    return keyboard

# === Витрина PRO ===
def pro_pdf_keyboard():
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton("📘 Кофейня Pro+", callback_data='pro_coffee'),
        InlineKeyboardButton("📘 Курсы Pro+", callback_data='pro_courses')
    )
    keyboard.add(
        InlineKeyboardButton("📘 Телеграм-канал Pro+", callback_data='pro_tg'),
        InlineKeyboardButton("📘 Маркетплейс Pro+", callback_data='pro_marketplace')
    )
    keyboard.add(
        InlineKeyboardButton("📘 Дизайн-студия Pro+", callback_data='pro_design')
    )
    return keyboard
