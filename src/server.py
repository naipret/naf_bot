import discord


def setup(bot):
    @bot.tree.command(
        name="ip",
        description="IP of the SMP server.",
    )
    async def ip(interaction: discord.Interaction):
        await interaction.response.send_message(
            f"-> https://discord.com/channels/998500551488708618/1129023879105499177/1130148231553241092"
        )

    @bot.tree.command(
        name="minigame",
        description="IP of the MINIGAME server.",
    )
    async def minigame(interaction: discord.Interaction):
        await interaction.response.send_message(
            f"-> https://discord.com/channels/998500551488708618/1267736839976910951/1267743994486718475"
        )

    @bot.tree.command(
        name="invite",
        description="Invite link of this Discord server.",
    )
    async def invite(interaction: discord.Interaction):
        await interaction.response.send_message(f"-> http://dsc.gg/nafdiscord")
