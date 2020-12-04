import discord
from discord.ext import commands
from PingPongTool import PingPong
from random import randint
import os
import time
import requests
import json

korea = "http://api.corona-19.kr/korea?serviceKey="
key = (os.environ['covidtoken']) #API 키(https://api.corona-19.kr/ 에서 무료 발급 가능)

response = requests.get(korea + key)
text = response.text
data = json.loads(text)

def RandomColor():
    return randint(0, 0xFFFFFF)

Authorization = (os.environ['pingpongtoken'])
URL = "https://builder.pingpong.us/api/builder/5f8bdb67e4b07b8420a30e71/integration/v0.2/custom/{sessionId}"

bot = commands.Bot(command_prefix=['?', '띵아 '])
Ping = PingPong(URL, Authorization)

@bot.event
async def on_ready():
    print("준비 완료!")
    game = discord.Game("'띵아 도움말' 명령어로 띵이봇과 노는법을 알아보세요! | 버전: TEB 2.11.4")
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
    else:
        embed = discord.Embed(title="오류!!", description="오류가 발생했습니다.", color=0xFF0000)
        embed.add_field(name="상세", value=f"```{error}```")
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
    embed.add_field(name="1번", value="공지채널로 설정할 채널 이름을 **0띵이봇, 봇-공지, 또는 봇공지**로 시작하세요!", inline=False)
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

@bot.command()
async def ping(ctx):
    latancy = bot.latency
    await ctx.send("\U0001F4E2"f' Pong! {round(latancy * 1000)}ms')

@commands.has_permissions(administrator=True)
@bot.command(name="kick", pass_context=True)
async def _kick(ctx, *, user_name: discord.Member, reason=None):
    await user_name.kick(reason=reason)
    await ctx.send(str(user_name)+"을(를) 추방하였습니다!")

@commands.has_permissions(administrator=True)
@bot.command(name="ban", pass_context=True)
async def _ban(ctx, *, user_name: discord.Member):
    await user_name.ban()
    await ctx.send(str(user_name)+"을(를) 이 서버에서 밴해버렸습니다!")

@commands.has_permissions(administrator=True)
@bot.command(name="unban", pass_context=True)
async def _unban(ctx, *, user_name):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = user_name.split('#')
    for ban_entry in banned_users:
        user = ban_entry.user
        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f"{user.mention}을(를) 밴 해제했어요!")
            return
    
@commands.has_permissions(administrator=True)
@bot.command(name="지워", pass_context=True)
async def _clear(ctx, *, amount=5):
    await ctx.channel.purge(limit=amount)
    
@bot.command(name="코로나현황")
async def ping(ctx):
        response = requests.get(korea + key)
        text = response.text
        data = json.loads(text)
        await ctx.channel.send(
            "<:covid:783582454619045910> [ " + data["updateTime"] + " ] <:covid:783582454619045910>\n\n" + 
            "국내 확진자: " + data["TotalCase"] + "(+" + data["TotalCaseBefore"] + ")"+ "\n" + 
            "국내 완치자: " + data["TotalRecovered"] + "(+" + data["TodayRecovered"] + ")"+ "\n" + 
            "국내 사망자: " + data["TotalDeath"] + "(+" + data["TodayDeath"] + ")"+ "\n" + 
            "국내 치료중: " + data["NowCase"] + "\n\n" +
            "우리는 코로나를 이길수 있어요!! 퐈이팅!!!"
        )

bot.remove_command("help")
bot.run(os.environ['token'])
