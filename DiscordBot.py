import discord
from discord.ext import commands
from PingPongTool import PingPong
from random import randint
import os

def RandomColor():
    return randint(0, 0xFFFFFF)

Authorization = "Basic a2V5OmUwNzA4ZDkxNDAwYjEzMDM3ZTZmMjc5OWIwYjNkOTRh"
URL = "https://builder.pingpong.us/api/builder/5f8bdb67e4b07b8420a30e71/integration/v0.2/custom/{sessionId}"

bot = commands.Bot(command_prefix=['?', '띵아 '])
Ping = PingPong(URL, Authorization)


@bot.listen()
async def on_command_error(ctx, error):
    if type(error) is commands.errors.CommandNotFound:
        data = await Ping.Pong(ctx.author.id, ctx.message.content, NoTopic=False)
        embed = discord.Embed(
            title="핑퐁",
            description=data['text'],
            color=RandomColor()
        )
        embed.set_footer(text="Using PingPongTool")
        if data['image'] is not None:
            embed.set_image(url=data['image'])
        await ctx.send(embed=embed)


@bot.command(name="따라해")
async def Echo(ctx, *, text: str):
    await ctx.send(text)

discord.client.run(os.environ['token'])
