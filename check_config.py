import os
import sys
import requests

# === Настройки путей ===
ENV_FILE = ".env"
MAIN_FILE = "mainly/main.py"
KEYBOARDS_FILE = "mainly/keyboards.py"
IMAGES_PATH = "mainly/images"
PDF_BASE_PATH = "mainly/pdf_files"

PDF_SUBFOLDERS = {
    "Free": "1Free",
    "Base": "2Base",
    "Pro": "3Pro",
    "VIP": "4VIP"
}

REQUIRED_IMAGES = [
    "bot_checking_payment.png",
    "bot_congrats_purchase.png",
    "bot_generating.png",
    "bot_help_response.png",
    "bot_thanks_for_payment.png"
]

REQUIRED_PDFS = {
    "Free": [
        "01_5Ошибок.pdf",
        "02_Бизнес_план.pdf",
        "03_Стратегия_продаж.pdf",
        "04_Как_выбрать_нишу.pdf",
        "05_Аватар_клиента.pdf",
        "06_Чек_лист_запуска_ТГ.pdf"
    ],
    "Base": [
        "base_coffee.pdf",
        "base_courses.pdf",
        "base_tg.pdf",
        "base_marketplace.pdf",
        "base_design.pdf"
    ],
    "Pro": [
        "pro_coffee.pdf",
        "pro_courses.pdf",
        "pro_tg.pdf",
        "pro_marketplace.pdf",
        "pro_design.pdf"
    ],
    "VIP": [
        # Добавь сюда нужные файлы при необходимости
    ]
}

# === Общий флаг успешности ===
all_ok = True

def fail(msg):
    global all_ok
    print(f"\n❌ {msg}")
    all_ok = False

def success(msg):
    print(f"✅ {msg}")

# === Проверка .env и токена ===
def check_env_token():
    if not os.path.exists(ENV_FILE):
        fail("Файл .env не найден")
        return None
    with open(ENV_FILE) as f:
        for line in f:
            if line.startswith("BOT_TOKEN="):
                token = line.strip().split("=", 1)[-1]
                if token:
                    success("BOT_TOKEN найден в .env")
                    return token
    fail("BOT_TOKEN не найден в .env")
    return None

def validate_token(token):
    try:
        url = f"https://api.telegram.org/bot{token}/getMe"
        response = requests.get(url)
        if response.status_code == 200 and response.json().get("ok"):
            success("Токен Telegram валиден")
        else:
            fail("Недействительный токен Telegram")
    except Exception as e:
        fail(f"Ошибка при проверке токена: {e}")

# === Проверка файлов ===
def check_file_exists(path, label):
    if not os.path.exists(path):
        fail(f"Файл {label} не найден: {path}")
    else:
        success(f"Файл {label} найден: {path}")

def check_main_file():
    check_file_exists(MAIN_FILE, "main.py")
    if os.path.exists(MAIN_FILE):
        with open(MAIN_FILE) as f:
            lines = f.readlines()
        if len(lines) >= 150:
            success(f"main.py содержит {len(lines)} строк (нормально)")
        else:
            fail(f"main.py содержит слишком мало строк: {len(lines)}")

def check_keyboards():
    check_file_exists(KEYBOARDS_FILE, "keyboards.py")

def check_folders():
    for folder in [IMAGES_PATH, PDF_BASE_PATH, "mainly"]:
        if not os.path.isdir(folder):
            fail(f"Папка не найдена: {folder}")
        else:
            success(f"Папка найдена: {folder}")

def check_images():
    if not os.path.isdir(IMAGES_PATH):
        fail(f"Папка изображений не найдена: {IMAGES_PATH}")
        return
    files = os.listdir(IMAGES_PATH)
    for img in REQUIRED_IMAGES:
        if img in files:
            success(f"Найдено изображение: {img}")
        else:
            fail(f"Нет изображения: {img}")

def check_pdfs():
    for label, subfolder in PDF_SUBFOLDERS.items():
        full_path = os.path.join(PDF_BASE_PATH, subfolder)
        if not os.path.isdir(full_path):
            fail(f"Папка PDF для {label} не найдена: {full_path}")
            continue
        success(f"Папка PDF найдена: {label} → {subfolder}")
        files = os.listdir(full_path)
        for required_file in REQUIRED_PDFS.get(label, []):
            if required_file in files:
                success(f"✅ PDF в {label}: {required_file}")
            else:
                fail(f"❌ Нет PDF в {label}: {required_file}")

# === Точка входа ===
if __name__ == "__main__":
    print("\n🔍 Проверка конфигурации...")
    token = check_env_token()
    if token:
        validate_token(token)
    check_main_file()
    check_keyboards()
    check_folders()
    check_images()
    check_pdfs()

    print("\n📋 Сводка проверки: ")
    if all_ok:
        print("✅ Всё в порядке. Можно запускать бота.")
    else:
        print("❌ Обнаружены ошибки. Запуск main.py остановлен.")
        sys.exit(1)

    print("\n✨ Готов к запуску! Нажимай ▶ Run или пиши в Shell:")
    print("python3 mainly/main.py")