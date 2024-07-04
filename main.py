import discord
from discord import app_commands
import json

from src import server
from src import administrator
from src import math

with open("config.json", "r") as file:
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

naf = Bot(intents=intents)


@naf.event
async def on_ready():
    print("")
    print(f"Your bot {naf.user} is now RUNNING!")
    print(
        f"Invite link: https://discord.com/api/oauth2/authorize?client_id={naf.user.id}&permissions=8&scope=bot%20applications.commands"
    )
    print("")
    await naf.change_presence(activity=discord.Game(name="dsc.gg/nafdiscord"))


server.setup(naf)
administrator.setup(naf)
# math.setup(naf)


@naf.tree.command(name="help", description="Shows this help message.")
async def help(interaction: discord.Interaction):
    embed = discord.Embed(
        title="List of all available commands",
        description="Github repo: https://github.com/naipret/naf_bot",
    )
    for command in naf.tree.get_commands():
        embed.add_field(
            name=f"/{command.name}", value=command.description, inline=False
        )
    await interaction.response.send_message(embed=embed)


naf.run(token, reconnect=True)
