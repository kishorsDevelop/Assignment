from dataclasses import dataclass
from app import db

@dataclass
class Share(db.Model):
    id: int
    notes_id: int
    username: str

    __tablename__ = "share"
 
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    notes_id = db.Column(db.Integer, nullable=False)
    username = db.Column(db.String(50), nullable=False)