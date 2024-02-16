# ChatGPT-Telegram-Bot

This Python script creates a Telegram bot that automatically replies to messages using OpenAI's natural language processing capabilities. The bot listens for messages in a Telegram group and responds to mentions or direct messages addressed to it. It uses the GPT model for generating replies.

## Features

- Automatically responds to messages in a Telegram group or chat room.
- Supports personalized replies based on the sender's prompt.
- Can be enabled or disabled based on user commands.
- Provides basic information about the bot upon request.

## Prerequisites

Before running the script, ensure you have the following set up:
- Python 3.11 environment with required dependencies installed (Telepot, OpenAI).
- Create your own Telegram bot and obtain a token from [@BotFather](https://core.telegram.org/bots).
- [OpenAI](https://platform.openai.com/) API key.

## Configuration

1. Replace the placeholder values for `bot_token` and `api_key` with your Telegram bot token and OpenAI API key, respectively.
2. Set the `current_model` variable to the desired OpenAI model (e.g., gpt-4-0613).
3. Customize the `prompt` variable to define the personality and behavior of the AI.
4. Update `bot_nickname`, `bot_username`, and `group_user_nickname` as needed to match your Telegram bot's details and group settings.

## Usage

1. Run the script using Python: `python3 auto_reply_bot.py &`.
2. Start a conversation with the Telegram bot in your group or send messages directly.
3. Mention the bot's name or use predefined commands to trigger responses.
4. Disable or enable the bot as needed using the provided commands.

## Commands

- `/info`: Get basic information about the bot.
- `/enable_bot`: Enable the bot to start responding to messages.
- `/disable_bot`: Disable the bot to stop responding to messages.
