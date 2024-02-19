from dataclasses import dataclass
from app import db

@dataclass
class Notes(db.Model):
    id: int
    title: str
    content: str
    author:str 

    __tablename__ = "notes"
 
    id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True)
    title = db.Column(db.String(500), nullable=False)
    content = db.Column(db.String(5000), nullable=False)
    author = db.Column(db.String(500), nullable=False)