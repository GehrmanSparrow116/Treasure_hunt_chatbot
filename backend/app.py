# from fastapi import FastAPI, Depends # pyright: ignore[reportMissingImports]
# from sqlalchemy.orm import Session # pyright: ignore[reportMissingImports]
# from database import SessionLocal, engine
# import models
# from auth import create_user, authenticate_user
# from api import get_hint, chat_with_ai
# from logic import process_input
# from config import SCENARIO
# from fastapi.middleware.cors import CORSMiddleware # pyright: ignore[reportMissingImports]

# models.Base.metadata.create_all(bind=engine)

# app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# @app.get("/")
# def home():
#     return {"message": " Alien Riddle Game Backend Running"}

# @app.get("/start")
# def start_game():
#     return {
#         "scenario": SCENARIO
#     }

# @app.post("/register")
# def register(username: str, password: str, db: Session = Depends(get_db)):
#     return create_user(db, username, password)

# @app.post("/login")
# def login(username: str, password: str, db: Session = Depends(get_db)):
#     user = authenticate_user(db, username, password)

#     if not user:
#         return {"error": "Invalid credentials"}

#     return {
#         "message": "Login successful",
#         "user_id": user.id
#     }

# # --- THE CHAT ENDPOINT ---
# @app.post("/chat")
# def chat(user_id: int, message: str, db: Session = Depends(get_db)):
#     user = db.query(models.User).filter(models.User.id == user_id).first()

#     if not user:
#         return {"error": "User not found"}

#     result = process_input(message, user.points)

#     if result["type"] == "correct":
#         user.points = result["points"]
#         db.commit()
#         return {
#             "status": "correct",
#             "message": result["message"],
#             "points": user.points
#         }

#     if result["type"] == "game_over":
#         user.points = 0
#         db.commit()
#         return {
#             "status": "game_over",
#             "message": result["message"],
#             "points": 0
#         }

#     if result["type"] == "wrong":
#         user.points = result["points"]
#         db.commit()
#         return {
#             "status": "wrong",
#             "reply": result["message"],
#             "points": user.points
#         }

# # ---------------- CONVERSATION ----------------
#     if result["type"] == "chat":
#         # Fetch ONLY this specific user's chat history securely
#         # Fetch ONLY the last 10 messages to prevent token explosion
#         past_chats = db.query(models.ChatHistory)\
#                        .filter(models.ChatHistory.user_id == user_id)\
#                        .order_by(models.ChatHistory.id.desc())\
#                        .limit(10).all()
#         # Put them back in chronological order for the AI to read properly
#         past_chats.reverse()
        
#         # Pass the history to the AI function
#         reply = chat_with_ai(message, past_chats)

#         user.points = max(0, user.points - 1)
#         db.commit()

#         # Save the new interaction
#         chat_entry = models.ChatHistory(
#             user_id=user_id,
#             user_message=message,
#             bot_response=reply
#         )
#         db.add(chat_entry)
#         db.commit()

#         return {
#             "status": "chat",
#             "reply": reply,
#             "points": user.points
#         }

# # --- THE BRAND NEW HINT ENDPOINT ---
# @app.post("/hint")
# def trigger_hint(user_id: int, db: Session = Depends(get_db)):
#     user = db.query(models.User).filter(models.User.id == user_id).first()

#     # NEW: Check if they are dead or too poor
#     if user.points <= 0:
#         return {"status": "game_over", "reply": "YOU FAILED. EARTH HAS BEEN DESTROYED.", "points": 0}
#     if user.points < 10:
#         return {"status": "wrong", "reply": "Insufficient cosmic energy for a direct hint.", "points": user.points}

#     # 1. Fetch only recent history so we don't repeat hints and save tokens
#     past_chats = db.query(models.ChatHistory)\
#                    .filter(models.ChatHistory.user_id == user_id)\
#                    .order_by(models.ChatHistory.id.desc())\
#                    .limit(10).all()
#     past_chats.reverse()

