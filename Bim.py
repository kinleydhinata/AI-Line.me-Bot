import time
import pyautogui
import pyperclip
import requests
import logging

# Configure logging for concise output
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
    datefmt="%H:%M:%S"
)

# API Configuration
API_URL = "http://localhost:1234/v1/chat/completions"

# Model Parameters
MAX_TOKENS = 500
TEMPERATURE = 0.8
TOP_P = 1.0
STOP_SEQUENCES = ["\n", "user:", "assistant:"]

# Tweakable Variables
TYPING_SPEED = 0.001  # Typing speed in seconds per character
COMMAND_PREFIX = "/b"  # Command prefix for triggering the bot
INITIAL_GREETING = f"Hello I am Bim, an AI created by Master Lord Kinley! Use {COMMAND_PREFIX} to talk to me. 😊"
INITIAL_GREETING_DELAY = 2  # Delay before sending initial greeting
TAB_COUNT = 2  # Number of Tab presses to focus on chat input
REFRESH_INTERVAL = 0.1  # Time (in seconds) between each refresh/check for new messages

SYSTEM_PROMPT = (
    "Be direct"
)

# Conversation history and processed messages
conversation_history = {}
processed_messages = set()

# Flag to track if the initial greeting has been sent
initial_greeting_sent = False


def chat_with_bot(messages, max_tokens=MAX_TOKENS):
    payload = {
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": TEMPERATURE,
        "top_p": TOP_P,
        "stop": STOP_SEQUENCES
    }
    try:
        response = requests.post(API_URL, json=payload)
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content'].strip()
        else:
            logging.error(f"API Error: {response.status_code}")
            return None
    except Exception as e:
        logging.error(f"API Call Error: {e}")
        return None


def detect_new_message():
    # Focus on the chat input field
    for _ in range(TAB_COUNT):
        pyautogui.press('tab')
        time.sleep(0.1)

    # Select all text in the chat input field
    pyautogui.hotkey('ctrl', 'a')
    time.sleep(0.5)

    # Copy the selected text
    pyautogui.hotkey('ctrl', 'c')
    time.sleep(0.5)

    # Retrieve the copied text
    full_conversation = pyperclip.paste().strip()

    # Log the copied text for debugging
    logging.debug(f"Copied Text: {full_conversation}")

    # Split the conversation into lines
    lines = full_conversation.splitlines()

    # Iterate through the lines in reverse order to find the latest message
    for line in reversed(lines):
        if COMMAND_PREFIX in line and not line.startswith("Bot:") and line not in processed_messages:
            logging.debug(f"Detected New Message: {line}")
            return line.strip()

    return None


def parse_message(message):
    """
    Parses a message into its components: username and content.
    Example input: "23:15 John Bob /b who are you?"
    Example output: ("John Bob", "who are you?")
    """
    # Split the message by spaces to extract the timestamp
    parts = message.split(maxsplit=1)

    if len(parts) < 2:
        return None, None  # Invalid format

    # Extract the timestamp (first part)
    timestamp = parts[0]

    # Find the position of the command prefix ("/b")
    command_start_index = message.find(COMMAND_PREFIX)
    if command_start_index == -1:
        return None, None  # Command prefix not found

    # Extract the username (everything between the timestamp and the command prefix)
    username = message[len(timestamp) + 1:command_start_index].strip()

    # Extract the content (everything after the command prefix)
    content = message[command_start_index + len(COMMAND_PREFIX):].strip()

    return username, content


def send_message(message):
    for _ in range(TAB_COUNT):
        pyautogui.press('tab')
        time.sleep(0.1)
    pyautogui.write(message, interval=TYPING_SPEED)
    pyautogui.press('enter')
    pyautogui.press('tab')


if __name__ == "__main__":
    logging.info("Starting Line bot automation...")
    time.sleep(INITIAL_GREETING_DELAY)
    # Send the initial greeting only once
    if not initial_greeting_sent:
        send_message(INITIAL_GREETING)
        initial_greeting_sent = True
    while True:
        latest_message = detect_new_message()
        if latest_message:
            username, user_input = parse_message(latest_message)
            if not username or not user_input:
                time.sleep(REFRESH_INTERVAL)
                continue
            # Ensure the message hasn't already been processed
            if latest_message in processed_messages:
                logging.info("[INFO] Duplicate message detected. Skipping...")
                time.sleep(REFRESH_INTERVAL)
                continue
            # Log the username and user input
            logging.info(f"User: {username}, Question: {user_input}")
            # Initialize conversation history for the user if not already present
            if username not in conversation_history:
                system_prompt_with_username = SYSTEM_PROMPT.format(username=username)
                conversation_history[username] = [{"role": "system", "content": system_prompt_with_username}]
            # Add the user's input to their conversation history
            conversation_history[username].append({"role": "user", "content": user_input})
            # Get the bot's response
            bot_response = chat_with_bot(conversation_history[username], max_tokens=MAX_TOKENS)
            if bot_response:
                # Log the bot's response
                logging.info(f"Bot Response: {bot_response}")
                send_message(bot_response)
                # Add the bot's response to the conversation history
                conversation_history[username].append({"role": "assistant", "content": bot_response})
                # Mark the message as processed
                processed_messages.add(latest_message)
        time.sleep(REFRESH_INTERVAL)