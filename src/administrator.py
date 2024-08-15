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
        # Check if the user has administrator permissions
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message(
                "You do not have permission to use this command.",
                ephemeral=True,
            )
            return
        # Check if there are any template files available at config/message/ otherwise it will continue with raw message_content
        if available_file(message_content):
            with open(
                f"config/message/{message_content}.txt",
                "r",
                encoding="utf-8",
            ) as file:
                message_content = file.read()
        else:
            message_content = message_content.replace("\\n", "\n")
        # Send the message to that member
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

    @bot.tree.command(
        name="broadcast",
        description="Send a message to all members in the server.",
    )
    async def broadcast(interaction: discord.Interaction):
        # Check if the user has administrator permissions
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message(
                "You do not have permission to use this command.",
                ephemeral=True,
            )
            return
        # You may have to wait a few minutes
        await interaction.response.send_message(
            "The app may be unresponsive for a few minutes.",
            ephemeral=True,
        )
        # Load the message content from config/message/broadcast.txt
        try:
            with open(
                "config/message/broadcast.txt",
                "r",
                encoding="utf-8",
            ) as file:
                message_content = file.read()
        except FileNotFoundError:
            await interaction.response.send_message(
                "'config/message/broadcast.txt' not found.",
                ephemeral=True,
            )
            return
        # Fetch the server (guild) and its members
        guild = interaction.guild
        if guild is None:
            await interaction.response.send_message(
                "This command can only be used in a server.",
                ephemeral=True,
            )
            return
        # Send the message to all members
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
