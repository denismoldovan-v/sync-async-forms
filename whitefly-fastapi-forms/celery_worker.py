from models import Message, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from celery import Celery

celery = Celery("worker",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)

@celery.task(name="celery_worker.save_message_async")
def save_message_async(title, content):
    try:
        DATABASE_URL = "postgresql://whitefly_user:whitefly_pass@localhost/whitefly_fastapi"
        engine = create_engine(DATABASE_URL)

        SessionLocal = sessionmaker(bind=engine)
        Base.metadata.create_all(bind=engine)

        db = SessionLocal()
        new_msg = Message(title=title, content=content)
        db.add(new_msg)
        db.commit()
        db.close()
        print("Message saved.")
    except Exception as e:
        print(f"ERROR in save_message_async: {e}")
