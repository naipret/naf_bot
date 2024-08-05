import discord


async def on_member_join(
    member: discord.Member,
    welcome_channel_id,
):
    channel = member.guild.get_channel(welcome_channel_id)
    if channel is not None:
        await channel.send(
            f"{member.mention} | `{member.name}` | `{member.id}` has join the server!"
        )
    else:
        print(f"Could not find the welcome channel with ID:", welcome_channel_id)


async def on_member_remove(
    member: discord.Member,
    goodbye_channel_id,
):
    channel = member.guild.get_channel(goodbye_channel_id)
    if channel is not None:
        await channel.send(
            f"{member.mention} | `{member.name}` | `{member.id}` has left the server!"
        )
    else:
        print(f"Could not find the goodbye channel with ID:", goodbye_channel_id)
