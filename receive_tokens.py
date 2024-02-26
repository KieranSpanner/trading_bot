import re
import asyncio
import aiohttp
from telethon import TelegramClient, events
from telethon.errors import SessionPasswordNeededError

# Your Telegram API credentials
api_id = '21541291'  # Replace with your API ID
api_hash = 'af82bfefbea914721c61323256933366'  # Replace with your API hash
phone = '+61402987419'  # Your phone number with the country code

# Initialize the client
client = TelegramClient('session_name', api_id, api_hash)

async def send_address_to_telegram_group(address):
    # First, send the '/buy' command to the Telegram group
    buy_command_message = "/buy"
    await client.send_message('target_telegram_group_name', buy_command_message)

    # Ensure there's a slight delay to maintain order and give the receiving end a moment to process
    await asyncio.sleep(1)  # Adjust the sleep time if necessary

    # Then, send the address as a separate message
    address_message = address
    await client.send_message('target_telegram_group_name', address_message)

@client.on(events.NewMessage(chats='source_chat_identifier'))
async def group_message_handler(event):
    if event.text:
        address = extract_address(event.text)
        if address:
            print("Address found in group:", address)
            await send_address_to_telegram_group(address)

# Function to extract the relevant address
def extract_address(text):
    # Regular expression to match the token address pattern
    token_address_pattern = r'([a-zA-Z0-9]{42,44})'
    match = re.search(token_address_pattern, text)

    if match:
        return match.group(1)  # Return the matched token address

    return None

# Main function
async def main():
    await client.start()
    print("Client Created")

    if not await client.is_user_authorized():
        await client.send_code_request(phone)
        try:
            await client.sign_in(phone, input('Enter the code: '))
        except SessionPasswordNeededError:
            await client.sign_in(password=input('Password: '))

    await client.run_until_disconnected()

# Run the main function
with client:
    client.loop.run_until_complete(main())
