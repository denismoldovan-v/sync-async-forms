from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Message
from celery import Celery

app = FastAPI(root_path="/fastapi_asgi_nginx")
templates = Jinja2Templates(directory="templates")

# SQLAlchemy
DATABASE_URL = "postgresql://whitefly_user:whitefly_pass@localhost/whitefly_fastapi"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

# Celery
celery = Celery(
    __name__,
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    db = SessionLocal()
    messages = db.query(Message).all()
    db.close()
    return templates.TemplateResponse("index.html", {"request": request, "messages": messages})

@app.get("/create", response_class=HTMLResponse)
def create_form(request: Request):
    return templates.TemplateResponse("create.html", {"request": request})

@app.post("/create")
def create(title: str = Form(...), content: str = Form(...)):
    db = SessionLocal()
    new_msg = Message(title=title, content=content)
    db.add(new_msg)
    db.commit()
    db.close()
    return RedirectResponse(url=request.scope.get('root_path', '') + "/", status_code=303)


@app.get("/create-async", response_class=HTMLResponse)
def create_async_form(request: Request):
    return templates.TemplateResponse("create_async.html", {"request": request})

@app.post("/create-async")
async def create_async_api(title: str = Form(...), content: str = Form(...)):
    if not title or not content:
        return JSONResponse(status_code=400, content={"message": "Missing fields"})
    
    celery.send_task("celery_worker.save_message_async", args=[title, content])
    return JSONResponse(status_code=202, content={"message": "Task queued"})
