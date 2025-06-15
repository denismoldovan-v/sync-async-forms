from flask import Flask, render_template, request, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
import os

# === 1. Inicjalizacja aplikacji ===
app = Flask(__name__)
app.config['SECRET_KEY'] = '491f66ea21948906630a977ff223b779279917cfb8b84d3'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://whitefly_user:whitefly_pass@localhost/whitefly_flask'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["DEBUG"] = True

# === 2. Inicjalizacja bazy danych ===
db = SQLAlchemy(app)

# === 3. Inicjalizacja Celery ===
from celery_worker import init_celery, celery
init_celery(app)

# === 4. Import route'ów itd. ===
import main

