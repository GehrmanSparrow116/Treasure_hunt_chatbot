from fastapi import HTTPException
from sqlalchemy.orm import Session
from models import User
from passlib.hash import bcrypt

def create_user(db: Session, username, password):
    existing_user = db.query(User).filter(User.username == username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists. Please choose another one.")

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