from tkinter import INSERT
from models import db
from app import app

db.drop_all()
db.create_all()
