from flask import Flask, render_template, request, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from celery import Celery
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = '491f66ea21948906630a977ff223b779279917cfb8b84d39'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://whitefly_user:whitefly_pass@localhost/whitefly_flask'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

import main
