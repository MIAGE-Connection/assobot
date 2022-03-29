from discord.ext import commands

@commands.command(name='del')
async def delete(ctx, *args):
    if (args):
        number = int(args[0])
    else:
        number = 1
    messages = await ctx.channel.history(limit=number + 1).flatten()
    for each_message in messages:
        await each_message.delete()

@commands.command()
async def hello(ctx, *args):
    if (args):
        member = args[0]
    else:
        member = ctx.author.mention
    await ctx.channel.send(f"Hello {member} !")