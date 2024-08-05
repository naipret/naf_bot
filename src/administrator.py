import discord
import os


def setup(bot):
    def available_file(message_content: str) -> bool:
        message_folder = "config/message/"
        if not os.path.exists(message_folder):
            return False
        files = os.listdir(message_folder)
        message_list = [
            os.path.splitext(file)[0]
            for file in files
            if os.path.isfile(os.path.join(message_folder, file))
        ]
        return message_content in message_list

    @bot.tree.command(
        name="msg",
        description="Send a private message to a user.",
    )
    async def msg(
        interaction: discord.Interaction,
        user: discord.User,
        message_content: str,
    ):
        if available_file(message_content):
            with open(
                f"config/message/{message_content}.txt",
                "r",
                encoding="utf-8",
            ) as file:
                message_content = file.read()
        else:
            message_content = message_content.replace("\\n", "\n")
        if interaction.user.guild_permissions.administrator:
            try:
                await user.send(message_content)
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
