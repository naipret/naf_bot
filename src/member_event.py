import discord


async def on_member_join(
    member: discord.Member,
    join_channel_id,
):
    channel = member.guild.get_channel(join_channel_id)
    if channel is not None:
        await channel.send(
            f"{member.mention} | `{member.name}` | `{member.id}` has joined the server!"
        )
    else:
        print(f"Could not find the join channel with ID:", join_channel_id)


async def on_member_remove(
    member: discord.Member,
    leave_channel_id,
):
    channel = member.guild.get_channel(leave_channel_id)
    if channel is not None:
        await channel.send(
            f"{member.mention} | `{member.name}` | `{member.id}` has left the server!"
        )
    else:
        print(f"Could not find the leave channel with ID:", leave_channel_id)