#     # 2. Pass the history to the AI
#     hint_text = get_hint(past_chats)
    
#     # 3. Deduct the points
#     user.points = max(0, user.points - 10) 
    
#     # 4. SAVE THE HINT TO THE DATABASE so the AI remembers saying it!
#     chat_entry = models.ChatHistory(
#         user_id=user_id,
#         user_message="[Player requested a dedicated hint]",
#         bot_response=hint_text
#     )
#     db.add(chat_entry)
#     db.commit()

#     return {
#         "status": "hint",
#         "reply": hint_text,
#         "points": user.points
#     }


from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models
from auth import create_user, authenticate_user
from api import get_hint, chat_with_ai
from logic import process_input
from config import SCENARIO, RIDDLE_1, RIDDLE_2
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def home():
    return {"message": " Alien Riddle Game Backend Running"}


# @app.post("/register")
# def register(username: str, password: str, db: Session = Depends(get_db)):
#     return create_user(db, username, password)


# @app.post("/login")
# def login(username: str, password: str, db: Session = Depends(get_db)):
#     user = authenticate_user(db, username, password)

#     if not user:
#         return {"error": "Invalid credentials"}

#     return {
#         "message": "Login successful",
#         "user_id": user.id
#     }

@app.post("/register")
def register(username: str, password: str, db: Session = Depends(get_db)):
    return create_user(db, username, password)

@app.post("/login")
def login(username: str, password: str, db: Session = Depends(get_db)):
    user = authenticate_user(db, username, password)

    if not user:
        return {"error": "Invalid credentials"}

    return {
        "message": "Login successful",
        "user_id": user.id
    }


@app.get("/start")
def start_game():
    return {
        "scenario": SCENARIO,
        "riddle": RIDDLE_1
    }


@app.post("/chat")
def chat(user_id: int, message: str, db: Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        return {"status": "error", "reply": "User not found."}

    user_level = getattr(user, "level", 1) or 1

    result = process_input(message, user.points, user_level)

    # LEVEL UP
    if result["type"] == "level_up":
        if hasattr(user, "level"):
            user.level = 2
        db.commit()

        return {
            "status": "level_up",
            "message": result["message"],
            "next_riddle": RIDDLE_2,
            "points": user.points
        }

    # FINAL WIN
    if result["type"] == "final_win":
        return {
            "status": "win",
            "message": result["message"],
            "points": user.points
        }

    # WRONG
    if result["type"] == "wrong":
        user.points = result["points"]
        db.commit()

        return {
            "status": "wrong",
            "reply": result["message"],
            "points": user.points
        }

    # GAME OVER
    if result["type"] == "game_over":
        user.points = 0
        db.commit()

        return {
            "status": "game_over",
            "message": result["message"],
            "points": 0
        }

    # CHAT
    if result["type"] == "chat":
        past_chats = db.query(models.ChatHistory)\
            .filter(models.ChatHistory.user_id == user_id)\
            .order_by(models.ChatHistory.id.desc())\
            .limit(10).all()
        past_chats.reverse()

        reply = chat_with_ai(message, user_level, past_chats)

        chat_entry = models.ChatHistory(
            user_id=user_id,
            user_message=message,
            bot_response=reply
        )
        db.add(chat_entry)
        db.commit()

        return {
            "status": "chat",
            "reply": reply,
            "points": user.points
        }


@app.post("/hint")
def hint(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        return {"status": "error", "reply": "User not found."}

    user_level = getattr(user, "level", 1) or 1

    past_chats = db.query(models.ChatHistory)\
        .filter(models.ChatHistory.user_id == user_id)\
        .order_by(models.ChatHistory.id.desc())\
        .limit(10).all()
    past_chats.reverse()

    hint = get_hint(user_level, past_chats)

    user.points = max(0, user.points - 10)
    db.commit()

    return {
        "status": "hint",
        "reply": hint,
        "points": user.points
    }