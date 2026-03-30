# from config import GEMINI_API_KEYS, SYSTEM_PROMPT, SECRET_ANSWER
# import google.generativeai as genai # pyright: ignore[reportMissingImports]
# from google.api_core.exceptions import ResourceExhausted # pyright: ignore[reportMissingImports]

# # This keeps track of which key in the list we are currently using
# current_key_index = 0

# def get_model():
#     """Configures the Gemini client with the currently active key."""
#     genai.configure(api_key=GEMINI_API_KEYS[current_key_index])
#     return genai.GenerativeModel("gemini-2.5-flash")


# def generate_with_fallback(prompt):
#     """Tries to generate content, rotating keys if a rate limit is hit."""
#     global current_key_index
#     attempts = 0
#     max_attempts = len(GEMINI_API_KEYS)

#     # Keep trying until we've tested every single key in the list
#     while attempts < max_attempts:
#         try:
#             model = get_model()
#             response = model.generate_content(prompt)
#             return response.text
            
#         except ResourceExhausted:
#             # If the quota is full, switch to the next key in the list
#             print(f"Key {current_key_index + 1} exhausted. Switching to next key...")
#             current_key_index = (current_key_index + 1) % len(GEMINI_API_KEYS)
#             attempts += 1
            
#         except Exception as e:
#             print(f"API Error: {e}")
#             return "[SYSTEM ERROR: Communication link with the Guardian severed.]"

#     # If the loop finishes and ALL keys are exhausted:
#     return "[SYSTEM WARNING: Cosmic interference detected. All Guardian energy channels are depleted. Please wait 30 seconds.]"

# def get_hint(past_chats=None):
#     # Format the history so the AI knows what it already said
#     history_text = ""
#     if past_chats:
#         for chat in past_chats:
#             history_text += f"User: {chat.user_message}\nGuardian: {chat.bot_response}\n"

#     prompt = f"""
# {SYSTEM_PROMPT}

# The secret word is: {SECRET_ANSWER}

# PAST CONVERSATION HISTORY WITH THIS USER:
# {history_text}

# MODE: HINT MODE
# Goal: Give a clearer but still non-trivial hint.
# Allowed formats: Riddles, Poems, Encoded clues (Caesar cipher, Morse code), or Structured clues.
# Keep it challenging but solvable within thought, not brute force.
# Do not be straightforward.

# CRITICAL RULE: Look at the PAST CONVERSATION HISTORY. You MUST NOT repeat a hint, riddle, or clue you have already given. Generate a completely new, unique hint  that can help players.
# """
#     return generate_with_fallback(prompt)

# def chat_with_ai(user_message, past_chats=None):
    
#     # Format the history into a readable script for the AI
#     history_text = ""
#     if past_chats:
#         for chat in past_chats:
#             history_text += f"User: {chat.user_message}\nGuardian: {chat.bot_response}\n"

#     prompt = f"""
#     {SYSTEM_PROMPT}

#     The secret word is: {SECRET_ANSWER}

#     PAST CONVERSATION HISTORY WITH THIS USER:
#     {history_text}

#     LATEST USER MESSAGE: {user_message}

#     MODE: NORMAL MODE
#     Goal: React dynamically to the user's input while maintaining the persona.

#     Rules for this response:
#     1. YES/NO QUESTIONS: If the user asks a direct Yes/No question, answer it clearly but keep it short and in your alien tone.
#     2. OPEN QUESTIONS & HINTS: If the user makes a wrong guess or asks an open-ended question, continue the cosmic narrative. 
#     3. CONTEXT: Remember what you have already told them in the PAST CONVERSATION HISTORY. Do not repeat the exact same riddles.

#     Respond appropriately.
#     """
#     return generate_with_fallback(prompt)


from config import GEMINI_API_KEYS, SYSTEM_PROMPT, SECRET_ANSWER_1, SECRET_ANSWER_2
import google.generativeai as genai
from google.api_core.exceptions import ResourceExhausted

current_key_index = 0

VALID_GEMINI_API_KEYS = [key for key in GEMINI_API_KEYS if key]


def fallback_guardian_hint(level):
    if level == 1:
        return """I am born where gravity devours even light,
A cosmic abyss where shadows take flight.
I cannot be seen, only inferred by my greed,
Consuming all matter, every star, every seed."""
    return """I am the final word spoken by a titan who has no voice,
A paradox of destruction that leaves creation no choice.
I am neither the silence nor the song, but the breath between,
The architect of dust, unseen, unclean.
From my ruin, the universe dares to dream again,
But to name me is to know the shape of pain."""


