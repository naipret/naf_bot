import discord
import os

MESSAGE_FOLDER = "config/message/"


def setup(bot):
    def available_files() -> list[str]:
        if not os.path.exists(MESSAGE_FOLDER):
            return []
        return [
            os.path.splitext(file)[0]
            for file in os.listdir(MESSAGE_FOLDER)
            if os.path.isfile(os.path.join(MESSAGE_FOLDER, file))
        ]

    def load_message_content(filename: str) -> str:
        try:
            with open(f"{MESSAGE_FOLDER}{filename}.txt", "r", encoding="utf-8") as file:
                return file.read()
        except FileNotFoundError:
            return ""

    async def check_admin_permission(interaction: discord.Interaction) -> bool:
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message(
                "You do not have permission to use this command.",
                ephemeral=True,
            )
            return False
        return True

    @bot.tree.command(
        name="msg",
        description="Send a private message to a user.",
    )
    async def msg(
        interaction: discord.Interaction,
        user: discord.User,
        message_content: str,
    ):
        if not await check_admin_permission(interaction):
            return

        available_messages = available_files()
        if message_content in available_messages:
            message_content = load_message_content(message_content)
        else:
            message_content = message_content.replace("\\n", "\n")

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
        if not await check_admin_permission(interaction):
            return

        await interaction.response.defer(ephemeral=True)

        message_content = load_message_content("broadcast")
        if not message_content:
            await interaction.followup.send(
                f"'{MESSAGE_FOLDER}broadcast.txt' not found.",
                ephemeral=True,
            )
            return

        guild = interaction.guild
        if not guild:
            await interaction.followup.send(
                "This command can only be used in a server.",
                ephemeral=True,
            )
            return

        failed_members = []
        for member in guild.members:
            if not member.bot:
                try:
                    await member.send(message_content)
                except discord.Forbidden:
                    failed_members.append(member.display_name)

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
