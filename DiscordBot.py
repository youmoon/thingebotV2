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

@bot.event
async def on_ready():
    print("준비 완료!")
    game = discord.Game("다시 돌아온 띵이봇! '띵아 [할말]' 명령어로 더 인공지능이 된 띵이봇을 만나보세요!")
    await bot.change_presence(status=discord.Status.online, activity=game)
    
@bot.listen()
async def on_command_error(ctx, error):
    if type(error) is commands.errors.CommandNotFound:
        data = await Ping.Pong(ctx.author.id, ctx.message.content, NoTopic=False)
        embed = discord.Embed(
            title="띵이봇 V.2",
            description=data['text'],
            color=RandomColor()
        )
        embed.set_footer(text="띵이봇 V.2입니다!")
        if data['image'] is not None:
            embed.set_image(url=data['image'])
        await ctx.send(embed=embed)


@bot.command(name="따라해")
async def Echo(ctx, *, text: str):
    await ctx.send(text)

@bot.command(name="hellothisisverification")
async def ping(ctx):
    await ctx.send('애브리띵#2227(694017913723682946)')
    
@bot.command(name="공지")
async def ping(ctx):
    await ctx.send('공지 채널을 설정하려면 채널 이름을 **0띵이봇**으로 시작하세요!')
    
@bot.command(name="초대")
async def ping(ctx):
    await ctx.send('봇의 초대코드 입니다! 도움이 필요하시면 공식 깃헙 이슈 또는 커뮤니티에서 문의 주세요!')
    await ctx.send('> 띵이봇 초대: https://discord.com/oauth2/authorize?client_id=776239926684811314&scope=bot&permissions=515152&redirect_uri=https%3A%2F%2Fanyf.kro.kr%2Fpages%2Fthanks')
    await ctx.send('> 띵이봇 위키: https://github.com/OHvrything/thingebotV2/wiki')
    
@bot.command(name="도움말")
async def ping(ctx):
    await ctx.send('깃헙 띵이봇 위키를 참고하세요!')
    await ctx.send('> 띵이봇 위키: https://github.com/OHvrything/thingebotV2/wiki')

bot.run(os.environ['token'])
