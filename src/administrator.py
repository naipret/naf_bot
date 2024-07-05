import discord
from discord import app_commands


def setup(bot):
    @bot.tree.command(
        name="msg",
        description="Send a private message to a user.",
    )
    async def msg(
        interaction: discord.Interaction,
        user: discord.User,
        message: str,
    ):
        message = message.replace("\n")
        if interaction.user.guild_permissions.administrator:
            try:
                await user.send(message)
                await interaction.response.send_message(
                    f"Guide message sent to {user.mention}.",
                    ephemeral=True,
                )
            except discord.Forbidden:
                await interaction.response.send_message(
                    f"Could not send a message to {user.mention}. They might have DMs disabled.",
                    ephemeral=True,
                )
        else:
            await interaction.response.send_message(
                "You do not have permission to send guide messages to other users.",
                ephemeral=True,
            )

    @bot.tree.command(
        name="guide",
        description="Send a guide message to a user.",
    )
    async def guide(
        interaction: discord.Interaction,
        user: discord.User = None,
    ):
        with open(
            "config/message/guide.txt",
            "r",
            encoding="utf-8",
        ) as file:
            message = file.read()
        if user:
            if interaction.user.guild_permissions.administrator:
                try:
                    await user.send(message)
                    await interaction.response.send_message(
                        f"Guide message sent to {user.mention}.",
                        ephemeral=True,
                    )
                except discord.Forbidden:
                    await interaction.response.send_message(
                        f"Could not send a message to {user.mention}. They might have DMs disabled.",
                        ephemeral=True,
                    )
            else:
                await interaction.response.send_message(
                    "You do not have permission to send guide messages to other users.",
                    ephemeral=True,
                )
        else:
            try:
                await interaction.user.send(message)
                await interaction.response.send_message(
                    "Guide message sent to you.",
                    ephemeral=True,
                )
            except discord.Forbidden:
                await interaction.response.send_message(
                    "Could not send a message to you. You might have DMs disabled.",
                    ephemeral=True,
                )
