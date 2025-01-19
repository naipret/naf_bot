import discord
import os

MESSAGE_FOLDER = "config/message/"


def setup(bot):
    async def check_admin_permission(interaction: discord.Interaction) -> bool:
        #! Check if the user has administrator permissions; send a message if not
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message(
                "You do not have permission to use this command.",
                ephemeral=True,
            )
            return False
        return True

    def available_files() -> list[str]:
        # Check if the message folder exists; if not, return an empty list
        if not os.path.exists(MESSAGE_FOLDER):
            return []
        return [
            # List all files in the MESSAGE_FOLDER without their extensions
            os.path.splitext(file)[0]
            for file in os.listdir(MESSAGE_FOLDER)
            if os.path.isfile(os.path.join(MESSAGE_FOLDER, file))
        ]

    def load_message_content(filename: str) -> str:
        # Attempt to read the content of a message file; return empty string if not found
        try:
            with open(f"{MESSAGE_FOLDER}{filename}.txt", "r", encoding="utf-8") as file:
                return file.read()
        except FileNotFoundError:
            return ""

    @bot.tree.command(
        name="msg",
        description="Send a private message to a user.",
    )
    async def msg(
        interaction: discord.Interaction,
        user: discord.User,
        message_content: str,
    ):
        #! Check for admin permission before proceeding
        if not await check_admin_permission(interaction):
            return

        available_messages = available_files()
        # If the message content matches a file name, load its content; otherwise, format the message
        if message_content in available_messages:
            message_content = load_message_content(message_content)
        else:
            message_content = message_content.replace("\\n", "\n")

        try:
            # Attempt to send the message to the user
            await user.send(message_content)
            await interaction.response.send_message(
                f"Message sent to {user.mention}.",
                ephemeral=True,
            )
        except discord.Forbidden:
            # Handle the case where the user has DMs disabled
            await interaction.response.send_message(
                f"Could not send a message to {user.mention}. They might have DMs disabled.",
                ephemeral=True,
            )

    @bot.tree.command(
        name="broadcast",
        description="Send a message to all members in the server.",
    )
    async def broadcast(interaction: discord.Interaction):
        #! Check for admin permission before proceeding
        if not await check_admin_permission(interaction):
            return

        await interaction.response.defer(ephemeral=True)

        # Load the broadcast message content; notify if the file is not found
        message_content = load_message_content("broadcast")
        if not message_content:
            await interaction.followup.send(
                f"'{MESSAGE_FOLDER}broadcast.txt' not found.",
                ephemeral=True,
            )
            return

        guild = interaction.guild
        # Ensure the command is used in a server context
        if not guild:
            await interaction.followup.send(
                "This command can only be used in a server.",
                ephemeral=True,
            )
            return

        failed_members = []
        # Attempt to send the broadcast message to all non-bot members
        for member in guild.members:
            if not member.bot:
                try:
                    await member.send(message_content)
                except discord.Forbidden:
                    # Keep track of members who could not receive the message
                    failed_members.append(member.display_name)

        # Notify the user about the success or failure of the broadcast
        if failed_members:
            await interaction.followup.send(
                f"Message sent, but failed to reach: {', '.join(failed_members)}",
                ephemeral=True,
            )
        else:
            await interaction.followup.send(
                "Message sent to all members successfully!",
                ephemeral=True,
            )
