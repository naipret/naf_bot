import os
import discord
from discord import Intents, Client, Message, Interaction, app_commands

import responses

# Input bot token =======================
file = open("botToken.txt", "r")
token = file.read()
file.close()

# Bot set up ============================
intents: Intents = Intents.default()
intents.message_content = True
client: Client = Client(command_prefix='/', intents=intents)

# If running normally ===================
@client.event
async def on_ready() -> None:
    print(f"{client.user} is now running!")
    print(f"Invite Link: https://discord.com/api/oauth2/authorize?client_id={client.user.id}&permissions=8&scope=bot%20applications.commands")
    await client.change_presence(activity=discord.Game(name="Minecraft"))

# Handling request command ==============
@client.event
async def on_message(message: Message) -> None:
    if message.author == client.user:
        return
    userName: str = str(message.author)
    userMessage: str = str(message.content)
    channel: str = str(message.channel)
    print(f"[{channel}] {userName}: '{userMessage}'")
    await send_message(message, userMessage)

# Handling private messages =============
async def send_message(message: Message, userMessage: str) -> None:
    if (not userMessage):
        print("(Message was empty because intents were not enabled probably)")
        return
    if (is_private := userMessage[0] == '?'):
        userMessage = userMessage[1:]
    try:
        response: str = get_response(userMessage)
        await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as e:
        print(e)

# Handling responses ====================
def get_response(message: str) -> str:
    try:
        return responses.get_response(message)
    except Exception as e:
        print(e)
    
# Main entry point ======================
def main() -> None:
    client.run(token=token)

if __name__ == '__main__':
    main()
