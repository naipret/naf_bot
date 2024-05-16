import discord
from discord import app_commands
import json

with open("config.json", 'r') as file:
    config = json.load(file)
    token = config["token"]

class Bot(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)
    async def setup_hook(self):
        await self.tree.sync()

intents = discord.Intents.default()
intents.message_content = True

bot = Bot(intents=intents)

@bot.event
async def on_ready():
    # print("")
    # try:
    #     print(f"Synced {len(synced)} commands...")
    #     synced = await bot.tree.sync()
    # except Exception as e:
    #     print(f"Error syncing commands: {e}")
    print("")
    print(f"Your bot {bot.user} is now RUNNING!")
    print(f"Invite link: https://discord.com/api/oauth2/authorize?client_id={bot.user.id}&permissions=8&scope=bot%20applications.commands")
    await bot.change_presence(activity=discord.Game(name="Minecraft"))
    print("")

@bot.tree.command(name="ip", description="IP of the Minecraft server.")
async def ip(interaction: discord.Interaction) -> None:
    await interaction.response.send_message(f"-> <#1137766486803480686>")

@bot.tree.command(name="invite", description="Invite link of this Discord server.")
async def invite(interaction: discord.Interaction) -> None:
    await interaction.response.send_message(f"-> http://dsc.gg/newsvcc")
    
@bot.tree.command(name="ping", description="Check the bot's latency.")
async def ping(interaction: discord.Interaction) -> None:
    await interaction.response.send_message(f"Pong! {round(bot.latency * 1000)}ms")

@bot.tree.command(name="echo", description="Echoes the user's message.")
async def echo(interaction: discord.Interaction, message: str) -> None:
    await interaction.response.send_message(message)

@bot.tree.command(name="add", description="Adds two numbers together.")
async def add(interaction: discord.Interaction, num1: int, num2: int) -> None:
    await interaction.response.send_message(f"{num1} + {num2} = {num1 + num2}")

@bot.tree.command(name="subtract", description="Subtracts two numbers.")
async def subtract(interaction: discord.Interaction, num1: int, num2: int) -> None:
    await interaction.response.send_message(f"{num1} - {num2} = {num1 - num2}")

@bot.tree.command(name="multiply", description="Multiplies two numbers.")
async def multiply(interaction: discord.Interaction, num1: int, num2: int) -> None:
    await interaction.response.send_message(f"{num1} * {num2} = {num1 * num2}")

@bot.tree.command(name="divide", description="Divides two numbers.")
async def divide(interaction: discord.Interaction, num1: int, num2: int) -> None:
    if num2 == 0:
        await interaction.response.send_message("Cannot divide by zero.")
    else:
        await interaction.response.send_message(f"{num1} / {num2} = {num1 / num2}")

@bot.tree.command(name="version", description="Version of the bot.")
async def version(interaction: discord.Interaction) -> None:
    await interaction.response.send_message(f"Version 3.5 (16/05/2024)")

@bot.tree.command(name="help", description="Shows this help message.")
async def help(interaction: discord.Interaction) -> None:
    embed = discord.Embed(title="Help", description="List of available commands:", color=0x00ff00)
    for command in bot.tree.get_commands():
        embed.add_field(name=f"/{command.name}", value=command.description, inline=False)
    await interaction.response.send_message(embed=embed)

bot.run(token)
