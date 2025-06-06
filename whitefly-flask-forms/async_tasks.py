from celery_worker import celery
from app import db
from models import Message


@celery.task(name="save_message_async")
def save_message_async(title, content):
    new_message = Message(title=title, content=content)
    db.session.add(new_message)
    db.session.commit()
