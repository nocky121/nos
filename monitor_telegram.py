from telethon import TelegramClient, events
import requests
import os
import logging
import asyncio

# Configure logging
logging.basicConfig(level=logging.INFO)

# Define your API ID, API hash, and bot token
api_id = '25810549'
api_hash = '695283c8b7c61e2c9726e1b2a5f3beb7'
bot_token = '7492683084:AAEQ-SnTtxtvpG6kIB1GPJDX7-y40rHMa8w'
bot_chat_id = '6735950714'
TARGET_NUMBERS = {24, 72, 216, 648, 1944}
channel_username = 'lottery_9_7'

# Use a unique session name for each instance
session_name = os.environ.get('SESSION_NAME', 'session')

# Ensure the session file is stored in a persistent location
session_file_path = os.path.join('persistent', session_name)

# Create a Telegram client with the unique session name
client = TelegramClient(session_file_path, api_id, api_hash)

# Define the function to send a message to your bot
def send_message_to_bot(text):
    url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
    data = {
        'chat_id': bot_chat_id,
        'text': text
    }
    response = requests.post(url, data=data)
    logging.info(f"Message sent to bot: {text} - Status Code: {response.status_code}")

# Event handler for new messages
@client.on(events.NewMessage(chats=channel_username))
async def my_event_handler(event):
    try:
        message_text = event.message.message
        if any(str(num) in message_text for num in TARGET_NUMBERS):
            message_link = f'https://t.me/{channel_username}/{event.message.id}'
            alert_text = f"Alert: Found message with target number(s) - {message_link}"
            send_message_to_bot(alert_text)
            logging.info(f"Alert sent: {alert_text}")
    except Exception as e:
        logging.error(f"Error processing message: {e}")

# Start the client
async def main():
    try:
        # Ensure that the client starts with the bot token
        await client.start(bot_token=bot_token)
        logging.info('Monitoring started...')
        await client.run_until_disconnected()
    except Exception as e:
        logging.error(f"Error starting client: {e}")

# Run the main coroutine
if __name__ == '__main__':
    try:
        asyncio.run(main())
    except Exception as e:
        logging.error(f"Error running the bot: {e}")
