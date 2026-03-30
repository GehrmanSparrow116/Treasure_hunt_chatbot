# from config import SECRET_ANSWER

# def process_input(user_input, current_points):
#     user_input_clean = user_input.lower().strip()

#     # Correct guess
#     if user_input_clean == SECRET_ANSWER:
#         return {
#             "type": "correct",
#             "message": "CORRECT. YOU HAVE EARNED THE CORE.",
#             "points": current_points
#         }

#     words = user_input_clean.split()

#     # If it's a short, wrong guess
#     if len(words) <= 2:
#         new_points = max(0, current_points - 1)

#         if new_points == 0:
#             return {
#                 "type": "game_over",
#                 "message": " YOU FAILED.",
#                 "points": 0
#             }

#         return {
#             "type": "wrong",
#             "message": "INCORRECT GUESS.",
#             "points": new_points
#         }

#     # Otherwise => full conversation
#     return {
#         "type": "chat"
#     }

from config import SECRET_ANSWER_1, SECRET_ANSWER_2

def process_input(user_input, current_points, level):
    user_input_clean = user_input.lower().strip()

    correct_answer = (SECRET_ANSWER_1 if level == 1 else SECRET_ANSWER_2).lower()

    # CORRECT
    if user_input_clean == correct_answer:
        if level == 1:
            return {
                "type": "level_up",
                "message": "CORE STABILIZED. PROCEED TO NEXT PHASE.",
                "points": current_points
            }
        else:
            return {
                "type": "final_win",
                "message": "YOU HAVE MASTERED THE COSMIC SEQUENCE."
                "           Next phase unlocked:\n"
                " "
                "The god of war stands at his post in the cosmic queue.\n"
                " "
                 "The ringed wanderer holds a further station, cold and true.\n"
                 " "
                 "Don't add them. Don't multiply. Don't subtract or divide.\n"
                 " "
                "Simply place them as they stand — the answer hides inside\n",
                " "
                "points": current_points
            }

    # WRONG GUESS
    words = user_input_clean.split()

    if len(words) <= 2:
        new_points = max(0, current_points - 1)

        if new_points == 0:
            return {
                "type": "game_over",
                "message": " YOU FAILED.",
                "points": 0
            }

        return {
            "type": "wrong",
            "message": "INCORRECT GUESS.",
            "points": new_points
        }

    # CHAT
    return {
        "type": "chat"
    }