import discord
from discord import app_commands


def setup(bot):
    @bot.tree.command(
        name="ip",
        description="IP of the SMP or MINIGAME server.",
    )
    @app_commands.describe(which_server="SMP or MINIGAME")
    @app_commands.choices(
        which_server=[
            app_commands.Choice(name="smp", value="smp"),
            app_commands.Choice(name="minigame", value="minigame"),
        ]
    )
    async def ip(
        interaction: discord.Interaction,
        which_server: str = "smp",
    ):
        if which_server == "smp":
            await interaction.response.send_message(
                f"-> https://discord.com/channels/998500551488708618/1129023879105499177/1130148231553241092"
            )
        elif which_server == "minigame":
            await interaction.response.send_message(
                f"-> https://discord.com/channels/998500551488708618/1267736839976910951/1267743994486718475"
            )
        else:
            await interaction.response.send_message(
                f'Invalid server type. Please choose either "smp" or "minigame".',
                ephemeral=True,
            )

    @bot.tree.command(
        name="smp",
        description="IP of the SMP server.",
    )
    async def smp(interaction: discord.Interaction):
        await ip.callback(interaction, "smp")

    @bot.tree.command(
        name="minigame",
        description="IP of the MINIGAME server.",
    )
    async def minigame(interaction: discord.Interaction):
        await ip.callback(interaction, "minigame")

    @bot.tree.command(
        name="invite",
        description="Invite link of this Discord server.",
    )
    async def invite(interaction: discord.Interaction):
        await interaction.response.send_message(f"-> http://dsc.gg/nafdiscord")
