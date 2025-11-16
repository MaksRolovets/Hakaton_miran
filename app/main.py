from fastapi import FastAPI, UploadFile, File, Form, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse
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
class SendGrph(BaseModel):
    id: int
    inspector: Optional[str] = None
    department: Optional[str] = None
    scheduled_date: str
    start_time: str
    end_time: str
    status: str
    notes: str | None = None

class Sendn8nput(BaseModel):
    id: int
    inspector: Optional[str] = None
    department: Optional[str] = None
    scheduled_date: str
    start_time: str
    end_time: str
    status: str
    notes: str | None = None
    message: Optional[str] = None  # Добавьте это поле

class PostGrph(BaseModel):

    inspector: str
    department: str
    scheduled_date: str
    start_time: str
    end_time: str
    status: str
    notes: str | None = None

class ChangeInspectorIn(BaseModel):
    schedule_id: int
    new_inspector_name: str

class RescheduleIn(BaseModel):
    schedule_id: int
    new_date: str   # "YYYY-MM-DD"

# Настраиваем шаблоны
templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="D:\\хакатон\\app\\static"), name="static") # директория css

# Главная страница
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request":request})

@app.get("/landing", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("landing3.html", {"request": request})

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.get("/sched", response_class=HTMLResponse)
async def shedul(request : Request):
    return templates.TemplateResponse("test.html", {"request": request})



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
    s.scheduled_date::text as scheduled_date,
    s.start_time::text as start_time,
    d.name as department_name,
    s.notes
FROM schedules s
LEFT JOIN users u ON s.inspector_id = u.id
LEFT JOIN departments d ON s.department_id = d.id
WHERE s.scheduled_date BETWEEN CURRENT_DATE AND CURRENT_DATE + INTERVAL '7 days'
  AND s.status = 'planned'
  AND u.contact_info IS NOT NULL
ORDER BY s.scheduled_date, s.start_time LIMIT 2;"""
        try:
            result = await database.fetch_all(query=query)
        except:
            raise HTTPException(status_code=500, detail="Ошибка из базы")
        data_json =  [Sendn8n(**dict(record)).model_dump(mode='json') 

# поинт для бд
        for record in result]
        response = await client.post("https://n8nsmartmarketing.sellsystems.agency/webhook/inspections", json={"qw":data_json})
    return {"status": response.status_code}

#поинт для графика
@app.get("/schedules")
async def get_shedules():
    query="""SELECT 
    s.id,
    u.full_name as inspector,
    d.name as department,
    s.scheduled_date::text ,
    COALESCE(s.start_time::text, '') as start_time,  -- преобразуем NULL в пустую строку
    COALESCE(s.end_time::text, '') as end_time,  
    s.status,
    s.notes
    FROM schedules s
    LEFT JOIN users u ON s.inspector_id = u.id
    LEFT JOIN departments d ON s.department_id = d.id
    WHERE s.scheduled_date BETWEEN CURRENT_DATE AND CURRENT_DATE + INTERVAL '7 days'
    ORDER BY s.scheduled_date, s.start_time;"""

    try:
        result = await database.fetch_all(query=query)
    except:
        raise HTTPException(status_code=500, detail="проблема с базой")
    
    data_json = [SendGrph(**dict(record)).model_dump(mode='json') for record in result]
    return data_json

@app.post("/schedules/add")
async def post_schedules(data : PostGrph):
    query = """INSERT INTO schedules (
    inspector_id, 
    department_id, 
    scheduled_date, 
    start_time, 
    end_time, 
    status, 
    notes
)
VALUES (
    (SELECT id FROM users WHERE full_name = :inspector),
    (SELECT id FROM departments WHERE name = :department),
    :scheduled_date::DATE,
    NULLIF(:start_time,'')::TIME,
    NULLIF(:end_time,'')::TIME,
    :status,
    :notes
)
RETURNING id;""" 
    values = {**data.model_dump()}
    try:
        result = await database.execute(query=query, values=values)
    except:
        raise HTTPException(status_code=500, detail="Скорее всего неправильный запрос")
    return result

@app.put("/schedules/change-inspector")
async def update_graph( payload : ChangeInspectorIn):
    check_q = "SELECT id, inspector_id, status FROM schedules WHERE id = :id LIMIT 1;"
    sch = await database.fetch_one(query=check_q, values={"id": payload.schedule_id})
    if not sch:
        raise HTTPException(status_code=404, detail="Проверка не найдена")
    if sch["status"] != "planned":
        raise HTTPException(status_code=400, detail="Можно менять инспектора только для запланированных проверок")
    query = """WITH updated_schedule AS (
    UPDATE schedules 
    SET inspector_id = (
        SELECT id FROM users 
        WHERE full_name = :new_inspector_name
        AND role = 'inspector'
    )
    WHERE id = :schedule_id
    AND status = 'planned'
    RETURNING *
)
SELECT 
    us.id,
    u.full_name as inspector,
    d.name as department,
    us.scheduled_date::text,
    COALESCE(us.start_time::text, '') as start_time,
    COALESCE(us.end_time::text, '') as end_time,
    us.status,
    us.notes,
    'Инспектор успешно изменен' as message
FROM updated_schedule us
LEFT JOIN users u ON us.inspector_id = u.id
LEFT JOIN departments d ON us.department_id = d.id;"""
    
    values = {"schedule_id":payload.schedule_id,"new_inspector_name":payload.new_inspector_name}

    try:
        result = await database.fetch_one(query=query, values=values)
    except:
        raise HTTPException(status_code=500, detail="Поломка в обновлении")
    
    data_json = SendGrph(**dict(result)).model_dump(mode='json')

    async with httpx.AsyncClient() as client:
        response = await client.post("https://n8nsmartmarketing.sellsystems.agency/webhook/inspections", json={"data":data_json, "message":"Пользователь заменен"})
    return result

@app.put("/schedules/reschedule")
async def reschedule_date(schedule_id:int, new_date:str):
    query = """UPDATE schedules 
SET 
    scheduled_date = :new_date::DATE,
    notes = COALESCE(notes, '') || ' Перенесено на :new_date'
WHERE id = :schedule_id
AND status = 'planned'
RETURNING id;"""
    values = {'schedule_id':schedule_id, "new_date":new_date}
    try:
        result = await database.execute(query=query, values=values)
    except:
        raise HTTPException(status_code=500, detail="Поломка в обновлении")
    
    return result