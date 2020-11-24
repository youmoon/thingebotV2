import discord
from discord.ext import commands
from PingPongTool import PingPong
from random import randint
import os
import json

def RandomColor():
    return randint(0, 0xFFFFFF)

Authorization = (os.environ['pingpongtoken'])
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
        embed.set_footer(text="띵이봇 입니다!")
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
    embed=discord.Embed(title="공지 채널 설정 방법", description="띵이봇의 공지채널 설정 방법이에요!", color=0x0008ff)
    embed.set_thumbnail(url="https://canary.discord.com/assets/0634b5f01a88a0121bed072779e81bd6.svg")
    embed.add_field(name="1번", value="공지채널로 설정할 채널 이름을 0**띵이봇**으로 시작하세요!", inline=False)
    embed.add_field(name="2번", value="띵이봇 공식 포럼에서 **0띵이봇-공지** 채널을 팔로우하세요!", inline=False)
    embed.add_field(name="1번이 안될때는?", value="띵이봇이 메시지를 보낼 수 있는지 권한을 확인하세요!", inline=True)
    embed.add_field(name="공식 포럼", value="https://discord.gg/nrsVh8EUHE", inline=True)
    embed.set_footer(text="띵이봇! 디스코드를 더욱더 즐겁게!")
    await ctx.send(embed=embed)

    
@bot.command(name="초대")
async def ping(ctx):
    embed=discord.Embed(title="띵이봇 초대하기!", color=0x04ff00)
    embed.add_field(name="띵이봇의 초대링크!", value="http://invite.thingebot.kro.kr/", inline=True)
    embed.add_field(name="띵이봇 위키!", value="https://github.com/OHvrything/thingebotV2/wiki", inline=False)
    embed.set_footer(text="띵이봇을 초대하고 함게 놀아요!")
    await ctx.send(embed=embed)
    
@bot.command(name="도움말")
async def ping(ctx):
    embed=discord.Embed(title="띵이봇 위키", description="깃허브에서 제공하는 띵이봇 위키를 살펴보세요!", color=0x04ff00)
    embed.add_field(name="띵이봇 위키", value="https://github.com/OHvrything/thingebotV2/wiki", inline=True)
    embed.add_field(name="공식 포럼", value="https://discord.gg/nrsVh8EUHE", inline=False)
    embed.set_footer(text="띵이봇의 도움말, 초대 등이 있어요!")
    await ctx.send(embed=embed)
        
@bot.event
async def on_message(message):
    if message.author.bot == False:
        with open('users.json', 'r') as f:
            users = json.load(f)

        await update_data(users, message.author)
        await add_experience(users, message.author, 5)
        await level_up(users, message.author, message)

        with open('users.json', 'w') as f:
            json.dump(users, f)

    await bot.process_commands(message)


async def update_data(users, user):
    if not f'{user.id}' in users:
        users[f'{user.id}'] = {}
        users[f'{user.id}']['experience'] = 0
        users[f'{user.id}']['level'] = 0


async def add_experience(users, user, exp):
    users[f'{user.id}']['experience'] += exp


async def level_up(users, user, message):
    with open('levels.json', 'r') as g:
        levels = json.load(g)
    experience = users[f'{user.id}']['experience']
    lvl_start = users[f'{user.id}']['level']
    lvl_end = int(experience ** (1 / 4))
    if lvl_start < lvl_end:
        embed = discord.Embed(title='레밸이 상승되였습니다!', color=0x00FF00,
                        description=f'{user.mention}님의 래벨이 상승 되였습니다'
                                    f'\n 현제 레밸: {lvl_end}')
        await message.channel.send(embed=embed)
        users[f'{user.id}']['level'] = lvl_end

@bot.command(name="레벨")
async def level(ctx, member: discord.Member = None):
    if not member:
        id = ctx.message.author.id
        with open('users.json', 'r') as f:
            users = json.load(f)
        lvl = users[str(id)]['level']
        await ctx.send(f'당신의 레벨입니다!\n현제 래벨 : [{lvl}]')
    else:
        id = member.id
        with open('users.json', 'r') as f:
            users = json.load(f)
        lvl = users[str(id)]['level']
        await ctx.send(f'{member}님의 레벨입니다!\n현제 래벨 : {lvl}')

bot.run(os.environ['token'])
