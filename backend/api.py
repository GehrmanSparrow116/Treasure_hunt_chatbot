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


from config import FEATHERLESS_API_KEYS, FEATHERLESS_MODEL, SYSTEM_PROMPT, SECRET_ANSWER_1, SECRET_ANSWER_2
from openai import OpenAI

# Keep track of which key in the list we are currently using
current_key_index = 0
VALID_FEATHERLESS_KEYS = [key for key in FEATHERLESS_API_KEYS if key]

def get_client():
    """Returns an OpenAI client initialized with the current active Featherless key."""
    if not VALID_FEATHERLESS_KEYS:
        return None
    return OpenAI(
        base_url="https://api.featherless.ai/v1",
        api_key=VALID_FEATHERLESS_KEYS[current_key_index]
    )

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

import re

def sanitize_response(response):
    """Programmatically removes secret words from the AI response as a fail-safe."""
    if not response:
        return response
    
    # List of all possible secret answers across levels
    secrets = [SECRET_ANSWER_1, SECRET_ANSWER_2]
    
    sanitized = response
    for secret in secrets:
        # Case-insensitive replacement of the secret word with a placeholder
        # We use regex to match word boundaries if possible, but also handle partial matches for safety
        pattern = re.compile(re.escape(secret), re.IGNORECASE)
        sanitized = pattern.sub("[the celestial entity]", sanitized)
    
    return sanitized

def generate_with_fallback(system_message, user_message):
    global current_key_index
    attempts = 0
    max_attempts = len(VALID_FEATHERLESS_KEYS)

    if max_attempts == 0:
        print("Missing FEATHERLESS_API_KEYS")
        return None

    while attempts < max_attempts:
        try:
            client = get_client()
            if not client:
                return None
            
            response = client.chat.completions.create(
                model=FEATHERLESS_MODEL,
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": user_message}
                ],
                temperature=0.2,
                max_tokens=300,
                presence_penalty=0.5,
                frequency_penalty=0.5
            )
            
            raw_content = response.choices[0].message.content
            return sanitize_response(raw_content)

        except Exception as e:
            print(f"Featherless API Exception with Key {current_key_index + 1}: {e}")
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
        user_prompt = f"""
Mode: RIDDLE GENERATION MODE - Level 1
Task: Generate an intermediate-level riddle for the secret word: {secret}.
{definition}
The riddle should be exactly 3 to 4 lines long.
Do not reveal the secret word.
Format: Just the riddle text, no other commentary.
"""
    else:
        user_prompt = f"""
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
    
    riddle = generate_with_fallback(SYSTEM_PROMPT, user_prompt)
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

    user_prompt = f"""
IMPORTANT: DO NOT USE THE WORD '{secret}' IN YOUR RESPONSE.

Secret word: {secret}
{definition}

History:
{history_text}

Give a new hint without revealing answer.
"""
    reply = generate_with_fallback(SYSTEM_PROMPT, user_prompt)
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

    user_prompt = f"""
IMPORTANT: DO NOT USE THE WORD '{secret}' IN YOUR RESPONSE.

Secret word: {secret}
{definition}

History:
{history_text}

User: {user_message}

Respond intelligently.
"""
    reply = generate_with_fallback(SYSTEM_PROMPT, user_prompt)
    if reply:
        return reply
    return fallback_guardian_chat(level)