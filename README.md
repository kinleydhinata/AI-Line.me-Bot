# Line Bot Automation Script

This Python script automates interactions with the LINE application on Windows using the pyautogui library to simulate user actions (e.g., typing and sending messages) and integrates with an AI model via an API from LM Studio to generate responses. The bot listens for commands prefixed with /b (customizable), processes them, and sends back intelligent responses.

Best of all, this solution is completely free ! It leverages open-source tools and libraries, along with your local AI models hosted via LM Studio, ensuring no additional costs for running the bot. Whether you're looking for a personal assistant or a group chat moderator, this script provides a cost-effective way to enhance your LINE chats with AI-powered automation.

---

## Table of Contents

1. [Features](#features)
2. [Prerequisites](#prerequisites)
3. [Installation](#installation)
4. [Configuration](#configuration)
5. [Usage](#usage)
6. [How It Works](#how-it-works)
7. [Setting Up LM Studio](#setting-up-lm-studio)
8. [Contributing](#contributing)
9. [License](#license)

---

## Features

- **Command-Based Interaction**: Responds to messages prefixed with `/b` (Changable).
- **AI-Powered Responses**: Uses an external API to generate intelligent responses using LM Studio.
- **Conversation History**: Maintains a conversation history for each user to provide context-aware responses.
- **Customizable Typing Speed**: Simulates realistic typing behavior.
- **Duplicate Message Handling**: Prevents processing the same message multiple times.
- **Initial Greeting**: Sends an introductory message when the bot starts.
- **Support for Groups and Multi-Chat**: Works in group chats and multi-user conversations (though rapid questions may confuse the bot).

---

## Prerequisites

Before running the script, ensure you have the following installed:

- Python 3.8 or higher
- Required Python libraries:
  - `pyautogui`
  - `pyperclip`
  - `requests`

You can install the required libraries using the following command:

```bash
pip install pyautogui pyperclip requests
```

Additionally, ensure that:
- The **LINE** application is installed and running. You can download it from [here](https://desktop.line-scdn.net/win/new/LineInst.exe).
- The chat interface is open and focused on your screen.
- The API server (e.g., LM Studio) is running at `http://localhost:1234/v1/chat/completions`.

---

## Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/yourusername/AI-Line.me-Bot.git
   cd AI-Line.me-Bot
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

---

## Configuration

The script includes several configurable parameters. You can modify these in the script file:

### API Configuration

- `API_URL`: URL of the API endpoint for generating responses.
- `MAX_TOKENS`: Maximum number of tokens in the response.
- `TEMPERATURE`: Controls randomness of the AI responses (lower = more deterministic).
- `TOP_P`: Controls diversity of the AI responses.
- `STOP_SEQUENCES`: Stops generating text when encountering specific sequences.

### Bot Behavior

- `TYPING_SPEED`: Simulated typing speed in seconds per character.
- `COMMAND_PREFIX`: Prefix for triggering the bot (default: `/b`).
- `INITIAL_GREETING`: The first message sent by the bot.
- `TAB_COUNT`: Number of Tab key presses to focus on the chat input field.
- `REFRESH_INTERVAL`: Time interval (in seconds) between checks for new messages.

### Logging

- Logs are configured to display concise information about the bot's activity.

---

## Usage

1. **Start the API Server**:
   - Ensure your AI model's API server is running at `http://localhost:1234/v1/chat/completions`. 
   - The server must support the OpenAI-compatible API format. If using LM Studio, start the local server and verify it's active.

2. **Prepare the LINE Application**:
   - Open the **LINE** desktop application on your Windows machine.
   - Navigate to the chat where you want to use the bot.
     ![Open](https://github.com/user-attachments/assets/b980d7df-1ec4-496f-a3df-d5d33b5bff28)
   - Right-click on the chat and select **Open in Separate Window**. This ensures the bot can interact without interference from other chats.
   - Click on the **chat bubble panel** (the area displaying the conversation history) **and NOT the chat input box**. This step is crucial because the bot uses the clipboard to detect new messages, and focusing on the chat input box may cause incorrect behavior.

3. **Clear the Clipboard**:
   - Before starting the bot, ensure that your clipboard does not contain any text copied from the chat or elsewhere. 
   - To clear the clipboard, copy an empty space or use a blank text editor to reset it. This prevents the bot from mistakenly processing old or irrelevant data.

4. **Run the Script**:
   - Execute the bot script by running the following command in your terminal:
     ```bash
     python bim.py
     ```
   - After starting the script, the bot will wait for new messages prefixed with `/b` in the chat window.

5. **Interact with the Bot**:
   - Type a message in the chat input box, prefixed with `/b` (e.g., `/b who are you?`), and press Enter.
   - The bot will detect the message, process it through the AI model, and simulate typing the response into the chat input field before sending it.
     ![Capture](https://github.com/user-attachments/assets/fcdb0fbb-2548-4092-b165-158dabd173ec)
     
6. **Important Notes**:
   - Ensure no other applications interfere with the chat window while the bot is running.
   - Avoid rapid consecutive questions in group chats, as this may confuse the bot due to overlapping messages.
   - Keep the chat bubble panel focused and avoid manually typing or interacting with the chat while the bot is active.

By following these steps, you can seamlessly integrate the bot into your LINE chats and enjoy AI-powered interactions!

## How It Works

1. **Message Detection**:
   - The bot periodically checks the chat input field for new messages using `pyautogui` and `pyperclip`.
   - It parses the latest message to extract the username and content.

2. **AI Response Generation**:
   - The bot sends the parsed message to the configured API endpoint.
   - The API generates a response based on the conversation history and returns it.

3. **Response Sending**:
   - The bot simulates typing the response into the chat input field and sends it.

4. **Conversation History**:
   - Each user has their own conversation history stored in memory.
   - This ensures context-aware responses during interactions.

5. **Duplicate Handling**:
   - Messages are marked as processed to prevent duplicate responses.

---

## Setting Up LM Studio

To use this bot with a local AI model, you can set up **LM Studio**, which provides an API-compatible interface for local models.

### Steps to Set Up LM Studio:

1. **Download and Install LM Studio**:
   - Download LM Studio from [here](https://lmstudio.ai/).
   - Install it on your Windows machine.

2. **Download a Local Model**:
   - Open LM Studio and browse the available models.
   - Download a model that suits your needs (e.g., Llama, Mistral, etc.).

3. **Start the Local Server**:
   - In LM Studio, go to the **Local Server** tab.
   - Start the server on `http://localhost:1234` (or another port if needed).
   - Ensure the server is running before starting the bot script.

4. **Configure the Bot**:
   - Update the `API_URL` in the script to match the LM Studio server address (default: `http://localhost:1234/v1/chat/completions`).

5. **Run the Bot**:
   - Follow the instructions in the [Usage](#usage) section to run the bot.

---

Feel free to reach out if you have any questions or suggestions!
