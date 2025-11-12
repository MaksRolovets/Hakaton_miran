from fastapi import FastAPI, UploadFile, File, Form, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List, Optional
import json, os
from datetime import datetime

app = FastAPI(title="Checklist API (без БД)")

# Разрешаем фронтенду обращаться к API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Папка для фото
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

class ChecklistItem(BaseModel):
    item_id: str
    result: Optional[str]
    comment: Optional[str]
    photos: List[str] = []

class ChecklistCreate(BaseModel):
    form_id: str
    date: str
    inspector_id: int
    department_id: int
    items: List[ChecklistItem]


# Монтируем статические файлы (CSS, JS, изображения)
#app.mount("/static", StaticFiles(directory="static"), name="static")

# Настраиваем шаблоны
templates = Jinja2Templates(directory="app/templates")

# Главная страница
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/landing", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("landing3.html", {"request": request})

# Страница Формы 1
# @app.get("/form1", response_class=HTMLResponse)
# async def form1_page(request: Request):
#     return templates.TemplateResponse("form1.html", {"request": request})

# # Страница Формы 2
# @app.get("/form2", response_class=HTMLResponse)
# async def form2_page(request: Request):
#     return templates.TemplateResponse("form2.html", {"request": request})

# # Страница Формы 3
# @app.get("/form3", response_class=HTMLResponse)
# async def form3_page(request: Request):
#     return templates.TemplateResponse("form3.html", {"request": request})

# # Страница результатов
# @app.get("/results", response_class=HTMLResponse)
# async def results_page(request: Request):
#     return templates.TemplateResponse("results.html", {"request": request})
@app.post("/api/v1/checklists")
async def create_checklist(payload: ChecklistCreate):
    """
    Принимает чек-лист с результатами и ссылками на фото.
    Сохраняет всё в JSON-файл в ./uploads/reports/
    """
    reports_dir = os.path.join(UPLOAD_DIR, "reports")
    os.makedirs(reports_dir, exist_ok=True)

    filename = f"report_{payload.form_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    filepath = os.path.join(reports_dir, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(payload.dict(), f, ensure_ascii=False, indent=2)

    return {"status": "ok", "file": f"/uploads/reports/{filename}"}


# ===============================
# 🖼 3. Загрузка одного фото
# ===============================
@app.post("/api/v1/checklists/upload_photo")
async def upload_photo(file: UploadFile = File(...)):
    """
    Загружает фото и возвращает ссылку для вставки в чек-лист.
    """
    filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, filename)
    with open(file_path, "wb") as f:
        f.write(await file.read())

    return {"url": f"/uploads/{filename}"}


@app.post("/v1/n8n/webhook")
async def receive_n8n_webhook(request: Request):
    try:
        data = await request.json()
        
        print("✅ УСПЕШНО ПОЛУЧЕНЫ ДАННЫЕ:")
        print(json.dumps(data, indent=2, ensure_ascii=False))
        
        return {"status": "success", "data": data}
        
    except Exception as e:
        print(f"❌ ОШИБКА: {e}")
        return {"status": "error", "message": "Невалидный JSON"}
    

