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

naf = Bot(intents=intents)

@naf.event
async def on_ready():
    print("")
    print(f"Your bot {naf.user} is now RUNNING!")
    print(f"Invite link: https://discord.com/api/oauth2/authorize?client_id={naf.user.id}&permissions=8&scope=bot%20applications.commands")
    await naf.change_presence(activity=discord.Game(name="dsc.gg/nafdiscord"))
    print("")

@naf.tree.command(name="ip", description="IP of the Minecraft server.")
async def ip(interaction: discord.Interaction):
    await interaction.response.send_message(f"-> <#1137766486803480686>")

@naf.tree.command(name="invite", description="Invite link of this Discord server.")
async def invite(interaction: discord.Interaction):
    await interaction.response.send_message(f"-> http://dsc.gg/nafdiscord")
    
# @bot.tree.command(name="ping", description="Check the bot's latency.")
# async def ping(interaction: discord.Interaction) -> None:
#     await interaction.response.send_message(f"Pong! {round(bot.latency * 1000)}ms")

@naf.tree.command(name="echo", description="Echoes the user's message.")
async def echo(interaction: discord.Interaction, message: str) -> None:
    await interaction.response.send_message(message)

# @bot.tree.command(name="add", description="Adds two numbers together.")
# async def add(interaction: discord.Interaction, num1: int, num2: int) -> None:
#     await interaction.response.send_message(f"{num1} + {num2} = {num1 + num2}")

# @bot.tree.command(name="subtract", description="Subtracts two numbers.")
# async def subtract(interaction: discord.Interaction, num1: int, num2: int) -> None:
#     await interaction.response.send_message(f"{num1} - {num2} = {num1 - num2}")

# @bot.tree.command(name="multiply", description="Multiplies two numbers.")
# async def multiply(interaction: discord.Interaction, num1: int, num2: int) -> None:
#     await interaction.response.send_message(f"{num1} * {num2} = {num1 * num2}")

# @bot.tree.command(name="divide", description="Divides two numbers.")
# async def divide(interaction: discord.Interaction, num1: int, num2: int) -> None:
#     if num2 == 0:
#         await interaction.response.send_message("Cannot divide by zero.")
#     else:
#         await interaction.response.send_message(f"{num1} / {num2} = {num1 / num2}")

@naf.tree.command(name="guide", description="Send a guide message to a new user.")
@app_commands.checks.has_permissions(administrator=True)
async def guide(interaction: discord.Interaction, user: discord.User = None):
    guide_message = (
        "_Discord: http://dsc.gg/nafdiscord _\n"
        "_Author: <@812886139593687080> _\n\n"
        "# 🎉 CHÀO MỪNG BẠN ĐẾN VỚI NAIPRET AND FRIENDS 🎉\n"
        "Chúng tôi rất vui khi được chào đón bạn đến với cộng đồng **naf**.\n"
        "Dưới đây là một số thông tin hữu ích giúp bạn bắt đầu.\n\n"
        "## 📚 Các thông tin chung 📚\n"
        "- Nội quy -> https://discord.com/channels/998500551488708618/1130707359937871872\n"
        "- Thông báo -> https://discord.com/channels/998500551488708618/1134709980566667334\n"
        "- Cập nhật -> https://discord.com/channels/998500551488708618/1115931700900409384\n"
        "- Góp ý và bình chọn -> https://discord.com/channels/998500551488708618/1114563225300770928\n\n"
        "## 🎮 Chơi tại naf như thế nào 🎮\n"
        "- Ip -> https://discord.com/channels/998500551488708618/1137766486803480686\n"
        "- Hướng dẫn -> https://discord.com/channels/998500551488708618/1129023879105499177\n\n"
        "Bạn có thể DM cho -> <@812886139593687080> nếu cần hỗ trợ trực tiếp.\n"
        "Hoặc tại kênh hỗ trợ -> https://discord.com/channels/998500551488708618/1241614553863946369\n\n"
        "_Chúng tôi hy vọng bạn sẽ có những trải nghiệm tuyệt vời và kỷ niệm đáng nhớ tại đây._\n"
        "_**Chân thành cảm ơn!**_"
    )
    try:
        if user:
            await user.send(guide_message)
            await interaction.response.send_message(f"Guide message sent to {user.mention}.", ephemeral=True)
        else:
            await interaction.user.send(guide_message)
            await interaction.response.send_message("Guide message sent to you.", ephemeral=True)
    except discord.Forbidden:
        if user:
            await interaction.response.send_message(f"Could not send a message to {user.mention}. They might have DMs disabled.", ephemeral=True)
        else:
            await interaction.response.send_message("Could not send a message to you. You might have DMs disabled.", ephemeral=True)

@naf.tree.command(name="msg", description="Send a private message to a user.")
@app_commands.checks.has_permissions(administrator=True)
async def msg(interaction: discord.Interaction, user: discord.User, message: str):
    try:
        await user.send(message)
        await interaction.response.send_message(f"Message sent to {user.mention}.", ephemeral=True)
    except discord.Forbidden:
        await interaction.response.send_message(f"Could not send a message to {user.mention}. They might have DMs disabled.", ephemeral=True)

async def handle_command_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.MissingPermissions):
        await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)

guide.error(handle_command_error)
msg.error(handle_command_error)

@naf.tree.command(name="help", description="Shows this help message.")
async def help(interaction: discord.Interaction):
    embed = discord.Embed(title="Help", description="List of available commands:")
    for command in naf.tree.get_commands():
        embed.add_field(name=f"/{command.name}", value=command.description, inline=False)
    await interaction.response.send_message(embed=embed)

naf.run(token, reconnect = True)
