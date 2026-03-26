from sqlalchemy.orm import Session
from models import User
from passlib.hash import bcrypt

def create_user(db: Session, username, password):
    hashed = bcrypt.hash(password)
    user = User(username=username, password=hashed)
    db.add(user)
    db.commit()
    db.refresh(user)
    return {
    "id": user.id,
    "username": user.username,
    "points": user.points
}

def authenticate_user(db: Session, username, password):
    user = db.query(User).filter(User.username == username).first()
    if user and bcrypt.verify(password, user.password):
        return user
    return None