import json
import os
import shutil
from datetime import datetime
from typing import List, Dict, Any
from pathlib import Path

from fastapi import FastAPI, UploadFile, File, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel

# --- Базовая настройка ---
app = FastAPI(title="Checklist API")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

# --- Настройка путей ---
BASE_DIR = Path(__file__).parent.parent
SITE_DIR = BASE_DIR / "site"
FORMS_DIR = SITE_DIR / "forms"
REPORTS_DIR = SITE_DIR / "reports"
PHOTOS_DIR = SITE_DIR / "photos"
DEPARTMENTS_FILE = SITE_DIR / "brigada.json"

# Создаем папки, если они не существуют
FORMS_DIR.mkdir(exist_ok=True)
REPORTS_DIR.mkdir(exist_ok=True)
PHOTOS_DIR.mkdir(exist_ok=True)

# --- Модели данных Pydantic ---
class ReportPayload(BaseModel):
    filename: str
    data: Dict[str, Any]

class TemplateData(BaseModel):
    title: str
    classes: List[Dict[str, Any]]

# === ЭНДПОИНТЫ ДЛЯ УПРАВЛЕНИЯ ОТДЕЛЕНИЯМИ ===

@app.get("/api/departments", response_model=List[str])
async def get_departments():
    """Читает и возвращает список отделений из departments.json."""
    if not DEPARTMENTS_FILE.exists():
        with open(DEPARTMENTS_FILE, "w", encoding="utf-8") as f:
            json.dump([], f)
        return []
    try:
        with open(DEPARTMENTS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []

@app.post("/api/departments")
async def save_departments(departments: List[str] = Body(...)):
    """Принимает новый список отделений и перезаписывает departments.json."""
    try:
        with open(DEPARTMENTS_FILE, "w", encoding="utf-8") as f:
            json.dump(departments, f, ensure_ascii=False, indent=2)
        return {"status": "ok", "message": "Список отделений обновлен."}
    except Exception as e:
        return JSONResponse(content={"status": "error", "message": str(e)}, status_code=500)

# === ЭНДПОИНТЫ ДЛЯ РАБОТЫ С ШАБЛОНАМИ (FORMS) ===

@app.get("/api/templates", response_model=List[Dict[str, Any]])
async def get_templates_list():
    """Возвращает список всех доступных шаблонов с их метаданными."""
    if not FORMS_DIR.is_dir():
        return []
    templates = []
    for file_path in FORMS_DIR.glob("*.json"):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            templates.append({
                "filename": file_path.stem,
                "title": data.get("title", file_path.stem),
                "classes_count": len(data.get("classes", [])),
                "last_modified": datetime.fromtimestamp(file_path.stat().st_mtime).isoformat()
            })
        except (json.JSONDecodeError, IOError):
            continue
    return templates

@app.get("/api/templates/{filename}")
async def get_template(filename: str):
    """Возвращает конкретный шаблон по имени файла."""
    file_path = FORMS_DIR / f"{filename}.json"
    if not file_path.exists():
        return JSONResponse(content={"error": "Template not found"}, status_code=404)
    return FileResponse(file_path)

@app.post("/api/templates/{filename}")
async def save_template(filename: str, template_data: TemplateData):
    """Сохраняет или обновляет шаблон формы."""
    file_path = FORMS_DIR / f"{filename}.json"
    try:
        save_data = {
            "title": template_data.title,
            "classes": template_data.classes,
            "last_modified": datetime.now().isoformat()
        }
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(save_data, f, ensure_ascii=False, indent=2)
        return {"status": "ok", "message": f"Шаблон '{filename}.json' сохранен"}
    except Exception as e:
        return JSONResponse(content={"status": "error", "message": str(e)}, status_code=500)

@app.delete("/api/templates/{filename}")
async def delete_template(filename: str):
    """Удаляет шаблон формы."""
    file_path = FORMS_DIR / f"{filename}.json"
    if not file_path.exists():
        return JSONResponse(content={"error": "Template not found"}, status_code=404)
    try:
        file_path.unlink()
        return {"status": "ok", "message": f"Шаблон '{filename}' удален"}
    except Exception as e:
        return JSONResponse(content={"status": "error", "message": str(e)}, status_code=500)

# === ЭНДПОИНТЫ ДЛЯ РАБОТЫ С ОТЧЕТАМИ (REPORTS) ===

@app.post("/api/reports")
async def save_report(payload: ReportPayload):
    """Сохраняет файл отчета в папку с текущей датой."""
    now = datetime.now()
    report_dir = REPORTS_DIR / str(now.year) / f"{now.month:02d}" / f"{now.day:02d}"
    report_dir.mkdir(parents=True, exist_ok=True)
    file_path = report_dir / Path(payload.filename).name
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(payload.data, f, ensure_ascii=False, indent=2)
        return {"status": "ok", "message": "Отчет сохранен."}
    except Exception as e:
        return JSONResponse(content={"status": "error", "message": str(e)}, status_code=500)

# --- НОВЫЙ ЭНДПОИНТ ---
@app.get("/api/reports/{year}/{month}/{day}", response_model=List[str])
async def get_reports_for_date(year: int, month: int, day: int):
    """Возвращает список имен файлов отчетов за указанную дату."""
    report_dir = REPORTS_DIR / str(year) / f"{month:02d}" / f"{day:02d}"
    if not report_dir.is_dir():
        return []
    try:
        return [f.name for f in report_dir.glob("*.json")]
    except Exception:
        return []

# === ЭНДПОИНТЫ ДЛЯ ЗАГРУЗКИ ФАЙЛОВ ===

@app.post("/api/upload-photo")
async def upload_photo(file: UploadFile = File(...)):
    """Загружает фото в папку /photos."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    unique_filename = f"{timestamp}_{file.filename}"
    file_path = PHOTOS_DIR / unique_filename
    try:
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    finally:
        file.file.close()
    return {"url": f"/photos/{unique_filename}"}

# === ЯВНЫЕ МАРШРУТЫ ДЛЯ HTML СТРАНИЦ ===

@app.get("/", include_in_schema=False)
async def root():
    return FileResponse(os.path.join(SITE_DIR, 'index.html'))

@app.get("/constructor.html", include_in_schema=False)
async def constructor_page():
    return FileResponse(os.path.join(SITE_DIR, 'constructor.html'))
    
@app.get("/checklist_filler.html", include_in_schema=False)
async def checklist_filler_page():
    return FileResponse(os.path.join(SITE_DIR, 'checklist_filler.html'))

# --- НОВЫЙ МАРШРУТ ---
@app.get("/reports.html", include_in_schema=False)
async def reports_page():
    return FileResponse(os.path.join(SITE_DIR, 'reports.html'))

# === Монтирование статики ===
# Этот маршрут должен быть в самом конце, чтобы не перекрывать API-эндпоинты
app.mount("/", StaticFiles(directory=SITE_DIR), name="site")