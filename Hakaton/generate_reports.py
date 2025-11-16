import json
import os
import random
import copy
from datetime import datetime, timedelta
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

# --- 1. НАСТРОЙКА ПУТЕЙ ---
# Скрипт должен находиться в корневой папке проекта
BASE_DIR = Path(__file__).resolve().parent
SITE_DIR = BASE_DIR / "site"
FORMS_DIR = SITE_DIR / "forms"
REPORTS_DIR = SITE_DIR / "reports"
PHOTOS_DIR = SITE_DIR / "photos"
DEPARTMENTS_FILE = SITE_DIR / "brigada.json"

# --- 2. ПАРАМЕТРЫ ГЕНЕРАЦИИ ---
NUMBER_OF_DAYS = 365 * 2  # Генерируем отчеты на 2 года вперед
SUCCESS_RATE = 0.95  # 95% ответов будут "Соответствует"

# Список случайных комментариев для несоответствий
FAILURE_COMMENTS = [
    "Обнаружена утечка масла.",
    "Требуется срочный ремонт крепления.",
    "Сильное загрязнение, необходима чистка.",
    "Поврежден защитный кожух.",
    "Отсутствует маркировка.",
    "Нарушение техники безопасности.",
]

# --- 3. ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ---

def create_dummy_photo(date_str: str, question_id: str) -> str:
    """Создает фиктивное изображение и возвращает его имя."""
    PHOTOS_DIR.mkdir(exist_ok=True)
    
    # Генерируем уникальное имя файла
    timestamp = datetime.now().strftime("%H%M%S")
    filename = f"{date_str}_{timestamp}_{question_id}.jpg"
    filepath = PHOTOS_DIR / filename

    # Создаем серое изображение
    img = Image.new('RGB', (800, 600), color='grey')
    draw = ImageDraw.Draw(img)

    # Пытаемся загрузить шрифт, если не получится - используем стандартный
    try:
        font = ImageFont.truetype("arial.ttf", 40)
    except IOError:
        font = ImageFont.load_default()

    # Добавляем текст на изображение
    text = f"Фото несоответствия\n{datetime.now().strftime('%Y-%m-%d %H:%M')}"
    draw.text((10, 10), text, fill='white', font=font)
    
    img.save(filepath)
    return filename

def process_questions(questions: list, date_str: str):
    """Рекурсивно обрабатывает список вопросов, добавляя ответы."""
    if not questions:
        return
        
    for question in questions:
        # Симулируем ответ пользователя
        is_success = random.random() < SUCCESS_RATE
        
        if is_success:
            question["userAnswer"] = "Соответствует"
            question["userComment"] = ""
            question["userPhoto"] = None
            question["status"] = "Заполнено"
        else:
            question["userAnswer"] = "Не соответствует"
            # Для несоответствий генерируем фото и комментарий
            photo_filename = create_dummy_photo(date_str, question.get('id', 'unknown_id'))
            question["userPhoto"] = f"FILE:{photo_filename}"
            
            # С вероятностью 80% добавляем комментарий
            if random.random() < 0.8:
                question["userComment"] = random.choice(FAILURE_COMMENTS)
            else:
                question["userComment"] = ""
            
            question["status"] = "Заполнено"

def generate_single_report(template_data: dict, department: str, report_date: datetime) -> dict:
    """Создает один отчет на основе шаблона, отдела и даты."""
    # Глубокое копирование, чтобы не изменять оригинальный шаблон
    report_data = copy.deepcopy(template_data)
    
    # Добавляем метаданные
    report_data["department"] = department
    report_data["completionDate"] = report_date.isoformat()
    
    date_str_for_photo = report_date.strftime("%Y%m%d")

    # Обрабатываем вопросы в классах и подклассах
    for cls in report_data.get("classes", []):
        process_questions(cls.get("questions", []), date_str_for_photo)
        for subcls in cls.get("subclasses", []):
            process_questions(subcls.get("questions", []), date_str_for_photo)
            
    return report_data

# --- 4. ОСНОВНОЙ СКРИПТ ---

def main():
    """Главная функция для запуска генератора."""
    print("--- Запуск генератора отчетов ---")

    # Загружаем шаблоны и список отделений
    try:
        with open(DEPARTMENTS_FILE, "r", encoding="utf-8") as f:
            departments = json.load(f)
        
        templates = {}
        for form_file in FORMS_DIR.glob("*.json"):
            with open(form_file, "r", encoding="utf-8") as f:
                # Используем имя файла без .json как ключ
                templates[form_file.stem] = json.load(f)
                
    except FileNotFoundError as e:
        print(f"Ошибка: Не найден необходимый файл: {e}")
        return
    except json.JSONDecodeError as e:
        print(f"Ошибка: Неверный формат JSON в файле: {e}")
        return

    if not departments or not templates:
        print("Ошибка: Список отделений или папка с шаблонами пусты. Генерация невозможна.")
        return

    print(f"Найдено шаблонов: {len(templates)}")
    print(f"Найдено отделений: {len(departments)}")
    print(f"Генерация отчетов на {NUMBER_OF_DAYS} дней вперед...")

    start_date = datetime.now()
    total_reports = 0

    # Основной цикл по дням
    for day_offset in range(NUMBER_OF_DAYS):
        current_date = start_date + timedelta(days=day_offset)
        
        # Создаем папку для текущего дня
        report_dir = REPORTS_DIR / str(current_date.year) / f"{current_date.month:02d}" / f"{current_date.day:02d}"
        report_dir.mkdir(parents=True, exist_ok=True)
        
        # Цикл по шаблонам
        for template_name, template_content in templates.items():
            # Цикл по отделениям
            for department_name in departments:
                # Генерируем данные для отчета
                report_content = generate_single_report(template_content, department_name, current_date)
                
                # Формируем имя файла
                sane_department_name = department_name.replace(" ", "_")
                date_prefix = current_date.strftime("%d%m%Y")
                filename = f"{date_prefix}_{sane_department_name}_{template_name}.json"
                filepath = report_dir / filename
                
                # Сохраняем JSON-файл отчета
                with open(filepath, "w", encoding="utf-8") as f:
                    json.dump(report_content, f, ensure_ascii=False, indent=2)
                
                total_reports += 1

    print(f"\n--- Генерация завершена! ---")
    print(f"Создано отчетов: {total_reports}")
    print(f"Отчеты сохранены в папке: {REPORTS_DIR}")
    print(f"Фиктивные фото сохранены в папке: {PHOTOS_DIR}")


if __name__ == "__main__":
    main()