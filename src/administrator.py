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

    @bot.tree.command(
        name="broadcast",
        description="Send a message to all members in the server.",
    )
    async def broadcast(interaction: discord.Interaction):
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message(
                "You do not have permission to use this command.", ephemeral=True
            )
            return

        if available_file(message_content):
            with open(
                f"config/message/broadcast.txt",
                "r",
                encoding="utf-8",
            ) as file:
                message_content = file.read()
        else:
            await interaction.response.send_message(
                f"Message 'broadcast.txt' not found.",
                ephemeral=True,
            )
            return

        guild = interaction.guild
        if guild is None:
            await interaction.response.send_message(
                "This command can only be used in a server.",
                ephemeral=True,
            )
            return

        failed_members = []
        for member in guild.members:
            try:
                if not member.bot:
                    await member.send(message_content)
            except discord.Forbidden:
                failed_members.append(member.display_name)

        if failed_members:
            await interaction.response.send_message(
                f"Message sent, but failed to reach: {', '.join(failed_members)}",
                ephemeral=True,
            )
        else:
            await interaction.response.send_message(
                "Message sent to all members successfully!",
                ephemeral=True,
            )
