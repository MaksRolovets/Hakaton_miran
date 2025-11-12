from fastapi import FastAPI, UploadFile, File, Form, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from databases import Database
from pydantic import BaseModel
from typing import List, Optional
import json, os
import httpx
from datetime import datetime

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://myuser:1234@localhost/MIRAN")
database = Database(DATABASE_URL)

async def lifespan(app: FastAPI):
    await database.connect()
    yield
    await database.disconnect()

app = FastAPI(title="Checklist API (без БД)", lifespan=lifespan)

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

class Sendn8n(BaseModel):
    id : int
    contact_info : str
    full_name: str
    scheduled_date : str
    start_time : Optional[str]
    department_name : str
    notes : Optional[str]


# Настраиваем шаблоны
templates = Jinja2Templates(directory="app/templates")

# Главная страница
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/landing", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("landing3.html", {"request": request})

@app.post("/api/v1/checklists")
async def create_checklist(payload: ChecklistCreate):
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
    

@app.post("/send-to-n8n")
async def send_to_n8n():
    async with httpx.AsyncClient() as client:
        query = """SELECT 
    s.id,
    u.contact_info,
    u.full_name,
    s.scheduled_date::text as scheduled_date,  -- преобразуем в текст
    s.start_time::text as start_time,          -- преобразуем в текст
    d.name as department_name,                  -- исправлено название
    s.notes
FROM schedules s
LEFT JOIN users u ON s.inspector_id = u.id
LEFT JOIN departments d ON s.department_id = d.id
WHERE s.scheduled_date = CURRENT_DATE + INTERVAL '1 day'
  AND s.status = 'planned'
  AND u.contact_info IS NOT NULL"""
        try:
            result = await database.fetch_all(query=query)
        except:
            raise HTTPException(status_code=500, detail="Ошибка из базы")
        data_json =  [Sendn8n(**dict(record)).model_dump(mode='json') 
        for record in result]
        response = await client.post("https://kuedogelogep.beget.app/webhook/e64fc03b-2104-4022-bb92-5f0ab36bcd31", json={"qw":data_json})
    return {"status": response.status_code}

# поинт для бд

