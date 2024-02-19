from dataclasses import dataclass
from app import db, app


@dataclass
class Users(db.Model):
    id: int
    username: str

    __tablename__ = "users"
    id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(1000), nullable=False, unique=True)
    

    def create(self, username, password, id=None):
        user = Users.check_user(username)
        if user:
            return 
        user = Users(
            id=id,
            username=username,
            password=password,
        )
        db.session.add(user)
        db.session.commit()
        return user

    def check_user(username):
        try:
            result = Users.query.filter_by(username=username).first()
            print(result)
        except:
            '''table doesnot exist'''
            with app.app_context():
                db.create_all()
            result = None
        return result
    
    def get_by_id(id):
        user = Users.query.filter_by(id=id).first()
        return user.username