def fallback_guardian_chat(level):
    if level == 1:
        return "Seek the cosmic abyss that traps light itself. Speak with precision, not fear."
    return "Think of a stellar ending so bright it reshapes galaxies and seeds the next generation of stars."

def get_model():
    genai.configure(api_key=VALID_GEMINI_API_KEYS[current_key_index])
    return genai.GenerativeModel("gemini-2.5-flash")

def generate_with_fallback(prompt):
    global current_key_index
    attempts = 0
    max_attempts = len(VALID_GEMINI_API_KEYS)

    if max_attempts == 0:
        return None

    while attempts < max_attempts:
        try:
            model = get_model()
            response = model.generate_content(prompt)
            return response.text

        except ResourceExhausted as e:
            print(f"Key exhausted: {e}")
            current_key_index = (current_key_index + 1) % max_attempts
            attempts += 1

        except Exception as e:
            print(f"API Exception: {e}")
            current_key_index = (current_key_index + 1) % max_attempts
            attempts += 1

    return None


def get_secret_definition(level):
    if level == 1:
        return "Definition: 'Oumuamua is the first known interstellar object detected passing through the Solar System. It is highly elongated (cigar-shaped) and tumbling, with an unusual acceleration not caused by gravity (but lacking a visible comet tail)."
    else:
        return "Definition: Perigee is the point in the orbit of the Moon or a satellite at which it is nearest to the Earth. It represents the point of maximum gravitational pull and closest approach."

def generate_initial_riddle(level):
    secret = SECRET_ANSWER_1 if level == 1 else SECRET_ANSWER_2
    definition = get_secret_definition(level)
    
    if level == 1:
        prompt = f"""
{SYSTEM_PROMPT}

Mode: RIDDLE GENERATION MODE - Level 1
Task: Generate an intermediate-level riddle for the secret word: {secret}.
{definition}
The riddle should be exactly 3 to 4 lines long.
Do not reveal the secret word.
Format: Just the riddle text, no other commentary.
"""
    else:
        prompt = f"""
{SYSTEM_PROMPT}

Mode: RIDDLE GENERATION MODE - Level 2 (EXPERT DIFFICULTY)
Task: Generate an extremely vague, cryptic, and abstract riddle for the secret word: {secret}.
{definition}
The riddle should be exactly 5 to 6 lines long.
Rules:
- Do NOT use any obvious astronomical or scientific terminology.
- Use abstract metaphors, paradoxes, and philosophical language.
- The riddle should feel like a puzzle wrapped in poetry — deeply indirect.
- A player should need to think very hard and laterally to solve it.
- Do not reveal the secret word or make it easy to guess.
Format: Just the riddle text, no other commentary.
"""
    
    riddle = generate_with_fallback(prompt)
    if riddle:
        return riddle.strip()
    return fallback_guardian_hint(level) # Use fallback if AI fails


def get_hint(level, past_chats=None):
    history_text = ""
    if past_chats:
        for chat in past_chats:
            history_text += f"User: {chat.user_message}\nGuardian: {chat.bot_response}\n"

    secret = SECRET_ANSWER_1 if level == 1 else SECRET_ANSWER_2
    definition = get_secret_definition(level)

    prompt = f"""
{SYSTEM_PROMPT}

Secret word: {secret}
{definition}

History:
{history_text}

Give a new hint without revealing answer.
"""
    reply = generate_with_fallback(prompt)
    if reply:
        return reply
    return fallback_guardian_hint(level)


def chat_with_ai(user_message, level, past_chats=None):
    history_text = ""
    if past_chats:
        for chat in past_chats:
            history_text += f"User: {chat.user_message}\nGuardian: {chat.bot_response}\n"

    secret = SECRET_ANSWER_1 if level == 1 else SECRET_ANSWER_2
    definition = get_secret_definition(level)

    prompt = f"""
{SYSTEM_PROMPT}

Secret word: {secret}
{definition}

History:
{history_text}

User: {user_message}

Respond intelligently.
"""
    reply = generate_with_fallback(prompt)
    if reply:
        return reply
    return fallback_guardian_chat(level)