# from sqlalchemy import Column, Integer, String, ForeignKey
# from database import Base

# class User(Base):
#     __tablename__ = "users"

#     id = Column(Integer, primary_key=True, index=True)
#     username = Column(String, unique=True, index=True)
#     password = Column(String)
#     points = Column(Integer, default=100)


# class ChatHistory(Base):
#     __tablename__ = "chat_history"

#     id = Column(Integer, primary_key=True, index=True)
#     user_id = Column(Integer, ForeignKey("users.id"))
#     user_message = Column(String)
#     bot_response = Column(String)

from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    points = Column(Integer, default=100)

    # 🔥 NEW
    level = Column(Integer, default=1)


class ChatHistory(Base):
    __tablename__ = "chat_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    user_message = Column(String)
    bot_response = Column(String)