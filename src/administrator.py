import discord
import os


def setup(bot):
    def available_file(message: str) -> bool:
        message_dir = "config/message/"
        if not os.path.exists(message_dir):
            return False
        files = os.listdir(message_dir)
        message_list = [
            os.path.splitext(file)[0]
            for file in files
            if os.path.isfile(os.path.join(message_dir, file))
        ]
        return message in message_list

    @bot.tree.command(
        name="msg",
        description="Send a private message to a user.",
    )
    async def msg(
        interaction: discord.Interaction,
        user: discord.User,
        message: str,
    ):
        if available_file(message):
            with open(
                f"config/message/{message}.txt",
                "r",
                encoding="utf-8",
            ) as file:
                message = file.read()
        else:
            message = message.replace("\\n", "\n")
        if interaction.user.guild_permissions.administrator:
            try:
                await user.send(message)
                await interaction.response.send_message(
                    f"Message sent to {user.mention}.",
                    ephemeral=True,
                )
            except discord.Forbidden:
                await interaction.response.send_message(
                    f"Could not send a message to {user.mention}. They might have DMs disabled.",
                    ephemeral=True,
                )
        else:
            await interaction.response.send_message(
                "You do not have permission to send this message to other users.",
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
