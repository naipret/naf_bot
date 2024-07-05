import discord


def setup(bot):
    @bot.tree.command(
        name="ip",
        description="IP of the Minecraft server.",
    )
    async def ip(interaction: discord.Interaction):
        await interaction.response.send_message(f"-> <#1137766486803480686>")

    @bot.tree.command(
        name="invite",
        description="Invite link of this Discord server.",
    )
    async def invite(interaction: discord.Interaction):
        await interaction.response.send_message(f"-> http://dsc.gg/nafdiscord")
