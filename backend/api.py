from config import GEMINI_API_KEYS, SYSTEM_PROMPT, SECRET_ANSWER
import google.generativeai as genai # pyright: ignore[reportMissingImports]
from google.api_core.exceptions import ResourceExhausted # pyright: ignore[reportMissingImports]

# This keeps track of which key in the list we are currently using
current_key_index = 0

def get_model():
    """Configures the Gemini client with the currently active key."""
    genai.configure(api_key=GEMINI_API_KEYS[current_key_index])
    return genai.GenerativeModel("gemini-2.5-flash")

def generate_with_fallback(prompt):
    """Tries to generate content, rotating keys if a rate limit is hit."""
    global current_key_index
    attempts = 0
    max_attempts = len(GEMINI_API_KEYS)

    # Keep trying until we've tested every single key in the list
    while attempts < max_attempts:
        try:
            model = get_model()
            response = model.generate_content(prompt)
            return response.text
            
        except ResourceExhausted:
            # If the quota is full, switch to the next key in the list
            print(f"Key {current_key_index + 1} exhausted. Switching to next key...")
            current_key_index = (current_key_index + 1) % len(GEMINI_API_KEYS)
            attempts += 1
            
        except Exception as e:
            print(f"API Error: {e}")
            return "[SYSTEM ERROR: Communication link with the Guardian severed.]"

    # If the loop finishes and ALL keys are exhausted:
    return "[SYSTEM WARNING: Cosmic interference detected. All Guardian energy channels are depleted. Please wait 30 seconds.]"

def get_hint(past_chats=None):
    # Format the history so the AI knows what it already said
    history_text = ""
    if past_chats:
        for chat in past_chats:
            history_text += f"User: {chat.user_message}\nGuardian: {chat.bot_response}\n"

    prompt = f"""
{SYSTEM_PROMPT}

The secret word is: {SECRET_ANSWER}

PAST CONVERSATION HISTORY WITH THIS USER:
{history_text}

MODE: HINT MODE
Goal: Give a clearer but still non-trivial hint.
Allowed formats: Riddles, Poems, Encoded clues (Caesar cipher, Morse code), or Structured clues.
Keep it challenging but solvable within thought, not brute force.
Do not be straightforward.

CRITICAL RULE: Look at the PAST CONVERSATION HISTORY. You MUST NOT repeat a hint, riddle, or clue you have already given. Generate a completely new, unique hint  that can help players.
"""
    return generate_with_fallback(prompt)

def chat_with_ai(user_message, past_chats=None):
    
    # Format the history into a readable script for the AI
    history_text = ""
    if past_chats:
        for chat in past_chats:
            history_text += f"User: {chat.user_message}\nGuardian: {chat.bot_response}\n"

    prompt = f"""
    {SYSTEM_PROMPT}

    The secret word is: {SECRET_ANSWER}

    PAST CONVERSATION HISTORY WITH THIS USER:
    {history_text}

    LATEST USER MESSAGE: {user_message}

    MODE: NORMAL MODE
    Goal: React dynamically to the user's input while maintaining the persona.

    Rules for this response:
    1. YES/NO QUESTIONS: If the user asks a direct Yes/No question, answer it clearly but keep it short and in your alien tone.
    2. OPEN QUESTIONS & HINTS: If the user makes a wrong guess or asks an open-ended question, continue the cosmic narrative. 
    3. CONTEXT: Remember what you have already told them in the PAST CONVERSATION HISTORY. Do not repeat the exact same riddles.

    Respond appropriately.
    """
    return generate_with_fallback(prompt)