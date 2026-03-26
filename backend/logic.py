from config import SECRET_ANSWER

def process_input(user_input, current_points):
    user_input_clean = user_input.lower().strip()

    # Correct guess
    if user_input_clean == SECRET_ANSWER:
        return {
            "type": "correct",
            "message": "CORRECT. YOU HAVE EARNED THE CORE.",
            "points": current_points
        }

    words = user_input_clean.split()

    # If it's a short, wrong guess
    if len(words) <= 2:
        new_points = max(0, current_points - 1)

        if new_points == 0:
            return {
                "type": "game_over",
                "message": " YOU FAILED. EARTH HAS BEEN DESTROYED.",
                "points": 0
            }

        return {
            "type": "wrong",
            "message": "INCORRECT GUESS.",
            "points": new_points
        }

    # Otherwise => full conversation
    return {
        "type": "chat"
    }