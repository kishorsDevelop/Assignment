from flask import request, jsonify
from models.notes import Notes
from models.users import Users
from models.share import Share
from app import db, app
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from authenticate import token_required
from ratelimit import limits, sleep_and_retry


@app.route("/")
def hello():
    return "Hello, Welcome to Notes Application!"

@app.route("/api/auth/signup", methods=["POST"])
def signup():
    try:
        username = request.form.get('username')
        password = generate_password_hash(request.form.get('password'))
        user = Users().create(username, password)
        if not user:
            return {
                "message": "User already exists",
                "error": "Conflict"
            }, 409
        return {"message": "Successfully created new user"}, 201

    except Exception as e:
        return {
            "message": "Internal Server Error",
            "error": str(e)
        }, 500

@app.route("/api/auth/login", methods=["POST"])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    user = Users.query.filter_by(username=username).first()
    print(type(user))
    if not user or not check_password_hash(user.password, password):
        return {
            "message": "Error fetching auth token!, invalid username or password",
            "error": "Unauthorized"
        }, 404
    
    try:
        token = jwt.encode(
            {"user_id": user.id},
            app.config["SECRET_KEY"],
            algorithm="HS256"
        )
        return {
            "message": "Successfully fetched auth token",
            "data":
                {
                    "id": user.id,
                    "username": username,
                    "token": "Bearer " + token
                }
            }
    
    except Exception as e:
        return {
            "error": "Something went wrong",
            "message": str(e)
        }, 500

@app.route('/api/notes', methods=['GET', 'POST'])
@token_required
@sleep_and_retry
@limits(calls=10, period=1)
def notes(current_user):
    if request.method == "GET":
        details = db.session.query(Notes, Share).join(Share, Notes.id == Share.notes_id).filter_by(username=current_user).all()
        data = []
        for result in details:
            data.append(
                {
                    'id': result[1].notes_id,
                    'title': result[0].title,
                    'content': result[0].content,
                    'author': result[0].author
                }
            )
        return data, 200
    
    elif request.method == "POST":
        author = current_user
        title = request.form.get('title')
        content = request.form.get('content')
 
        notes_detail = Notes(
            author=author,
            title=title,
            content=content
        )
        db.session.add(notes_detail)
        db.session.commit()
        share_detail = Share(
            notes_id=notes_detail.id,
            username=current_user
        )
        db.session.add(share_detail)
        db.session.commit()
        return "Note added Successfully", 201


@app.route('/api/notes/<id>', methods=['GET', 'DELETE'])
@token_required
@sleep_and_retry
@limits(calls=10, period=1)
def notes_by_id(current_user, id):
    if request.method == "GET":
        details = Notes.query.filter_by(id=id, author=current_user).first()
        if details:
            return jsonify(details), 200
        return "No Details Found", 200

    elif request.method == "DELETE":
        details = Notes.query.filter_by(id=id, author=current_user).delete()
        db.session.commit()
        if details == 1:
            Share.query.filter_by(notes_id=id).delete()
            db.session.commit()
            return "Note Deleted Successfully", 200
        return "Nothing to Delete", 200

@app.route('/api/notes/<id>', methods=['PUT'])
@token_required
@sleep_and_retry
@limits(calls=10, period=1)
def update_notes(current_user, id):
    details = Notes.query.filter_by(id=id, author=current_user).first()
    if details and request.form.get('title'):
        details.title = request.form.get('title')
    if details and request.form.get('content'):
        details.content = request.form.get('content')
    db.session.commit()
    return "Note Updated Successfully", 200


@app.route('/api/notes/<id>/share', methods=['POST'])
@token_required
@sleep_and_retry
@limits(calls=10, period=1)
def share_notes(current_user, id):
    share_detail = Share(
        notes_id=id,
        username=current_user
    )
    db.session.add(share_detail)
    db.session.commit()
    return "Note Shared Successfully", 200

@app.route('/api/search', methods=['GET'])
@token_required
@sleep_and_retry
@limits(calls=10, period=1)
def search_notes(current_user):
    query = request.args.get('q')
    search = "%{}%".format(query)
    notes = Notes.query.filter(Notes.content.like(search), author=current_user).all()
    return jsonify(notes)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=5000, debug=True)