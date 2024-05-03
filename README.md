# Dalle Bot

Dalle Bot is a Telegram bot designed for generating images from text using OpenAI's DALL-E model.

## Prerequisites

Before running the bot, ensure you have the following installed:

- Python 3.9 or higher
- Docker (optional, for containerization)

## Installation

1. Clone this repository to your local machine.
2. Install the required Python packages by running:
    ```
    pip install -r requirements.txt
    ```
3. Optionally, if you're using Docker, build the Docker image:
    ```
    docker build -t dalle-bot .
    ```

## Configuration

1. Obtain API credentials:
    - Telegram bot API key
    - Azure API key and endpoint

2. Replace the placeholders in `Dalle_Bot.py` and `generation.py` with your API keys.

## Usage

To run the bot:

1. Run the `Dalle_Bot.py` script:
    ```
    python3 Dalle_Bot.py
    ```
   Or, if using Docker:
    ```
    docker run -d --name dalle-bot-container dalle-bot
    ```

2. Start a conversation with the bot on Telegram by searching for its username and sending it a message.

3. Follow the bot's prompts to generate images from text.

## Commands

- `/start`: Start the conversation with the bot.
- `/help`: Get help on how to use the bot.
- `Мои изображения`: View the images you have generated.
- `Подписка`: Information on subscription plans.
- `allow_list`: View the access list and remaining requests for users with access.

## File Structure

- `Dalle_Bot.py`: Main script for the Telegram bot.
- `generation.py`: Script for generating images from text using OpenAI's DALL-E model.
- `Dockerfile`: Docker configuration for containerizing the bot.
- `access_list.json`: JSON file to maintain user access and request limits.