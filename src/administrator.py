import discord
from discord import app_commands


def setup(naf):
    @naf.tree.command(name="msg", description="Send a private message to a user.")
    @app_commands.checks.has_permissions(administrator=True)
    async def msg(interaction: discord.Interaction, user: discord.User, message: str):
        try:
            await user.send(message)
            await interaction.response.send_message(
                f"Message sent to {user.mention}.", ephemeral=True
            )
        except discord.Forbidden:
            await interaction.response.send_message(
                f"Could not send a message to {user.mention}. They might have DMs disabled.",
                ephemeral=True,
            )

    @naf.tree.command(name="guide", description="Send a guide message to a user.")
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
                await interaction.response.send_message(
                    f"Guide message sent to {user.mention}.", ephemeral=True
                )
            else:
                await interaction.user.send(guide_message)
                await interaction.response.send_message(
                    "Guide message sent to you.", ephemeral=True
                )
        except discord.Forbidden:
            if user:
                await interaction.response.send_message(
                    f"Could not send a message to {user.mention}. They might have DMs disabled.",
                    ephemeral=True,
                )
            else:
                await interaction.response.send_message(
                    "Could not send a message to you. You might have DMs disabled.",
                    ephemeral=True,
                )

    async def handle_command_error(
        interaction: discord.Interaction, error: app_commands.AppCommandError
    ):
        if isinstance(error, app_commands.MissingPermissions):
            await interaction.response.send_message(
                "You do not have permission to use this command.", ephemeral=True
            )

    msg.error(handle_command_error)
    guide.error(handle_command_error)
