from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from databases import Database
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://myuser:1234@localhost/MIRAN")
database = Database(DATABASE_URL)

async def lifespan(app: FastAPI):
    await database.connect()
    yield
    await database.disconnect()

app = FastAPI(lifespan=lifespan)

# Монтируем статические файлы (CSS, JS, изображения)
#app.mount("/static", StaticFiles(directory="static"), name="static")



# Главная страница
@app.get("/", response_class=HTMLResponse)
async def read_root():
    return """
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Система чек-листов</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                max-width: 1200px;
                margin: 0 auto;
                padding: 20px;
                background-color: #f5f5f5;
            }
            .header {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 2rem;
                text-align: center;
                border-radius: 10px;
                margin-bottom: 2rem;
            }
            .checklist-card {
                background: white;
                padding: 1.5rem;
                margin: 1rem 0;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            .checklist-card h3 {
                color: #333;
                margin-bottom: 0.5rem;
            }
            .checklist-card p {
                color: #666;
                margin: 0.25rem 0;
            }
            .btn {
                background: #28a745;
                color: white;
                padding: 0.5rem 1rem;
                border: none;
                border-radius: 4px;
                cursor: pointer;
                margin: 0.5rem 0.5rem 0.5rem 0;
            }
            .btn:hover {
                background: #218838;
            }
            .loading {
                text-align: center;
                padding: 2rem;
                color: #666;
            }
            .error {
                background: #f8d7da;
                color: #721c24;
                padding: 1rem;
                border-radius: 4px;
                margin: 1rem 0;
            }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>📋 Система чек-листов</h1>
            <p>Проверка работоспособности базы данных</p>
        </div>

        <div id="loading" class="loading">
            <p>⏳ Загрузка чек-листов...</p>
        </div>

        <div id="checklists-container"></div>
        <div id="error-container" class="error" style="display: none;"></div>

        <script>
            async function loadChecklists() {
                try {
                    const response = await fetch('/api/checklists');
                    const result = await response.json();
                    
                    if (result.status === 'success') {
                        displayChecklists(result.data);
                    } else {
                        showError(result.message);
                    }
                } catch (error) {
                    showError('Ошибка загрузки: ' + error.message);
                }
            }

            function displayChecklists(checklists) {
                const container = document.getElementById('checklists-container');
                const loading = document.getElementById('loading');
                
                loading.style.display = 'none';
                
                if (checklists.length === 0) {
                    container.innerHTML = '<p>Нет доступных чек-листов</p>';
                    return;
                }

                let html = '<h2>Доступные чек-листы:</h2>';
                
                checklists.forEach(checklist => {
                    html += `
                    <div class="checklist-card">
                        <h3>${checklist.name}</h3>
                        <p><strong>ID:</strong> ${checklist.id}</p>
                        <p><strong>Версия:</strong> ${checklist.version}</p>
                        <p><strong>Статус:</strong> ${checklist.is_active ? '✅ Активен' : '❌ Неактивен'}</p>
                        <button class="btn" onclick="viewChecklist(${checklist.id})">
                            👁️ Просмотреть
                        </button>
                    </div>`;
                });

                container.innerHTML = html;
            }

            function viewChecklist(checklistId) {
                alert('Открываем чек-лист ID: ' + checklistId);
                // Здесь будет переход к детальному просмотру
            }

            function showError(message) {
                const loading = document.getElementById('loading');
                const errorContainer = document.getElementById('error-container');
                
                loading.style.display = 'none';
                errorContainer.style.display = 'block';
                errorContainer.innerHTML = `<strong>Ошибка:</strong> ${message}`;
            }

            // Загружаем данные при старте
            document.addEventListener('DOMContentLoaded', loadChecklists);
        </script>
    </body>
    </html>
    """

# API endpoint для получения чек-листов
@app.get("/api/checklists")
async def get_checklists():
    """
    Получение списка чек-листов из БД
    """
    try:
        query = """
            SELECT id, name, version, is_active 
            FROM checklist_templates 
            WHERE is_active = true
            ORDER BY id
        """
        
        results = await database.fetch_all(query)
        
        return {
            "status": "success",
            "message": "Данные успешно загружены",
            "data": results,
            "count": len(results)
        }
    except Exception as e:
        return {
            "status": "error", 
            "message": f"Ошибка базы данных: {str(e)}",
            "data": [],
            "count": 0
        }

# Детальный просмотр чек-листа
@app.get("/api/checklists/{checklist_id}")
async def get_checklist_detail(checklist_id: int):
    """
    Получение детальной информации о чек-листе
    """
    try:
        # Получаем основную информацию
        checklist_query = "SELECT * FROM checklist_templates WHERE id = :id"
        checklist = await database.fetch_one(checklist_query, {"id": checklist_id})
        
        if not checklist:
            return {"status": "error", "message": "Чек-лист не найден"}
        
        # Получаем пункты чек-листа
        items_query = """
            SELECT id, section, seq, criterion, has_violation
            FROM checklist_items 
            WHERE template_id = :template_id
            ORDER BY section, seq
        """
        items = await database.fetch_all(items_query, {"template_id": checklist_id})
        
        return {
            "status": "success",
            "checklist": dict(checklist),
            "items": items,
            "items_count": len(items)
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}