import discord
import math
from discord.ext import commands, tasks
from discord.utils import get
from itertools import cycle
from random import choice,randint,sample,shuffle
from PyDictionary import PyDictionary
from unit_converter.converter import converts
from googlesearch import search
from googletrans import Translator
from difflib import SequenceMatcher
from deck_of_cards import deck_of_cards
from github import Github
from captcha.image import ImageCaptcha
from pytrivia import Trivia,Type
from os import urandom,environ,getenv
from dotenv import load_dotenv
from pathlib import Path
from py_glo_boards_api import GloBoard
from string import ascii_lowercase
from lyrics_extractor import SongLyrics
from lyrics_extractor.lyrics import LyricScraperException
from textwrap import TextWrapper
import urllib
import urllib.request
import json
import asyncio
import arrow
import minesweeperPy
import typing

client = commands.Bot(command_prefix='s!')
df = "Elevator Server Bot Ver.17.51.267 Developed By: BLANK"
game = cycle(["A Bot for the Elevator Discord Server!",'Developed By: BLANK','Use s!help to see my commands!',df.replace(" Developed By: BLANK","")])
hc = 0x8681bb
client.remove_command('help')
if "GITHUB_TOKEN" not in environ.keys() and "BOT_TOKEN" not in environ.keys() and "KRAKEN_TOKEN" not in environ.keys()\
        and "GCS_TOKEN" not in environ.keys():
    env_path = Path(".") / ".env"
    load_dotenv(dotenv_path=env_path)
GITHUB_TOKEN = getenv("GITHUB_TOKEN")
BOT_TOKEN = getenv("BOT_TOKEN")
KRAKEN_TOKEN = getenv("KRAKEN_TOKEN")
GCS_TOKEN = getenv("GCS_TOKEN")
if GITHUB_TOKEN is None or BOT_TOKEN is None or KRAKEN_TOKEN is None or GCS_TOKEN is None:
    print("Cannot get either the github token or bot token or gitkraken token or the gcs token, make sure they are in "
          "environment variable OR .env file")
    exit()
github = Github(GITHUB_TOKEN)
repo = github.get_repo("BLANK-TH/elevator-bot-resources")
globoard = GloBoard(KRAKEN_TOKEN)
board_id = "5f2ae8cf15d46100116b20a5"
queue_column_id = "5f2ae8cf15d46100116b20ac"
approval_column_id = "5f2d4a30ab0eea0011aa048f"
all_labels = json.loads(urllib.request.urlopen(
    "https://raw.githubusercontent.com/BLANK-TH/elevator-bot-resources/bot-storage/labels.json").read())
lyrics_extractor = SongLyrics(GCS_TOKEN,"015568929789699384240:dwqehllbwrs")

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Game('Developed by BLANK'))
    change_game.start()
    print("Bot is ready.")

@tasks.loop(seconds=10)
async def change_game():
    await client.change_presence(activity=discord.Game(next(game)))

@client.event
async def on_message(message):
    if "S!" == message.content[:2]:
        message.content = "s!" + message.content[2:]
    for mention in message.mentions:
        if 699677108607123548 == mention.id:
            msg = await message.channel.send("<a:angryping:725393149484335165>")
            await msg.delete(delay=15)
            break
    if message.channel.id == 689077082609025089 and not message.author.bot:
        if "//" == message.content[:2]:
            return
        if "s!purge" == message.content[:7]:
            await client.process_commands(message)
            return
        try:
            cur_num = int(message.content)
        except:
            await message.delete()
            embed = discord.Embed(
                title="Please don't chat here, this channel is for counting only.",
                colour=hc
            )
            embed.set_footer(text=df)
            msg = await message.channel.send(embed=embed)
            await msg.delete(delay=5)
            return
        last_message = ""
        limit = 2
        while True:
            async for mes in message.channel.history(limit=limit):
                last_message = mes
            if "//" == last_message.content[:2] or (last_message.author.bot and mes.webhook_id is None):
                limit += 1
            else:
                break
        try:
            last_num = int(last_message.content)
        except Exception as e:
            await message.channel.send("An error has occurred! Everyone else ignore this message and keep counting! "
                                       "<@616032766974361640>",embed=discord.Embed(description=repr(e)))
            return
        if cur_num <= last_num or cur_num > last_num + 1:
            embed = discord.Embed(
                title="Incorrect Number",
                colour=hc
            )
            embed.set_footer(text=df)
            embed.add_field(name="Number You Entered:",value=str(cur_num))
            embed.add_field(name="Number You Should Have Entered:",value=str(last_num+1))
        elif message.author.id == last_message.author.id:
            embed = discord.Embed(
                title="Don't count by yourself!",
                colour=hc
            )
            embed.set_footer(text=df)
            embed.add_field(name="Your User ID:",value=message.author.id)
            embed.add_field(name="Last User ID:",value=last_message.author.id)
        else:
            return
        await message.delete()
        m = await message.channel.send("Sigh, I'm disappointed in you!",embed=embed)
        await m.delete(delay=5)
        return
    if message.channel.id == 740675095005102153 and not message.author.bot:
        if "//" == message.content[:2]:
            return
        if "s!purge" == message.content[:7]:
            await client.process_commands(message)
            return
        last_message = ""
        limit = 2
        while True:
            async for mes in message.channel.history(limit=limit):
                last_message = mes
            if "//" == last_message.content[:2] or (last_message.author.bot and mes.webhook_id is None):
                limit += 1
            else:
                break
        if " " in message.content:
            embed = discord.Embed(
                title="One Word Only!",
                colour=hc
            )
            embed.set_footer(text=df)
            embed.add_field(name="Message You Entered:",value=message.content)
        elif message.author.id == last_message.author.id:
            embed = discord.Embed(
                title="Don't make the story by yourself!",
                colour=hc
            )
            embed.set_footer(text=df)
            embed.add_field(name="Your User ID:", value=message.author.id)
            embed.add_field(name="Last User ID:", value=last_message.author.id)
        else:
            return
        await message.delete()
        msg = await message.channel.send("Sigh, I'm disappointed in you!",embed=embed)
        await msg.delete(delay=5)
        return
    await client.process_commands(message)

@client.event
async def on_member_join(member):
    sr_channel = client.get_channel(692521137166614570)
    w_channel = client.get_channel(685932859097350160)
    v_channel = client.get_channel(737093236803239977)
    c_channel = client.get_channel(686703151738519561)
    r_channel = client.get_channel(686700028399452181)
    b_channel = client.get_channel(690221900621676586)
    unverified = get(member.guild.roles, id=737092006349635706)
    w_embed = discord.Embed(
        description= f'Hey {member.mention}! Welcome to **elevator (F127)**! Make sure to verify yourself in '
                     f'{v_channel.mention} by using `s!verify` and read {r_channel.mention}. Once you\'ve done that'
                     f', Head over to {sr_channel.mention}, {c_channel.mention}, and {b_channel.mention}!!'
                     f' We hope you enjoy your time here :D',
        colour=hc
    )
    w_embed.set_footer(text=df)

    await w_channel.send(embed=w_embed)
    await member.add_roles(unverified)

@client.event
async def on_member_remove(member):
    w_channel = client.get_channel(686693349545213977)
    w_embed = discord.Embed(
        description=f'**{member}** has left!',
        colour=hc
    )
    w_embed.set_footer(text=df)

    await w_channel.send(embed=w_embed)

@client.event
async def on_command_error(ctx,error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.message.channel.send("Missing Required Argument: {}. For info on how to use the command, look at the "
                                       "help docs (`s!help`)".format(error.param.name))
    elif isinstance(error, commands.BadArgument):
        await ctx.message.channel.send("Bad Argument: Could Not Parse Commands Argument")
    elif isinstance(error, commands.CommandNotFound):
        def similar(a, b):
            return SequenceMatcher(None, a, b).ratio()
        command = ctx.message.content.split(" ")[0]
        command_similarities = {}
        for cmd in client.commands:
            command_similarities[similar(command,cmd.name)] = cmd.name
        if len(command_similarities) == 0:
            await ctx.message.channel.send("Invalid Command, no similar commands found.")
        highest_command = max([*command_similarities]), command_similarities[max([*command_similarities])]
        if highest_command[0] < 0.55:
            await ctx.message.channel.send("Invalid Command, no commands with greater than 55% similarity found.")
        else:
            await ctx.message.channel.send("Invalid Command, did you mean `{}`?".format(highest_command[1]))
    elif isinstance(error, commands.CommandOnCooldown):
        await ctx.message.channel.send("The Command is on Cooldown, Try Again in **{}** seconds".format(str(error.retry_after)))
    elif isinstance(error, commands.MissingPermissions):
        await ctx.message.channel.send("Missing Permissions to Run This Command: {}"
                                       .format(", ".join(x.replace("_"," ").title() for x in error.missing_perms)))
    elif isinstance(error, commands.BotMissingPermissions):
        await ctx.message.channel.send("Bot is Missing the Required Permissions to Run This Command: {}"
                                       .format(", ".join(x.replace("_"," ").title() for x in error.missing_perms)))
    else:
        await ctx.message.channel.send("Uncommon Error <@616032766974361640>",embed=discord.Embed(description=repr(error)))

@client.command()
async def help(ctx):
    help_embed = discord.Embed(
        title='Help',
        description="Commands: [CLICK HERE]({})".format(
            "https://github.com/BLANK-TH/elevator-bot-resources/blob/info/commands.md"
        ),
        colour=hc
    )
    help_embed.set_footer(text=df)
    await ctx.message.channel.send(embed=help_embed)

@client.command()
async def test(ctx):
    embed = discord.Embed(
        title="The bot works fine!",
        colour=hc
    )
    embed.set_footer(text=df)
    await ctx.channel.send(embed=embed)

@client.command(pass_context=True, aliases=['pfp','profile'])
async def avatar(ctx, member: discord.Member='None'):
    if member == "None":
        member = ctx.message.author
    a_embed = discord.Embed(
        description=f"{member.mention}'s Avatar/Profile Picture",
        colour=hc
    )
    a_embed.set_footer(text=df)
    a_embed.set_image(url=f'{member.avatar_url}')

    await ctx.message.channel.send(embed=a_embed)

@client.command()
async def mock(ctx,*,phrase:str):
    mock = ''
    for x in phrase:
        if x == ' ':
            mock += ' '
            continue
        rand = randint(1,2)
        if rand == 1:
            mock += x.upper()
            continue
        mock += x.lower()
    if ('theo' in phrase.lower() or 'blank' in phrase.lower()) and ctx.message.author.id != 616032766974361640:
        mock = f"How dare you insult my owner. {ctx.message.author.mention} go f*ck yourself!"
    embed = discord.Embed(
        description=mock,
        colour=hc
    )
    embed.set_footer(text=df)
    embed.set_image(url='https://i.imgur.com/qDhQKQb.gif')
    if ('theo' in phrase.lower() or 'blank' in phrase.lower()) and ctx.message.author.id != 616032766974361640:
        embed.set_image(url='https://i.imgur.com/t96AqDf.png')

    await ctx.message.channel.send(embed=embed)

@client.command(aliases=['pickup','pickupline','pl'])
async def pickuplines(ctx):
    url = urllib.request.urlopen("https://raw.githubusercontent.com/BLANK-TH/elevator-bot-resources/bot-storage/pickuplines.json")
    lines = json.loads(url.read())
    line = choice(lines)
    embed = discord.Embed(
        title=f"{ctx.message.author.name} here is your pickup line.",
        description=line,
        colour=hc
    )
    embed.set_footer(text=df)
    embed.set_image(url='https://g2x4w9d4.stackpathcdn.com/wp-content/uploads/2017/02/cheesy.gif')

    await ctx.message.channel.send(embed=embed)

@client.command()
async def hug(ctx,users:commands.Greedy[discord.Member]):
    random_hug_image_gif = ['https://i.imgur.com/FICmRtv.jpg',
                            'https://i.imgur.com/Ourqcvo.jpg',
                            'https://i.imgur.com/QIWmEhg.jpg',
                            'https://i.imgur.com/Rcee4gW.png',
                            'https://i.imgur.com/YmiehhV.png',
                            'https://i.imgur.com/hxmRmTm.png',
                            'https://i.imgur.com/fvlm134.jpg',
                            'https://i.imgur.com/m8DXSgw.jpg'
                            ]
    rhi = choice(random_hug_image_gif)
    user = ', '.join(x.mention for x in users)
    if user != ctx.message.author.display_name and len(users) >= 1:
        msg = f'{ctx.message.author.mention} has hugged {user}'
    else:
        msg = f'{ctx.message.author.mention} is hugging themselves?'
    a_embed = discord.Embed(
        description=msg,
        colour=hc
    )
    a_embed.set_footer(text=df)
    a_embed.set_image(url=rhi)

    await ctx.message.channel.send(embed=a_embed)

@client.command()
async def kiss(ctx,users:commands.Greedy[discord.Member]):
    random_kiss_image_gif = ['https://i.imgur.com/0CUZcy1.jpg',
                             'https://i.imgur.com/Bo6FcYk.jpg',
                             'https://i.imgur.com/Gc9eUHC.jpg'
                             ]
    rki = choice(random_kiss_image_gif)
    user = ', '.join(x.mention for x in users)
    if user != ctx.message.author.display_name and len(users) >= 1:
        msg = f'{ctx.message.author.mention} has kissed {user}'
    else:
        msg = f'{ctx.message.author.mention} is kissing themselves?'
    k_embed = discord.Embed(
        description=msg,
        colour=hc
    )
    k_embed.set_footer(text=df)
    k_embed.set_image(url=rki)

    await ctx.message.channel.send(embed=k_embed)

@client.command()
async def pat(ctx,users:commands.Greedy[discord.Member]):
    random_pats_image_gif = ['https://i.imgur.com/pUfhIEx.jpg',
                             'https://i.imgur.com/6IEORJr.jpg',
                             'https://i.imgur.com/26Deeck.jpg',
                             'https://i.imgur.com/Gj0fj7m.jpg',
                             'https://i.imgur.com/xOv9bY1.jpg',
                             'https://i.imgur.com/4t3drCT.jpg'
                             ]
    rpi = choice(random_pats_image_gif)
    user = ', '.join(x.mention for x in users)
    if user != ctx.message.author.display_name and len(users) >= 1:
        msg = f'{ctx.message.author.mention} is patting {user}!'
    else:
        msg = f'{ctx.message.author.mention} is patting themselves?'
    p_embed = discord.Embed(
        description=msg,
        colour=hc
    )
    p_embed.set_footer(text=df)
    p_embed.set_image(url=rpi)

    await ctx.message.channel.send(embed=p_embed)

@client.command()
async def facepalm(ctx):
    f_embed = discord.Embed(
        description=f'{ctx.message.author.mention} is facepalming!',
        colour=hc
    )
    f_embed.set_footer(text=df)
    f_embed.set_image(url='https://i.imgur.com/e1NsTzQ.jpg')

    await ctx.message.channel.send(embed=f_embed)

@client.command()
async def sigh(ctx):
    s_embed = discord.Embed(
        description=f'{ctx.message.author.mention} has sighed!',
        colour=hc
    )
    s_embed.set_footer(text=df)
    s_embed.set_image(url='https://i.imgur.com/JWeTHLT.jpg')

    await ctx.message.channel.send(embed=s_embed)

@client.command()
async def cute(ctx,*,user:discord.Member='empty'):
    random_cute_image_gif = ['https://i.imgur.com/r6CB5T0.jpg',
                             'https://i.imgur.com/pV9V1zj.jpg',
                             'https://i.imgur.com/FICmRtv.jpg',
                             'https://i.imgur.com/IpBEWZK.jpg',
                             'https://i.imgur.com/lLwkl9v.jpg',
                             'https://i.imgur.com/ez9K9wU.gif',
                             'https://i.imgur.com/S5M8tNM.jpg',
                             'https://i.imgur.com/8F4Y4vT.jpg',
                             'https://i.imgur.com/K4QDlLP.jpg',
                             'https://i.imgur.com/K4QDlLP.jpg',
                             'https://i.imgur.com/t8fvHeK.jpg',
                             'https://i.imgur.com/VM0Me3O.png',
                             'https://i.imgur.com/KUBa7EZ.jpg',
                             'https://i.imgur.com/D0qcnNz.jpg',
                             'https://i.imgur.com/NvCX3uF.jpg',
                             'https://i.imgur.com/hpoFYF3.jpg'
                             ]
    rci = choice(random_cute_image_gif)
    if user != 'empty':
        msg = f'{ctx.message.author.mention} thinks that {user.mention} is cute!'
    else:
        msg = f'{ctx.message.author.mention} is calling themselves cute?'
    c_embed = discord.Embed(
        description=msg,
        colour=hc
    )
    c_embed.set_footer(text=df)
    c_embed.set_image(url=rci)

    await ctx.message.channel.send(embed=c_embed)

@client.command(aliases=['rps'])
async def rockpaperscissors(ctx,choose):
    choose = choose.lower()
    if choose == 'rock' or choose == 'r':
        is_rps = True
        p_choose = 'Rock'
    elif choose == 'scissors' or choose == 's':
        is_rps = True
        p_choose = "Scissors"
    elif choose == 'paper' or choose == 'p':
        is_rps = True
        p_choose = "Paper"
    else:
        is_rps = False
        embed = discord.Embed(title="Invalid Option, Try again!",colour=discord.Colour.red())
        embed.set_image(url='https://i.imgur.com/XgqWMei.jpg')
    if is_rps:
        RPS_options = ['Rock', 'Paper', 'Scissors']
        b_choose = choice(RPS_options)
        #True = Bot Win False = Player Win Tie = Tie
        if b_choose == p_choose:
            wlt = "Tie"
        elif b_choose == 'Rock':
            if p_choose == "Scissors":
                wlt = True
            if p_choose == "Paper":
                wlt = False
        elif b_choose == "Scissors":
            if p_choose == "Rock":
                wlt = False
            if p_choose == "Paper":
                wlt = True
        elif b_choose == "Paper":
            if p_choose == "Rock":
                wlt = True
            if p_choose == "Scissors":
                wlt = False
        if wlt != "Tie":
            if wlt:
                embed = discord.Embed(title=f"I choose {b_choose}, You chose {p_choose}. I Win!",colour=discord.Colour.red())
            else:
                embed = discord.Embed(title=f"I choose {b_choose}, You chose {p_choose}. I Lose!",colour=discord.Colour.green())
        else:
            embed = discord.Embed(title=f"I choose {b_choose}, You chose {p_choose}. We Tie!",colour=discord.Colour.gold())
        if b_choose == "Rock":
            img = 'https://i.imgur.com/xQQE5UA.jpg'
        elif b_choose == "Scissors":
            img = 'https://i.imgur.com/WAuWmFI.png'
        elif b_choose == "Paper":
            img = 'https://i.imgur.com/SK50Kvl.png'
        embed.set_image(url=img)
    embed.set_footer(text=df)
    await ctx.message.channel.send(embed=embed)

@client.command(aliases=['8ball','8b'])
async def _8ball(ctx,*,question):
    responses = ["It is certain", "It is decidedly so", "Without a doubt", "Yes, definitely",
     "You may rely on it", "As I see it, yes", "Most Likely", "Outlook Good",
     "Yes", "Signs point to yes", "Reply hazy, try again", "Ask again later",
     "Better not tell you now", "Cannot predict now", "Concentrate and ask again",
     "Don't count on it", "My reply is no", "My sources say no", "Outlook not so good", "Very Doubtful"]

    sel_response = choice(responses)

    embed = discord.Embed(title=f'{sel_response}!',description=f'Your Question: {question}!',colour=hc)
    embed.set_image(url='https://i.imgur.com/Es4mCIe.jpg')
    embed.set_footer(text=df)

    await ctx.message.channel.send(embed=embed)

@client.command()
async def dice(ctx,out_of='6'):
    con = True
    try:
        out_of_int = int(out_of)
    except ValueError as e:
        embed = discord.Embed(title='Please enter a actual number!', colour=discord.Colour.red())
        embed.set_image(url='https://i.imgur.com/XgqWMei.jpg')
        embed.add_field(name="Error:", value=str(e))
        con = False
    if con:
        ran_num = str(randint(1,out_of_int))
        embed = discord.Embed(title=f'The Dice Says: {ran_num}', colour=hc)
    embed.set_footer(text=df)

    await ctx.message.channel.send(embed=embed)

@client.command(pass_context=True)
async def kill(ctx,user:discord.Member,*,reason='None'):
    random_kill_message = [f'{ctx.message.author.mention} has killed {user.mention}',
                           f'{ctx.message.author.mention} has headshotted {user.mention}',
                           f'{user.mention} was shot by {ctx.message.author.mention}']
    km = choice(random_kill_message)
    k_embed = discord.Embed(
        description=km,
        colour=hc
    )
    k_embed.set_footer(text=df)
    k_embed.set_image(url='https://i.imgur.com/Za8sxpF.gif')
    if reason != "None":
        k_embed.add_field(name="Reason:",value=reason)
    await ctx.message.channel.send(embed=k_embed)

@client.command()
async def dm(ctx,member: discord.Member,*,message):
    await ctx.message.delete()
    await member.send(message + "\n\n **-" + ctx.message.author.display_name + "**")

@client.command()
async def bdm(ctx,member: discord.Member,*,message):
    if ctx.message.author.id == 616032766974361640:
        await ctx.message.delete()
        await member.send(message)

@client.command()
async def bsay(ctx,*,message):
    if ctx.message.author.id == 616032766974361640:
        await ctx.message.delete()
        await ctx.send(message)

@client.command()
async def say(ctx,*,message):
    await ctx.message.delete()
    await ctx.send(message + "\n\n **-" + ctx.message.author.display_name + "**")

@client.command()
async def slap(ctx,user:discord.Member,*,reason="None"):
    random_slap_image_gif = ['https://i.imgur.com/8yJ9qoh.jpg',
                             'https://i.imgur.com/LLIKgWT.png'
    ]
    rsi = choice(random_slap_image_gif)
    c_embed = discord.Embed(
        description=f'{ctx.message.author.mention} has slapped {user.mention}!',
        colour=hc
    )
    c_embed.set_footer(text=df)
    c_embed.set_image(url=rsi)
    if reason != "None":
        c_embed.add_field(name="Reason:",value=reason)

    await ctx.message.channel.send(embed=c_embed)

@client.command()
async def punch(ctx,user:discord.Member,*,reason='None'):
    p_embed = discord.Embed(
        description=f'{ctx.message.author.mention} has punched {user.mention}!',
        colour=hc
    )
    p_embed.set_footer(text=df)
    p_embed.set_image(url='https://i.imgur.com/Za8sxpF.gif')
    if reason != "None":
        p_embed.add_field(name="Reason:",value=reason)

    await ctx.message.channel.send(embed=p_embed)

@client.command(aliases=['cry','sad'])
async def crysad(ctx,*,reason="None"):
    random_cry_sad_image = ['https://i.imgur.com/2idqzX5.jpg',
                            'https://i.imgur.com/21qHg4N.jpg',
                            'https://i.imgur.com/WEIMm9N.jpg',
                            'https://i.imgur.com/DgYa47G.png',
                            'https://i.imgur.com/ED5vXzC.jpg',
                            'https://i.imgur.com/weekaqO.png',
                            'https://i.imgur.com/yR0oqj8.jpg',
                            'https://i.imgur.com/sM6SvUm.jpg',
                            'https://i.imgur.com/ceHRXvU.jpg'
    ]
    random_cry_sad_message = [f"{ctx.message.author.mention} is sad!",
                              f"{ctx.message.author.mention} is crying!",
                              f"{ctx.message.author.mention} is sad! Someone go hug him/her!",
                              f"{ctx.message.author.mention} is crying! Someone go hug him/her!"
    ]
    rcsi = choice(random_cry_sad_image)
    rcsm = choice(random_cry_sad_message)
    embed = discord.Embed(description=rcsm,colour=hc)
    embed.set_image(url=rcsi)
    embed.set_footer(text=df)
    if reason != "None":
        embed.add_field(name="Reason:",value=reason)
    await ctx.message.channel.send(embed=embed)

@client.command(aliases=['mad'])
async def angry(ctx,*,reason="None"):
    random_angry_image = ['https://i.imgur.com/1VXQ0cl.jpg',
                          'https://i.imgur.com/lrXbqIq.jpg',
                          'https://i.imgur.com/xCZ8qEr.png'
    ]
    random_angry_message = [f"{ctx.message.author.mention} is mad!",
                              f"{ctx.message.author.mention} is angry!",
                              f"{ctx.message.author.mention} is mad! Don't piss him/her off more",
                              f"{ctx.message.author.mention} is angry! Someone go hug him/her!",
                              f"{ctx.message.author.mention} is mad! Tread lightly",
                              f"{ctx.message.author.mention} is angry! Tread lightly!"
    ]
    rai = choice(random_angry_image)
    ram = choice(random_angry_message)
    embed = discord.Embed(description=ram,colour=hc)
    embed.set_image(url=rai)
    embed.set_footer(text=df)
    if reason != "None":
        embed.add_field(name="Reason:",value=reason)
    await ctx.message.channel.send(embed=embed)

@client.command()
async def ship(ctx,user1: discord.Member,user2: discord.Member):
    length_u1 = math.floor(len(user1.display_name)/2)
    length_u2 = math.floor(len(user2.display_name)/2)
    u1 = user1.display_name[0:length_u1]
    u2 = user2.display_name[length_u2:len(user2.display_name)]
    ship_name = u1 + u2
    ship_embed = discord.Embed(
        title=ship_name,
        description=f"{user1.mention} and {user2.mention}'s Ship Name",
        colour=hc
    )
    ship_embed.set_footer(text=df)
    await ctx.message.channel.send(embed=ship_embed)

@client.command()
async def steal(ctx,user: discord.Member,*,item):
    random_steal_message = [f"{ctx.message.author.mention} has stolen {item} from {user.mention}!",
                            f"{ctx.message.author.mention} has taken {item} from {user.mention}!",
                            f"{user.mention}'s {item} is missing! It seems {ctx.message.author.mention} has taken it!",
                            f"{ctx.message.author.mention} really likes {user.mention}'s {item} so he/she took it!"
                            ]
    rsm = choice(random_steal_message)
    s_embed = discord.Embed(
        description=rsm,
        colour=hc
    )
    s_embed.set_footer(text=df)
    s_embed.set_image(url='https://i.imgur.com/gQNFxGj.jpg')
    await ctx.message.channel.send(embed=s_embed)

@client.command()
async def punish(ctx,user: discord.Member,*,reason="None"):
    p_embed = discord.Embed(
        description=f"{ctx.message.author.mention} has punished {user.mention}!",
        colour=hc
    )
    p_embed.set_footer(text=df)
    p_embed.set_image(url='https://i.imgur.com/RyEErwy.jpg')
    if reason != "None":
        p_embed.add_field(name="Reason:",value=reason)
    await ctx.message.channel.send(embed=p_embed)


@client.command()
async def insult(ctx,user:discord.Member,*,reason="None"):
    random_embed_message = [
        f"{ctx.message.author.mention} has insulted {user.mention}!",
        f"{ctx.message.author.mention} has insulted {user.mention}, what a savage!",
        f"{user.mention} has been insulted by {ctx.message.author.mention}!"
    ]
    rem = choice(random_embed_message)
    i_embed = discord.Embed(
        description=rem,
        colour=hc
    )
    i_embed.set_image(url='https://i.imgur.com/uaz7WXM.jpg')
    if reason != "None":
        i_embed.add_field(name="Reason:",value=reason)
    i_embed.set_footer(text=df)
    await ctx.message.channel.send(embed=i_embed)

@client.command(aliases=['hf'])
async def highfive(ctx,user:discord.Member):
    h_embed = discord.Embed(
        description=f"{ctx.message.author.mention} has high-fived {user.mention}",
        colour=hc
    )
    h_embed.set_image(url='https://i.imgur.com/CBdjdbi.jpg')
    h_embed.set_footer(text=df)

    await ctx.message.channel.send(embed=h_embed)

@client.command(aliases=['ck'])
async def chatkilled(ctx,user:discord.Member="None"):
    if user != "None":
        msg = f"{ctx.message.author.mention} thinks {user.mention} has killed the chat! Someone revive it!"
    else:
        msg = f"{ctx.message.author.mention} thinks the chat has been killed. Someone revive it!"
    c_embed = discord.Embed(
        description=msg,
        colour=hc
    )
    c_embed.set_footer(text=df)
    c_embed.set_image(url='https://i.imgur.com/6Z4bVys.jpg')

    await ctx.message.channel.send(embed=c_embed)

@client.command(aliases=['fac'])
async def flipacoin(ctx):
    sides = ["Heads","Tails"]
    ans = choice(sides)
    r_embed = discord.Embed(
        title=f"You got {ans}!",
        colour=hc
    )
    if ans == "Heads":
        r_embed.set_image(url='https://i.imgur.com/vmuGKvI.png')
    else:
        r_embed.set_image(url='https://i.imgur.com/47kev45.png')
    r_embed.set_footer(text=df)

    await ctx.message.channel.send(embed=r_embed)

@client.command()
async def agree(ctx,user:discord.Member="None"):
    if user != "None":
        msg = f"{ctx.message.author.mention} agrees with what {user.mention} said!"
    else:
        msg = f"{ctx.message.author.mention} agrees with what was said!"
    a_embed = discord.Embed(
        description=msg,
        colour=hc
    )
    a_embed.set_footer(text=df)
    a_embed.set_image(url="https://i.imgur.com/sxu72BJ.jpg")

    await ctx.message.channel.send(embed=a_embed)

@client.command()
async def give(ctx,user: discord.Member,*,item):
    random_give_image = ['https://i.imgur.com/H0dXCW0.jpg',
                         'https://i.imgur.com/6fR6XYD.jpg',
                         'https://i.imgur.com/54wX55D.png'
                            ]
    rgi = choice(random_give_image)
    g_embed = discord.Embed(
        description=f"{ctx.message.author.mention} has given {item} to {user.mention}",
        colour=hc
    )
    g_embed.set_footer(text=df)
    g_embed.set_image(url=rgi)
    await ctx.message.channel.send(embed=g_embed)

@client.command()
async def invite(ctx):
    #put invite here
    invite = 'https://discord.gg/Cr43nuF'
    i_embed = discord.Embed(
        title="Here is the invite for the Elevator Server",
        colour=hc
    )
    i_embed.set_footer(text=df)
    i_embed.add_field(name="Invite:",value=invite)

    await ctx.message.channel.send(embed=i_embed)

@client.command(aliases=['gj'])
async def goodjob(ctx,user:discord.Member,*,reason="None"):
    random_goodjob_message = [
        f"{ctx.message.author.mention} thinks {user.mention} did a good job!",
        f"{ctx.message.author.mention} is congratulating {user.mention} for doing a good job!",
        f"{user.mention} is getting praised by {ctx.message.author.mention} for doing a good job!"
    ]
    rgjm = choice(random_goodjob_message)

    g_embed = discord.Embed(
        description=rgjm,
        colour=hc
    )
    g_embed.set_footer(text=df)
    g_embed.set_image(url='https://i.imgur.com/YciY7Qo.jpg')
    if reason != "None":
        g_embed.add_field(name="Reason:",value=reason)

    await ctx.message.channel.send(embed=g_embed)

@client.command(aliases=['respects'])
async def f(ctx,user:discord.Member="None"):
    random_f_image = [
            'https://i.imgur.com/Qn4lHqJ.png',
            'https://i.imgur.com/Li6lOuw.jpg'
    ]
    rfi = choice(random_f_image)
    if user != "None":
        msg = f"Press F to pay respects to {user.mention}"
    else:
        msg = "Press F to pay respects!"
    f_embed = discord.Embed(
        description=msg,
        colour=hc
    )
    f_embed.set_footer(text=df)
    f_embed.set_image(url=rfi)

    await ctx.message.channel.send(embed=f_embed)

@client.command(aliases=['doubt'])
async def x(ctx,user:discord.Member="None"):
    random_x_image = [
        'https://i.imgur.com/0GETcS1.jpg',
        'https://i.imgur.com/wutBLAX.png'
    ]
    rxi = choice(random_x_image)
    if user != "None":
        msg = f"Spam X to doubt {user.mention}!"
    else:
        msg = "Spam X to doubt!"
    x_embed = discord.Embed(
        description=msg,
        colour=hc
    )
    x_embed.set_footer(text=df)
    x_embed.set_image(url=rxi)

    await ctx.message.channel.send(embed=x_embed)

@client.command(aliases=['hb','birthday'])
async def happybirthday(ctx,user:discord.Member):
    random_birthday_image = [
            'https://i.imgur.com/sgJBE5E.jpg',
            'https://i.imgur.com/oHVZmQm.jpg',
            'https://i.imgur.com/SlRPSvc.png'
    ]
    rbi = choice(random_birthday_image)
    b_embed = discord.Embed(
        description=f"{ctx.message.author.mention} wishes a happy birthday to {user.mention}",
        colour=hc
    )
    b_embed.set_footer(text=df)
    b_embed.set_image(url=rbi)

    await ctx.message.channel.send(embed=b_embed)

@client.command(aliases=['bored','boredom.exe'])
async def boredom(ctx):
    random_boredom_message = [
        f'{ctx.message.author.mention} is bored!',
        f'{ctx.message.author.mention} has started the process boredom.exe!',
        f'{ctx.message.author.mention} is bored! Someone do something with him/her!'
    ]
    rbm = choice(random_boredom_message)
    b_embed = discord.Embed(
        description=rbm,
        colour=hc
    )
    b_embed.set_footer(text=df)
    b_embed.set_image(url='https://i.imgur.com/JpSbAji.jpg')

    await ctx.message.channel.send(embed=b_embed)

@client.command(aliases=['think','thinking.exe'])
async def thinking(ctx):
    random_thinking_message = [
        f'{ctx.message.author.mention} is thinking!',
        f'{ctx.message.author.mention} has started the process thinking.exe!',
    ]
    random_thinking_image = [
        'https://i.imgur.com/tgUNcwr.jpg',
        'https://i.imgur.com/akIMMK9.jpg',
        'https://i.imgur.com/ebHYDox.jpg'
    ]
    rtm = choice(random_thinking_message)
    rti = choice(random_thinking_image)
    t_embed = discord.Embed(
        description=rtm,
        colour=hc
    )
    t_embed.set_footer(text=df)
    t_embed.set_image(url=rti)

    await ctx.message.channel.send(embed=t_embed)

@client.command()
async def oof(ctx,user: discord.Member="None"):
    random_oof_message = [
        f'{ctx.message.author.mention} got oofed!',
        f'{ctx.message.author.mention} had a oof moment!',
    ]
    if user != "None":
        random_oof_message.append(f'{ctx.message.author.mention} thinks {user.mention} had a oof moment!')
        random_oof_message.append(f'{ctx.message.author.mention} has oofed {user.mention}!')
    random_oof_image = [
        'https://i.imgur.com/x4nl4Le.jpg',
        'https://i.imgur.com/yDyG5YY.jpg',
        'https://i.imgur.com/jYJoP7i.jpg'
    ]
    rom = choice(random_oof_message)
    roi = choice(random_oof_image)
    o_embed = discord.Embed(
        descriptione=rom,
        colour=hc
    )
    o_embed.set_footer(text=df)
    o_embed.set_image(url=roi)

    await ctx.message.channel.send(embed=o_embed)

@client.command()
async def serverinfo(ctx):
    guild = ctx.author.guild
    creation_time = guild.created_at
    creation_time = creation_time.strftime("%Y-%m-%d %H:%M UTC")
    channels = [f"Channels of {guild.name}:"]
    roles = []
    for x in guild.channels:
        if type(x) != discord.TextChannel:
            continue
        channels.append(x.name)
    for x in guild.roles:
        roles.append(x.name)
    roles.append(f"Roles of {guild.name}:")
    roles.reverse()
    channel_msg = '\n'.join(x for x in channels)
    role_msg = '\n'.join(x for x in roles)
    async with ctx.message.channel.typing():
        channel_url = repo.create_file("ChannelListForServerInfoMSG{}.txt".format(
        str(ctx.message.id)),
        "Requester ID: {} | Requester Name + Discriminator {}#{} | Message ID: {} | Message Link: {} | At: {}".format(
            str(ctx.message.author.id), ctx.message.author.name,
            ctx.message.author.discriminator, str(ctx.message.id), ctx.message.jump_url,
            ctx.message.created_at.strftime("%b %d %Y %H:%M UTC")),
        channel_msg,branch="commands")['content'].html_url
        role_url = repo.create_file("RoleListForServerInfoRequestMSG{}.txt".format(
        str(ctx.message.id)),
        "Requester ID: {} | Requester Name + Discriminator {}#{} | Message ID: {} | Message Link: {} | At: {}".format(
            str(ctx.message.author.id), ctx.message.author.name,
            ctx.message.author.discriminator, str(ctx.message.id), ctx.message.jump_url,
            ctx.message.created_at.strftime("%b %d %Y %H:%M UTC")),
        role_msg,branch="commands")['content'].html_url
    i_embed = discord.Embed(
        title=f"Server Info for {guild.name}",
        colour=hc
    )
    i_embed.set_footer(text=df)
    i_embed.set_thumbnail(url=guild.icon_url)
    i_embed.add_field(name="Name:",value=guild.name)
    i_embed.add_field(name="Region:", value=str(guild.region))
    i_embed.add_field(name="ID:", value=guild.id)
    i_embed.add_field(name="Owner:", value=guild.owner.display_name)
    i_embed.add_field(name="Member Count:", value=guild.member_count)
    i_embed.add_field(name="Creation Time:", value=creation_time)
    i_embed.add_field(name="Channels:",value=f"[CLICK HERE]({channel_url})")
    i_embed.add_field(name="Roles:",value=f"[CLICK HERE]({role_url})")

    await ctx.message.channel.send(embed=i_embed)

@client.command()
async def hangman(ctx):
    d = PyDictionary()
    url = urllib.request.urlopen("https://raw.githubusercontent.com/bevacqua/correcthorse/master/wordlist.json")
    words = json.loads(url.read())
    word = choice(words)
    definition = d.meaning(word)
    if definition == None:
        definition = "Definition Not Found"
    lives = 6
    word_list = []
    guessed_letters = []
    win = False
    for x in word:
        word_list.append('%')
    s_embed = discord.Embed(
        title=''.join(x for x in word_list),
        description="Welcome to Hangman! You have 6 lives. You can only guess one letter at a time (no full word guesses). Type your response. To quit, enter the word 'quit'."
        + " The word can be any word in the english dictionary, and can contain dashes('-').",
        colour=hc
    )
    s_embed.set_footer(text=df)
    s_embed.add_field(name="Lives:",value=str(lives))
    s_embed.add_field(name="Letters Left:",value=str(len([i for i,l in enumerate(word_list) if l == '%'])))
    await ctx.message.channel.send(embed=s_embed)

    def check(message):
        if message.author == ctx.message.author and message.channel == ctx.message.channel:
            return True
        else:
            return False
    def result(msg,rnr):
        if rnr:
            c = discord.Colour.dark_green()
        else:
            c = discord.Colour.dark_red()
        t_embed = discord.Embed(
            title=''.join(x for x in word_list),
            colour=c
        )
        t_embed.set_footer(text=df)
        t_embed.add_field(name="You Guessed:",value=msg.upper())
        t_embed.add_field(name="Lives:",value=str(lives))
        t_embed.add_field(name="Letters Left:", value=str(len([i for i, l in enumerate(word_list) if l == '%'])))

        return t_embed
    def check_win():
        num_left = len([i for i,l in enumerate(word_list) if l == '%'])
        if num_left == 0:
            return True
        return False

    while True:
        if lives <= 0:
            break
        msg = await client.wait_for('message',check=check,timeout=None)
        msg = msg.content.lower()
        if msg == 'quit':
            break
        if not len(msg) == 1 or msg in guessed_letters:
            await ctx.message.channel.send("You have either already guessed that letter before or you have entered more or less than 1 letter")
            continue
        indexes = [i for i,l in enumerate(word) if l == msg]
        if len(indexes) == 0:
            lives -= 1
            rnr = False
        else:
            for x in indexes:
                word_list[int(x)] = msg
            rnr = True
        guessed_letters.append(msg)
        await ctx.message.channel.send(embed=result(msg,rnr))
        if check_win():
            win = True
            break
    if win:
        e_embed = discord.Embed(
            title="You win!!!",
            colour=discord.Colour.green()
        )
        e_embed.set_footer(text=df)
        e_embed.add_field(name="Word:",value=word)
        e_embed.add_field(name="Lives Left:",value=str(lives))
        e_embed.add_field(name="Definition:",value=definition,inline=False)
    else:
        e_embed = discord.Embed(
            title="You lose!!!",
            colour=discord.Colour.red()
        )
        e_embed.set_footer(text=df)
        e_embed.add_field(name="Word:", value=word)
        e_embed.add_field(name="Letters Left:", value=str(len([i for i, l in enumerate(word_list) if l == '%'])))
        e_embed.add_field(name="Definition:", value=definition, inline=False)
    await ctx.message.channel.send(embed=e_embed)

@client.command(aliases=['uc'])
async def unitconvert(ctx,num1,unitfrom,unitto):
    units = [
        'm/meter','g/gram','s/second','A/ampere','K/kelvin','mol/mole','cd/candela','Hz/hertz','N/newton','Pa/pascal',
        'J/joule','W/watt','C/coulomb','V/volt','Ω/ohm','S/siemens','F/farad','T/tesla','Wb/weber','H/henry',
        '°C/celsius','rad/radian','sr/steradian','lm/lumen','lx/lux','Bq/becquerel','Gy/gray','Sv/sievert','kat/katal',
        '°F/fahrenheit','th/thou','in/inch','ft/foot','yd/yard','ch/chain','fur/furlong','ml/mile','lea/league','bar',
        'min/minute','h/hour'
    ]
    full_form = num1 + ' ' + unitfrom
    try:
        ans = float(converts(full_form,unitto))
    except Exception as e:
        embed = discord.Embed(
            title="That unit doesn't exist!",
            colour=hc
        )
        embed.set_footer(text=df)
        if unitfrom in str(e):
            embed.add_field(name="Error Unit:",value=f'The unit "{unitfrom}" ' + "doesn't exist!")
        else:
            embed.add_field(name="Error Unit:",value=f'The unit "{unitto}" ' + "doesn't exist!")
        embed.add_field(name="Error:", value=str(e))
        embed.add_field(name="Supported Units",value=', '.join(x for x in units),inline=False)
        await ctx.message.channel.send(embed=embed)
        return
    embed = discord.Embed(
        title=f'{str(ans)} {unitto}',
        colour=hc
    )
    embed.add_field(name="Convert From:",value=f'{num1} {unitfrom}')
    embed.add_field(name="Convert To:",value=unitto)
    embed.set_footer(text=df)

    await ctx.message.channel.send(embed=embed)

@client.command(aliases=['numberguess','ng'])
async def numguess(ctx,lives=8,max=100):
    try:
        lives = int(lives)
        max = int(max)
    except:
        await ctx.message.channel.send("Please enter a number!")
        return
    truenum = randint(0,max)
    win = False
    start_embed = discord.Embed(
        title="Welcome to the number guessing game! Guess a number between the range below and follow the clues given to guess the correct number. Type 'quit' to quit.",
        colour=hc
    )
    start_embed.set_footer(text=df)
    start_embed.add_field(name="Lives:",value=str(lives))
    start_embed.add_field(name="Range:",value=f"0-{str(max)}")

    await ctx.message.channel.send(embed=start_embed)

    def check(message):
        if message.author == ctx.message.author:
            return True
        else:
            return False
    def result(num,highlow):
        embed = discord.Embed(
            title=f"You guessed too {highlow}!",
            colour=discord.Colour.dark_red()
        )
        embed.add_field(name="You Guessed:",value=str(num))
        embed.add_field(name='Lives Left:',value=str(lives))
        embed.set_footer(text=df)
        return embed
    while True:
        if lives <= 0:
            break
        msg = await client.wait_for('message',check=check,timeout=None)
        if msg.content == 'quit':
            break
        try:
            guessnum = int(msg.content)
        except:
            await ctx.message.channel.send("Please enter a number!")
            continue
        if guessnum > max or guessnum < 0:
            await ctx.message.channel.send(f"The number you guessed is out of the range specified! The range is 0-{str(max)}")
            continue
        if guessnum == truenum:
            win = True
            break
        else:
            lives -= 1
            if guessnum > truenum: highlow = "high"
            if guessnum < truenum: highlow = "low"
            await ctx.message.channel.send(embed=result(guessnum,highlow))
    if win:
        e_embed = discord.Embed(
            title="You win!!!",
            colour=discord.Colour.green()
        )
        e_embed.set_footer(text=df)
        e_embed.add_field(name="Number:",value=str(truenum))
        e_embed.add_field(name="Lives Left:",value=str(lives))
    else:
        e_embed = discord.Embed(
            title="You loose!!!",
            colour=discord.Colour.red()
        )
        e_embed.set_footer(text=df)
        e_embed.add_field(name="Number:", value=str(truenum))
    await ctx.message.channel.send(embed=e_embed)

@client.command(aliases=['currentinzone','ciz'])
async def currenttimeintimezone(ctx,*,timezone):
    if ' ' in timezone:
        timezone = timezone.title()
    else:
        timezone = timezone.upper()
    utc = arrow.utcnow()
    try:
        current = utc.to(timezone)
    except Exception as e:
        e_embed = discord.Embed(
            title="Invalid Timezone!",
            description="You have may have entered a invalid timezone, if you are sure that the timezone is correct, try entering it in it's" +
            " short or long form, for example if you entered EDT, enter Eastern Daylight Time, and if you entered Eastern Standard Time enter" +
            " EST. Another important thing to keep in mind is Daylight Savings, for example in Toronto if daylight savings is active, we use EDT" +
            "(Eastern Daylight Time) but normally we use EST (Eastern Standard Time). If you were to enter EST, when daylight savings is active, " +
            "The time will be 1 hour off. The same goes for the other timezones that have Daylight Savings or something similar. " +
            "This command also works with UTC, you can enter something like 'UTC-5' which is EST, or 'UTC-4' which is EDT, The same goes for GMT-5/GMT-4. " +
            "This module is still a bit finicky so if there are bugs, rest assured that I am working on fixing it",
            colour=hc
        )
        e_embed.set_footer(text=df)
        e_embed.add_field(name="Error:",value=str(e))
        await ctx.message.channel.send(embed=e_embed)
        return
    r_embed = discord.Embed(
        title=f"Here is the current time in {timezone}",
        colour=hc
    )
    r_embed.set_footer(text=df)
    r_embed.add_field(name="Current Time:",value=current.format('YYYY-MM-DD HH:mm UTC ZZ'))
    await ctx.message.channel.send(embed=r_embed)

@client.command(aliases=['convertfromzone','cfz'])
async def convertfromtimezone(ctx,hour,min,cfrom,cto):
    def error_zone(error):
        e_embed = discord.Embed(
            title="Invalid Timezone!",
            description="You have may have entered a invalid timezone, if you are sure that the timezone is correct, try entering it in it's" +
                        " short or long form, for example if you entered EDT, enter Eastern Daylight Time, and if you entered Eastern Standard Time enter" +
                        " EST. Another important thing to keep in mind is Daylight Savings, for example in Toronto if daylight savings is active, we use EDT" +
                        "(Eastern Daylight Time) but normally we use EST (Eastern Standard Time). If you were to enter EST, when daylight savings is active, " +
                        "The time will be 1 hour off. The same goes for the other timezones that have Daylight Savings or something similar. " +
                        "This command also works with UTC, you can enter something like 'UTC-5' which is EST, or 'UTC-4' which is EDT, The same goes for GMT-5/GMT-4. " +
                        "This module is still a bit finicky so if there are bugs, rest assured that I am working on fixing it",
            colour=hc
        )
        e_embed.set_footer(text=df)
        e_embed.add_field(name="Error:", value=str(error))
        return e_embed
    if ' ' in cfrom:
        cfrom = cfrom.title()
    else:
        cfrom = cfrom.upper()
    if ' ' in cto:
        cto = cto.title()
    else:
        cto = cto.upper()
    t_utc = arrow.utcnow()
    try:
        t_time_date = t_utc.to(cfrom)
    except Exception as e:
        await ctx.message.channel.send(embed=error_zone(e))
        return
    if len(hour) == 1:
        hour = '0' + hour
    if len(min) == 1:
        hour = '0' + hour
    format_for_get = t_time_date.format('YYYY-MM-DD') + ' ' + hour + ':' + min + ':00' + t_time_date.format('ZZ')
    c_time = arrow.get(format_for_get)
    try:
        current_to = c_time.to(cto)
    except Exception as e:
        await ctx.message.channel.send(embed=error_zone(e))
        return
    r_embed = discord.Embed(
        title=f"Here is the {str(hour)}:{str(min)} {cfrom} in {cto}",
        colour=hc
    )
    r_embed.set_footer(text=df)
    r_embed.add_field(name="Time in {}:".format(cto),value=current_to.format('YYYY-MM-DD HH:mm UTC ZZ'))
    await ctx.message.channel.send(embed=r_embed)

@client.command()
async def google(ctx,*,question):
    msg_list = []
    async def delete_message():
        for message in msg_list:
            await message.delete(delay=30)
    msg_list.append(ctx.message)
    for j in search(question, tld="co.in", num=10, stop=1, pause=0.9):
        result = j
    msg_list.append(await ctx.message.channel.send(f'Google Search Result For "{question}": {result}'))
    msg_list.append(await ctx.message.channel.send("Do you want more results? If you do, type the number of results (maximum of 5) you want below. If you don't type 'quit' or wait 30 seconds"))
    def check(message):
        if message.author == ctx.message.author:
            return True
        else:
            return False
    try:
        result_num = await client.wait_for('message', check=check, timeout=30)
        await result_num.delete(delay=30)
        if result_num.content == 'quit':
            msg_list.append(await ctx.message.channel.send('Request Quit!'))
            await delete_message()
            return
    except:
        msg_list.append(await ctx.message.channel.send("Request Timed Out"))
        await delete_message()
        return
    try:
        result_num = int(result_num.content)
    except:
        msg_list.append(await ctx.message.channel.send("That isn't a number! Request Timed Out"))
        await delete_message()
        return
    if result_num > 5:
        msg_list.append(await ctx.message.channel.send("Discord will only show a maximum of 5 results."))
        result_num = 5
    result_list = []
    for j in search(question, tld="co.in", num=10, stop=result_num, pause=1.8):
        result_list.append(j)
    result = '  |  '.join(x for x in result_list)
    msg_list.append(await ctx.message.channel.send(f'Google Search Result For "{question}": {result}'))
    await delete_message()

@client.command()
async def translate(ctx,*,text):
    LANGUAGES = json.loads(urllib.request.urlopen(
        "https://raw.githubusercontent.com/BLANK-TH/elevator-bot-resources/bot-storage/languages.json").read())
    translator = Translator()
    translated = translator.translate(text)
    embed = discord.Embed(
        title="Translation Completed",
        colour=hc
    )
    embed.add_field(name="Translated Text:",value=translated.text,inline=False)
    embed.add_field(name="Pronunciation:",value=translated.pronunciation,inline=True)
    embed.add_field(name="Source Language (Auto-Detected):",value=f"{LANGUAGES[translated.src.lower()]} ({translated.src.lower()})",inline=True)
    embed.add_field(name="Destination Language:",value=f"{LANGUAGES[translated.dest.lower()]} ({translated.dest.lower()})",inline=True)
    embed.set_footer(text=df)

    await ctx.message.channel.send(embed=embed)

@client.command()
async def translateto(ctx,languageto,*,text):
    LANGUAGES = json.loads(urllib.request.urlopen(
        "https://raw.githubusercontent.com/BLANK-TH/elevator-bot-resources/bot-storage/languages.json").read())
    translator = Translator()
    try:
        translated = translator.translate(text,dest=languageto)
    except Exception as e:
        embed = discord.Embed(title="The language you mentioned doesn't exist!", colour=discord.Colour.red())
        embed.add_field(name="Supported Languages:",value="https://pastebin.com/LMuNGwAK")
        embed.add_field(name="Error:", value=str(e))
        await ctx.message.channel.send(embed=embed)
        return
    embed = discord.Embed(
        title="Translation Completed",
        colour=hc
    )
    embed.add_field(name="Translated Text:", value=translated.text, inline=False)
    embed.add_field(name="Pronunciation:", value=translated.pronunciation, inline=True)
    embed.add_field(name="Source Language (Auto-Detected):",value=f"{LANGUAGES[translated.src.lower()]} ({translated.src.lower()})",inline=True)
    embed.add_field(name="Destination Language:",value=f"{LANGUAGES[translated.dest.lower()]} ({translated.dest.lower()})",inline=True)
    embed.set_footer(text=df)

    await ctx.message.channel.send(embed=embed)

@client.command()
async def translatefrom(ctx,languagefrom,*,text):
    LANGUAGES = json.loads(urllib.request.urlopen(
        "https://raw.githubusercontent.com/BLANK-TH/elevator-bot-resources/bot-storage/languages.json").read())
    translator = Translator()
    try:
        translated = translator.translate(text,src=languagefrom)
    except Exception as e:
        embed = discord.Embed(title="The language you mentioned doesn't exist!", colour=discord.Colour.red())
        embed.add_field(name="Supported Languages:",value="https://pastebin.com/LMuNGwAK")
        embed.add_field(name="Error:", value=str(e))
        await ctx.message.channel.send(embed=embed)
        return
    embed = discord.Embed(
        title="Translation Completed",
        colour=hc
    )
    embed.add_field(name="Translated Text:", value=translated.text, inline=False)
    embed.add_field(name="Pronunciation:", value=translated.pronunciation, inline=True)
    embed.add_field(name="Source Language:",value=f"{LANGUAGES[translated.src.lower()]} ({translated.src.lower()})",inline=True)
    embed.add_field(name="Destination Language:",value=f"{LANGUAGES[translated.dest.lower()]} ({translated.dest.lower()})",inline=True)
    embed.set_footer(text=df)

    await ctx.message.channel.send(embed=embed)

@client.command(aliases=['backname','bn'])
async def backwardsname(ctx,*,user:discord.Member="None"):
    if user == "None":
        user = ctx.message.author
    name = user.display_name
    backwards_name = ''.join(reversed(name))
    embed = discord.Embed(
        title=backwards_name,
        colour=hc
    )
    embed.add_field(name="Original Name:",value=name)
    embed.set_footer(text=df)

    await ctx.message.channel.send(embed=embed)

@client.command(aliases=['prune'])
@commands.has_permissions(manage_messages=True)
async def purge(ctx,number="None"):
    if number == "None":
        embed = discord.Embed(title="Please enter a number!",colour=discord.Colour.red())
        embed.set_image(url='https://i.imgur.com/XgqWMei.jpg')
        embed.set_footer(text=df)
    elif number != "None":
        try:
            num = int(number)
            con = True
        except ValueError as e:
            embed = discord.Embed(title="Please enter a number!", colour=discord.Colour.red())
            embed.set_image(url='https://i.imgur.com/XgqWMei.jpg')
            embed.add_field(name="Error:", value=str(e))
            embed.set_footer(text=df)
            con = False
        if con:
            await ctx.message.delete()
            await ctx.message.channel.purge(limit=num)
            embed = discord.Embed(title="Purge Success!", colour=discord.Colour.green())
            embed.add_field(name="Number of Messages",value=number)
            embed.add_field(name="Command Author",value=ctx.message.author.display_name)
            embed.set_footer(text=df)
    message = await ctx.message.channel.send(embed=embed)
    await message.delete(delay=7)

@client.command()
async def spam(ctx,num:int,*,message):
    if not ctx.message.author.id == 616032766974361640:
        msg = await ctx.message.channel.send("The spam command can only be used by the bot owner a.k.a. **NOT YOU**")
        await msg.delete(delay=30)
        return
    await ctx.message.delete()
    for x in range(0,num):
        await ctx.message.channel.send(message)
        await asyncio.sleep(0.9)

@client.command()
async def fastspam(ctx,num:int,*,message):
    if not ctx.message.author.id == 616032766974361640:
        msg = await ctx.message.channel.send("The spam command can only be used by the bot owner a.k.a. **NOT YOU**")
        await msg.delete(delay=30)
        return
    await ctx.message.delete()
    for x in range(0,num):
        await ctx.message.channel.send(message)

@client.command()
async def latency(ctx):
    current_ping = round(client.latency * 1000)
    embed = discord.Embed(
        title="Here is the current ping for the Elevator Server Bot",
        colour=hc
    )
    embed.set_footer(text=df)
    embed.add_field(name="Ping:",value=str(current_ping) + 'ms')

    await ctx.message.channel.send(embed=embed)

@client.command()
async def laugh(ctx):
    random_laugh_gif = ['https://i.imgur.com/hfBNc9K.jpg',
                        'https://i.imgur.com/wmpKu8K.jpg',
                        'https://i.imgur.com/Fc6Rpu7.gif'
                        ]
    lg = choice(random_laugh_gif)
    l_embed = discord.Embed(
        description=f'{ctx.message.author.mention} is laughing!',
        colour=hc
    )
    l_embed.set_footer(text=df)
    l_embed.set_image(url=lg)

    await ctx.message.channel.send(embed=l_embed)

@client.command()
async def stare(ctx,*,user:discord.Member='themselves?!?'):
    s_embed = discord.Embed(
        description=f'{ctx.message.author.mention} is staring at {user.mention}!',
        colour=hc
    )
    s_embed.set_footer(text=df)
    s_embed.set_image(url='https://i.ibb.co/XpNb1s9/stare.gif')

    await ctx.message.channel.send(embed=s_embed)

@client.command()
async def rankthot(ctx,*,user:discord.Member=None):
    if user is None:
        user = ctx.message.author
    if user.id == 616032766974361640:
        thot_level = 0
    elif user.id == 514835126220226580 or user.id == 429504383529517056:
        thot_level = 100
    else:
        thot_level = randint(0,100)
    title = "Thotties be thotting"
    message = f"{user.mention} is **{str(thot_level)}%**"
    if thot_level >= 75:
        embed = discord.Embed(
            title=title,
            description=message,
            colour=discord.Colour.red()
        )
    elif thot_level >= 50:
        embed = discord.Embed(
            title=title,
            description=message,
            colour=discord.Colour.gold()
        )
    else:
        embed = discord.Embed(
            title=title,
            description=message,
            colour=discord.Colour.green()
        )
    embed.set_footer(text=df)

    await ctx.message.channel.send(embed=embed)

@client.command()
async def deathbattle(ctx,user1,user2=None):
    if user2 is None:
        user2 = ctx.guild.get_member(int(user1.replace("<@", "").replace(">", "").replace("!",""))).display_name
        user1 = ctx.message.author.display_name
    else:
        try:
            user1 = ctx.guild.get_member(int(user1.replace("<@","").replace(">","").replace("!",""))).display_name
        except:
            pass
        try:
            user2 = ctx.guild.get_member(int(user2.replace("<@", "").replace(">", "").replace("!", ""))).display_name
        except:
            pass
    p1tup = (user1, 100)
    p2tup = (user2, 100)
    turn = randint(1,2)
    embed = discord.Embed(
        title="Deathbattle Time!!!",
        description=f"Deathbattle between **{user1}** and **{user2}**! {p1tup[0] if turn == 1 else p2tup[0]} goes first.",
        colour=discord.Colour.blue()
    )
    embed.set_footer(text=df)
    embed.add_field(name=p1tup[0],value=f"{str(p1tup[1])}/100")
    embed.add_field(name=p2tup[0], value=f"{str(p2tup[1])}/100")
    show_msg = await ctx.message.channel.send(embed=embed)
    if "blank" in p1tup[0].lower() or "blank" in p2tup[0].lower():
        if "blank" in p1tup[0].lower():
            winner = p1tup[0]
            p2tup = (p2tup[0],"-∞")
            msg = "<:deathbattleright:700815518193680434> __{}__ sent his robot swarm dealing __∞__ dmg to __{}__!".format(p1tup[0],p2tup[0])
        else:
            winner = p2tup[0]
            p1tup = (p1tup[0],"-∞")
            msg = "<:deathbattleleft:700815578499121183> __{}__ sent his robot swarm dealing __∞__ dmg to __{}__!".format(p1tup[0],p2tup[0])
        embed = discord.Embed(
            description=msg + f"\n🏆 **{winner}** has won!",
            colour=discord.Colour.gold()
        )
        embed.set_footer(text=df)
        embed.add_field(name=f"{p1tup[0]}:", value=str(p1tup[1]))
        embed.add_field(name=f"{p2tup[0]}:", value=str(p2tup[1]))
        await show_msg.edit(embed=embed)
        return
    elif "pidge" in p1tup[0].lower() or "pidge" in p2tup[0].lower() or "yuki" in p1tup[0].lower() or \
            "yuki" in p2tup[0].lower() or "ducky" in p1tup[0].lower() or "ducky" in p2tup[0].lower():
        if "pidge" in p1tup[0].lower() or "yuki" in p1tup[0].lower() or "ducky" in p1tup[0].lower():
            winner = p1tup[0]
            p2tup = (p2tup[0],"-∞")
            msg = "<:deathbattleright:700815518193680434> __{}__ sends her demonic wrath after __{}__ making you suffer slowly to your demise!".format(p1tup[0],p2tup[0])
        else:
            winner = p2tup[0]
            p1tup = (p1tup[0],"-∞")
            msg = "<:deathbattleleft:700815578499121183> __{}__ sends her demonic wrath after __{}__ making you suffer slowly to your demise!".format(p1tup[0],p2tup[0])
        embed = discord.Embed(
            description=msg + f"\n🏆 **{winner}** has won!",
            colour=discord.Colour.gold()
        )
        embed.set_footer(text=df)
        embed.add_field(name=f"{p1tup[0]}:", value=str(p1tup[1]))
        embed.add_field(name=f"{p2tup[0]}:", value=str(p2tup[1]))
        await show_msg.edit(embed=embed)
        return
    # make sure in responses, the person who is hitting is first, victim is second, damage is third
    responses = [
        "__{}__ shocks __{}__ with lightning for __{}__ dmg!",
        "__{}__ explodes a bomb on __{}__ for __{}__ dmg!",
        "__{}__ explodes a nuclear bomb on __{}__ for __{}__ dmg!",
        "__{}__ runs over __{}__ with a car for __{}__ dmg!",
        "__{}__ runs over __{}__ with a truck for __{}__ dmg!",
        "__{}__ assigns a echelon to kill __{}__, you manage to get away but suffer __{}__ dmg!",
        "__{}__ shoots __{}__ with a AR for __{}__ dmg!",
        "__{}__ shoots __{}__ with a HG for __{}__ dmg!",
        "__{}__ shoots __{}__ with a MG for __{}__ dmg!",
        "__{}__ shoots __{}__ with a RF for __{}__ dmg!",
        "__{}__ shoots __{}__ with a SG for __{}__ dmg!",
        "__{}__ shoots __{}__ with a SMG for __{}__ dmg!",
        "__{}__ slices __{}__ with a sword for __{}__ dmg!",
        "__{}__ hits __{}__ with a whip for __{}__ dmg!",
        "__{}__ slaps __{}__ for __{}__ dmg!",
        "__{}__ punches __{}__ for __{}__ dmg!",
        "__{}__ smacks __{}__ with a chair for __{}__ dmg!",
        "__{}__ bonks __{}__ with a bat for __{}__ dmg!",
        "__{}__ tortures __{}__ for __{}__ dmg!",
        "__{}__ karate chops __{}__ for __{}__ dmg!",
        "__{}__ kicks __{}__ for __{}__ dmg!",
        "__{}__ burns __{}__ for __{}__ dmg!",
        "__{}__ smacks __{}__ with a hammer for __{}__ dmg!",
        "__{}__ fires a torpedo at __{}__ for __{}__ dmg!",
        "__{}__ fires a canonball at __{}__ and dealt __{}__ dmg!",
        "__{}__ smacks __{}__ on the head with a ban and dealt __{}__ dmg!",
        "__{}__ casts the stupefy charm on __{}__ and dealt __{}__ dmg!",
        "__{}__ casts the expelliarmus charm on __{}__ and dealt __{}__ dmg!"
    ]
    past_responses = []
    def check_win(p1life,p2life):
        if p1life <= 0:
            return 2
        if p2life <= 0:
            return 1
        return 0
    def cur_stat(p1tup,p2tup,turn,dmg):
        temp_msg = choice(responses)
        if turn == 1:
            past_responses.append("<:deathbattleright:700815518193680434> " + temp_msg.format(f"**{p1tup[0]}**",f"**{p2tup[0]}**",f"**{str(dmg)}**"))
            if len(past_responses) > 3:
                del past_responses[0]
            msg = '\n'.join(x for x in past_responses)
            embed = discord.Embed(
                description=msg,
                colour=discord.Colour.green()
            )
        else:
            past_responses.append("<:deathbattleleft:700815578499121183> " + temp_msg.format(f"**{p2tup[0]}**",f"**{p1tup[0]}**",f"**{str(dmg)}**"))
            if len(past_responses) > 3:
                del past_responses[0]
            msg = '\n'.join(x for x in past_responses)
            embed = discord.Embed(
                description=msg,
                colour=discord.Colour.red()
            )
        embed.set_footer(text=df)
        embed.add_field(name=f"{p1tup[0]}:",value=str(p1tup[1]))
        embed.add_field(name=f"{p2tup[0]}:",value=str(p2tup[1]))
        past_responses.append(past_responses.pop().replace("**",""))
        return (embed,dmg)
    await asyncio.sleep(1.8)

    while check_win(p1tup[1],p2tup[1]) == 0:
        dmg = randint(0, 35)
        if turn == 1:
            p2tup = (p2tup[0],p2tup[1]-dmg)
        else:
            p1tup = (p1tup[0], p1tup[1] - dmg)
        stat = cur_stat(p1tup, p2tup, turn,dmg)
        await show_msg.edit(embed=stat[0])
        if turn == 1:
            turn = 2
        else:
            turn = 1
        await asyncio.sleep(2.3)

    if check_win(p1tup[1],p2tup[1]) == 1:
        winner = p1tup[0]
    else:
        winner = p2tup[0]
    past_responses.append(f"🏆 **{winner}** has won!")
    if len(past_responses) > 3:
        del past_responses[0]
    msg = '\n'.join(x for x in past_responses)
    embed = discord.Embed(
        description=msg,
        colour=discord.Colour.gold()
    )
    embed.set_footer(text=df)
    embed.add_field(name=f"{p1tup[0]}:", value=str(p1tup[1]))
    embed.add_field(name=f"{p2tup[0]}:", value=str(p2tup[1]))
    await show_msg.edit(embed=embed)

@client.command()
async def userinfo(ctx,*,user:discord.Member):
    embed = discord.Embed(
        description=user.mention,
        colour=hc
    )
    embed.set_thumbnail(url=user.avatar_url)
    embed.set_author(name=user.name + '#' + user.discriminator,icon_url=user.avatar_url)
    embed.add_field(name="Username:",value=user.nick)
    embed.add_field(name="ID:",value=str(user.id))
    embed.add_field(name="Joined At:",value=user.joined_at.strftime("%Y-%m-%d %H:%M UTC"))
    embed.add_field(name="Created At:", value=user.created_at.strftime("%Y-%m-%d %H:%M UTC"))
    embed.add_field(name="Status:",value=user.status)
    embed.add_field(name="Display Colour:",value=f"RGB: {user.colour.to_rgb()}\nHEX: {str(user.colour)}")
    embed.add_field(name="Top Role:",value=user.top_role.name)
    embed.add_field(name="Bot:", value=user.bot)
    embed.add_field(name="System User:",value=user.system)
    roles = []
    for x in user.roles:
        roles.append(x.name)
    val = ', '.join(x for x in roles)
    embed.add_field(name="Roles:", value=val, inline=False)
    guildperms = user.guild_permissions
    key_perms = {"Administrator":guildperms.administrator,"Ban Members":guildperms.ban_members,
                 "Kick Members":guildperms.kick_members,"Manage Channels":guildperms.manage_channels,
                 "Manage Server":guildperms.manage_guild,"Manage Roles":guildperms.manage_roles,
                 "Manage Nicknames":guildperms.manage_nicknames,"Mute Members":guildperms.mute_members,
                 "Deafen Members":guildperms.deafen_members,"Move Members":guildperms.deafen_members}
    key_permissions = []
    for x,y in key_perms.items():
        if y:
            key_permissions.append(x)
    if len(key_permissions) == 0:
        key_permissions = ["None"]
    key_perm = ", ".join(x for x in key_permissions)
    embed.add_field(name="Key Permissions:",value=key_perm,inline=False)
    embed.set_footer(text=df)

    await ctx.message.channel.send(embed=embed)

@client.command()
async def outsideuserinfo(ctx,id:int):
    user = await client.fetch_user(id)
    embed = discord.Embed(
        colour=hc
    )
    embed.set_thumbnail(url=user.avatar_url)
    embed.set_author(name=user.name + '#' + user.discriminator, icon_url=user.avatar_url)
    embed.add_field(name="ID:", value=str(user.id))
    embed.add_field(name="Created At:", value=user.created_at.strftime("%Y-%m-%d %H:%M UTC"))
    embed.add_field(name="Bot:", value=user.bot)
    embed.set_footer(text=df)

    await ctx.message.channel.send(embed=embed)

@client.command()
async def shiprate(ctx,user1:str,user2:str):
    try:
        user1 = ctx.message.author.guild.get_member(int(user1.replace("<@!", "").replace(">", ""))).display_name
    except:
        pass
    try:
        user2 = ctx.message.author.guild.get_member(int(user2.replace("<@!", "").replace(">", ""))).display_name
    except:
        pass
    rate = randint(0,100)
    bar_full = "<:shipratefull:701950795649777736>"
    bar_empty = "<:shiprateempty:701950795947704340>"
    cur_num = round(rate/10)
    empty_num = 10 - cur_num
    descrip_msg = f"💗 **MATCHMAKING** 💗\n🔻 *`{user1}`*\n🔺 *`{user2}`*"
    bar_msg = ""
    for x in range(0,cur_num):
        bar_msg += bar_full
    for x in range(0,empty_num):
        bar_msg += bar_empty
    if cur_num == 10:
        expression = "Perfect! 💯"
    elif cur_num > 8:
        expression = "Great! 😃"
    elif cur_num > 6:
        expression = "Not Bad! 🙂"
    elif cur_num > 4:
        expression = "Ok... 🙁"
    elif cur_num > 2:
        expression = "Horrible! 😢"
    else:
        expression = "Impossible... 😭"
    embed_msg = f"**{str(rate)}%** {bar_msg} {expression}"
    embed = discord.Embed(
        description=embed_msg,
        colour=0xff81d2
    )

    await ctx.message.channel.send(content=descrip_msg,embed=embed)

@client.command(aliases=['hellodarkness','hdmof'])
async def hellodarknessmyoldfriend(ctx):
    await ctx.message.channel.send("https://www.youtube.com/watch?v=qYS0EeaAUMw&t=3")

@client.command(aliases=['animemoji','ae'])
async def animatedemoji(ctx,*,emoji_name):
    def similar(a,b):
        return SequenceMatcher(None,a,b).ratio()
    emoji_similaritys = {}
    for emoji in ctx.guild.emojis:
        if emoji.animated:
            emoji_similaritys[similar(emoji_name,emoji.name)] = emoji
    highest_emoji = max([*emoji_similaritys]),emoji_similaritys[max([*emoji_similaritys])]
    if highest_emoji[0] < 0.1:
        await ctx.message.channel.send("Could not find any emojis that match `{}`".format(emoji_name))
        return
    await ctx.message.channel.send("<a:{}:{}>".format(highest_emoji[1].name,str(highest_emoji[1].id)))

@client.command(aliases=["bj"])
async def blackjack(ctx):
    def get_card(deck):
        first_len = len(deck.deck)
        card = deck.give_random_card()
        second_len = len(deck.deck)
        for x in range(0,first_len-second_len-1):
            deck.take_card(card)
        return card
    def get_emoji(value,suit):
        suit_values = {0:"S",1:"H",2:"D",3:"C"}
        suit_letter = suit_values[suit]
        for guild in client.guilds:
            for emoji in guild.emojis:
                if emoji.name == str(value) + suit_letter:
                    return "<:{}:{}>".format(emoji.name,str(emoji.id))
        return "Error: Emoji Not Found"
    def generate_deck(num_deck):
        deck_obj = deck_of_cards.DeckOfCards()
        for x in range(0,num_deck):
            deck_obj.add_deck()
        deck_obj.shuffle_deck()
        return deck_obj
    def get_value(hand):
        val = 0
        for card in hand:
            if card.value > 10:
                val += 10
                continue
            if card.value == 1:
                continue
            val += card.value
        for card in hand:
            if card.value == 1:
                if val + 11 <= 21:
                    val += 11
                    continue
                else:
                    val += 1
        return val
    def check_soft(hand):
        val = 0
        for card in hand:
            if card.value > 10:
                val += 10
                continue
            if card.value == 1:
                continue
            val += card.value
        status = []
        for card in hand:
            if card.value == 1:
                if val + 11 <= 21:
                    status.append(True)
                    val += 11
                else:
                    status.append(False)
                    val += 1
        for status in status:
            if status:
                return True
        return False
    def check(message):
        if (message.author == ctx.message.author and message.content.lower() == "hit") or (message.author == ctx.message.author and message.content.lower() == "stand"):
            return True
        return False
    def check_lose(hand):
        val = get_value(hand)
        if val > 21:
            return True
        return False
    def embed_gen(player,dealer,status):
        if status == "lost":
            colour = discord.Colour.red()
        elif status == "won":
            colour = discord.Colour.green()
        elif status == "tied":
            colour = discord.Colour.gold()
        else:
            status = "An Error Has Occured"
            colour = discord.Colour.dark_red()
        embed = discord.Embed(
            description="You {}!".format(status),
            colour=colour
        )
        embed.set_author(name=ctx.message.author.name + '#' + ctx.message.author.discriminator,
                         icon_url=ctx.message.author.avatar_url)
        embed.set_footer(text=df)
        player_emoji = " ".join(get_emoji(x.value, x.suit) for x in player)
        dealer_emoji = " ".join(get_emoji(x.value, x.suit) for x in dealer)
        player_value = str(get_value(player_hand))
        dealer_value = str(get_value(dealer_hand))
        if check_soft(player_hand):
            player_value = "Soft " + str(get_value(player_hand))
        if check_soft(dealer_hand):
            dealer_value = "Soft " + str(get_value(dealer_hand))
        if get_value(player_hand) == 21:
            player_value = "Blackjack"
        if get_value(dealer_hand) == 21:
            dealer_value = "Blackjack"
        embed.add_field(name="Your Hand:", value="{}\nValue: {}".format(player_emoji, player_value))
        embed.add_field(name="Dealer's Hand:", value="{}\nValue: {}".format(dealer_emoji, dealer_value))
        return embed
    player_hand = []
    dealer_hand = []
    deck = generate_deck(6)
    dealer_hand.append(get_card(deck))
    dealer_hand.append(get_card(deck))
    player_hand.append(get_card(deck))
    player_hand.append(get_card(deck))
    embed = discord.Embed(
        description="Type `hit` to draw another card or `stand` to pass. If you don't respond for 1 minute, you lose!",
        colour=discord.Colour.blue()
    )
    embed.set_author(name=ctx.message.author.name + '#' + ctx.message.author.discriminator, icon_url=ctx.message.author.avatar_url)
    embed.set_footer(text=df)
    player_emoji = " ".join(get_emoji(x.value,x.suit) for x in player_hand)
    dealer_emoji = get_emoji(dealer_hand[0].value,dealer_hand[0].suit) + " " + "<:blue_back:706507690054123561>"
    player_value = str(get_value(player_hand))
    dealer_value = str(dealer_hand[0].value)
    if dealer_hand[0].value > 10:
        dealer_value = "10"
    if check_soft(player_hand):
        player_value = "Soft " + str(get_value(player_hand))
    if check_soft(dealer_hand) and dealer_hand[0].value == 1:
        dealer_value = "Soft 11"
    embed.add_field(name="Your Hand:",value="{}\nValue: {}".format(player_emoji,player_value))
    embed.add_field(name="Dealer's Hand:",value="{}\nValue: {}".format(dealer_emoji,dealer_value))
    message = await ctx.message.channel.send(embed=embed)
    if check_lose(dealer_hand):
        await message.edit(embed=embed_gen(player_hand, dealer_hand,"won"))
        return
    if get_value(player_hand) == 21:
        await message.edit(embed=embed_gen(player_hand,dealer_hand,"won"))
        return
    if get_value(dealer_hand) == 21:
        await message.edit(embed=embed_gen(player_hand,dealer_hand,"lost"))
        return
    if check_lose(player_hand):
        await message.edit(embed=embed_gen(player_hand, dealer_hand,"lost"))
        return
    while True:
        try:
            choice = await client.wait_for("message",check=check,timeout=60)
        except asyncio.TimeoutError:
            await ctx.message.channel.send("You took more than 1 minute to answer, you lost!")
            return
        if choice.content.lower() == "stand":
            break
        player_hand.append(get_card(deck))
        if check_lose(player_hand):
            await message.edit(embed=embed_gen(player_hand,dealer_hand,"lost"))
            return
        if get_value(player_hand) == 21:
            await message.edit(embed=embed_gen(player_hand,dealer_hand,"won"))
            return
        if len(player_hand) >= 7:
            await message.edit(embed=embed_gen(player_hand,dealer_hand,"won"))
            return
        embed = discord.Embed(
            description="Type `hit` to draw another card or `stand` to pass. If you don't respond for 1 minute, you lose!",
            colour=discord.Colour.blue()
        )
        embed.set_author(name=ctx.message.author.name + '#' + ctx.message.author.discriminator,
                         icon_url=ctx.message.author.avatar_url)
        embed.set_footer(text=df)
        player_emoji = " ".join(get_emoji(x.value, x.suit) for x in player_hand)
        dealer_emoji = get_emoji(dealer_hand[0].value, dealer_hand[0].suit) + " " + "<:blue_back:706507690054123561>"
        player_value = str(get_value(player_hand))
        dealer_value = str(dealer_hand[0].value)
        if dealer_hand[0].value > 10:
            dealer_value = "10"
        if check_soft(player_hand):
            player_value = "Soft " + str(get_value(player_hand))
        if check_soft(dealer_hand) and dealer_hand[0].value == 1:
            dealer_value = "Soft 11"
        if get_value(player_hand) == 21:
            await message.edit(embed=embed_gen(player_hand, dealer_hand, "won"))
            return
        embed.add_field(name="Your Hand:", value="{}\nValue: {}".format(player_emoji, player_value))
        embed.add_field(name="Dealer's Hand:",value="{}\nValue: {}".format(dealer_emoji,dealer_value))
        await message.edit(embed=embed)
    while get_value(dealer_hand) < 17:
        dealer_hand.append(get_card(deck))
        if check_lose(dealer_hand):
            await message.edit(embed=embed_gen(player_hand,dealer_hand,"won"))
            return
        if get_value(dealer_hand) == 21:
            await message.edit(embed=embed_gen(player_hand,dealer_hand,"lost"))
            return
        if len(dealer_hand) >= 7:
            await message.edit(embed=embed_gen(player_hand, dealer_hand, "lost"))
            return
        embed = discord.Embed(
            description="Dealer is playing!",
            colour=discord.Colour.orange()
        )
        embed.set_author(name=ctx.message.author.name + '#' + ctx.message.author.discriminator,
                         icon_url=ctx.message.author.avatar_url)
        embed.set_footer(text=df)
        player_emoji = " ".join(get_emoji(x.value, x.suit) for x in player_hand)
        dealer_emoji = " ".join(get_emoji(x.value, x.suit) for x in dealer_hand)
        player_value = str(get_value(player_hand))
        dealer_value = str(get_value(dealer_hand))
        if check_soft(player_hand):
            player_value = "Soft " + str(get_value(player_hand))
        if check_soft(dealer_hand):
            dealer_value = "Soft " + str(get_value(dealer_hand))
        if get_value(player_hand) == 21:
            player_value = "Blackjack"
        if get_value(dealer_hand) == 21:
            dealer_value = "Blackjack"
        embed.add_field(name="Your Hand:", value="{}\nValue: {}".format(player_emoji, player_value))
        embed.add_field(name="Dealer's Hand:", value="{}\nValue: {}".format(dealer_emoji, dealer_value))
        await message.edit(embed=embed)
        await asyncio.sleep(1)
    if get_value(dealer_hand) == get_value(player_hand):
        await message.edit(embed=embed_gen(player_hand, dealer_hand, "tied"))
        return
    winning_value = min([get_value(player_hand),get_value(dealer_hand)],key=lambda list_value : abs(list_value - 21))
    if winning_value == get_value(player_hand):
        await message.edit(embed=embed_gen(player_hand, dealer_hand,"won"))
        return
    await message.edit(embed=embed_gen(player_hand, dealer_hand,"lost"))
    return

@client.command()
async def version(ctx):
    await ctx.message.channel.send("Elevator Bot is currently at {}".format(
        df.replace(" Developed By: BLANK","").replace("Elevator Server Bot ","")))

@client.command()
async def impersonate(ctx,username,*,message):
    await ctx.message.delete()
    def similar(a,b):
        return SequenceMatcher(None,a,b).ratio()
    user_similarities = {}
    for user in ctx.guild.members:
        if username.replace("<@","").replace(">","").replace("!","").isdigit():
            user_similarities[similar(username.replace("<@","").replace(">","").replace("!",""), str(user.id))] = user
            continue
        con = True
        for letter in username:
            if letter.lower() not in user.display_name.lower():
                con = False
        if con:
            user_similarities[similar(username.lower(), user.display_name.lower())] = user
    if len(user_similarities) <= 0:
        await ctx.message.channel.send("Could not find any users that match `{}`".format(username))
        return
    highest_user = max([*user_similarities]), user_similarities[max([*user_similarities])]
    if highest_user[0] < 0.1:
        await ctx.message.channel.send("Could not find any users that match `{}`".format(username))
        return
    user = highest_user[1]
    if user.id in [616032766974361640,699677108607123548,733474240854097920]:
        await ctx.message.channel.send("{} you are not allowed to impersonate {}!".format(ctx.message.author.mention,user.display_name))
        return
    webhook = None
    for hook in await ctx.message.channel.webhooks():
        if hook.user.id == 699677108607123548:
            webhook = hook
            break
    if webhook is None:
        webhook = await ctx.message.channel.create_webhook(name="Elevator Bot Webhook")
    await webhook.send(content=message,username=user.display_name,avatar_url=user.avatar_url)

@client.command()
async def usersend(ctx,*,details):
    # Generate random placeholder for backslash escape code to avoid someone finding out and it glitching
    escape_key = str(urandom(48))
    detail_list = details.replace("\|",escape_key).split("|")
    if len(detail_list) == 2:
        name = detail_list[0]
        message = detail_list[1].replace(escape_key,"|")
        avatar = None
    elif len(detail_list) == 3:
        name = detail_list[0]
        message = detail_list[1].replace(escape_key,"|")
        avatar = detail_list[2]
    else:
        await ctx.message.delete()
        await ctx.message.channel.send("You passed the incorrect number of parameters!")
        return
    if len(ctx.message.attachments) >= 1:
        avatar = ctx.message.attachments[0].url
    supported_image_extension = ["JPEG","JPG","GIF","WEBM","BMP","TIFF","PNG"]
    if not avatar is None:
        con = False
        for extension in supported_image_extension:
            if extension.lower() in avatar:
                con = True
                break
        if not con:
            await ctx.message.channel.send("The avatar link is not in the correct format. Supported formats are {}".format(
                ", ".join("." + x for x in supported_image_extension)
            ))
            await ctx.message.delete()
            return
    webhook = None
    for hook in await ctx.message.channel.webhooks():
        if hook.user.id == 699677108607123548:
            webhook = hook
            break
    if webhook is None:
        webhook = await ctx.message.channel.create_webhook(name="Elevator Bot Webhook")
    await webhook.send(content=message, username=name, avatar_url=avatar)
    await ctx.message.delete()

@client.command(aliases=["jm"])
async def jeopardymusic(ctx):
    await ctx.message.channel.send("https://www.youtube.com/watch?v=0Wi8Fv0AJA4")

@client.command()
async def disagree(ctx,user:discord.Member="None"):
    if user != "None":
        msg = f"{ctx.message.author.mention} disagrees with what {user.mention} said!"
    else:
        msg = f"{ctx.message.author.mention} disagrees with what was said!"
    a_embed = discord.Embed(
        description=msg,
        colour=hc
    )
    a_embed.set_footer(text=df)
    a_embed.set_image(url="https://i.imgur.com/ErwNJw3.jpg")

    await ctx.message.channel.send(embed=a_embed)

@client.command()
async def celebratemusic(ctx):
    await ctx.message.channel.send("https://www.youtube.com/watch?v=UWLIgjB9gGw")

@client.command()
async def sillyname(ctx,user:discord.Member=None):
    url = urllib.request.urlopen("https://raw.githubusercontent.com/bevacqua/correcthorse/master/wordlist.json")
    words = json.loads(url.read())
    if user is None:
        orig_nick = ctx.message.author.display_name
    else:
        orig_nick = user.display_name
    while True:
        name = choice(words).title() + " " + choice(words).title()
        if not len(name) > 32:
            break
    if user is not None:
        staff_role = get(ctx.guild.roles, id=725082640507469845)
        if staff_role in ctx.message.author.roles:
            try:
                await user.edit(nick=name)
            except discord.errors.Forbidden:
                await ctx.message.channel.send("My role isn't high enough to change your nickname!")
                return
            await ctx.message.channel.send(
                "`{}`'s nickname has been changed to `{}`! Their original name was `{}`".format(user.name,name, str(orig_nick)))
            return
        else:
            await ctx.message.channel.send("You do not have permissions to change someone else's nickname! Only Staff"
                                           " can do this.")
            return
    try:
        await ctx.message.author.edit(nick=name)
    except discord.errors.Forbidden:
        await ctx.message.channel.send("My role isn't high enough to change your nickname!")
        return
    await ctx.message.channel.send("You nickname has been changed to `{}`! If you would like to change it back, "
                                   "your original name was `{}`".format(name,str(orig_nick)))

@client.command()
async def redalert(ctx,*,reason=None):
    if reason is None:
        embed = discord.Embed(
            title="RED ALERT!!! RED ALERT!!! RED ALERT!!!",
            colour=discord.Colour.red()
        )
    else:
        embed = discord.Embed(
            title="RED ALERT!!! RED ALERT!!! RED ALERT!!!",
            description=reason,
            colour=discord.Colour.red()
        )
    embed.set_footer(text=df)
    embed.set_image(url="https://media1.tenor.com/images/5711e293284d2912a5bdec8b9997a2f0/tenor.gif?itemid=14378764")

    await ctx.message.channel.send(embed=embed)

@client.command()
async def mega(ctx):
    url = urllib.request.urlopen("https://raw.githubusercontent.com/bevacqua/correcthorse/master/wordlist.json")
    words = json.loads(url.read())
    await ctx.message.channel.send("MEGA{}".format(choice(words).upper()))

@client.command()
async def ping(ctx, username):
    for x in ctx.guild.members:
        if username.lower() in x.display_name.lower():
            user = x
            await ctx.message.channel.send(f'Ding! {user.mention}')
            break

@client.command()
async def toothfairy(ctx):
    embed = discord.Embed(description="I am the toothfairy, thank you for your tooth. Here's some money in return!",colour=hc)
    embed.set_footer(text=df)
    embed.set_image(url="https://s.marketwatch.com/public/resources/images/MW-HT282_dollar_ZG_20191014195738.jpg")
    await ctx.message.channel.send(embed=embed)

@client.command()
async def basbot(ctx):
    if ctx.message.author.id != 616032766974361640:
        return
    async with ctx.channel.typing():
        def check(message):
            if message.author == ctx.message.author and message.channel == ctx.message.channel:
                return True
            return False
        await ctx.message.delete()
        while True:
            msg = await client.wait_for('message',check=check)
            await msg.delete()
            if msg.content == "stopasbot":
                break
            await ctx.message.channel.send(msg.content)

@client.command(aliases=["c"])
async def calculate(ctx,*,expression):
    try:
        result = eval(expression,{},{})
        await ctx.message.channel.send("The answer to `{}` is `{}`".format(expression,str(result)))
    except Exception as e:
        await ctx.message.channel.send("An error has occured, please ensure that you entered a valid expression!\n"
                                       "Error: `{}`".format(repr(e)))

@client.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx,user: discord.Member,*,reason=None):
    if user.id in [616032766974361640,707984419998269480]:
        await ctx.message.channel.send("You can't ban BLANK, you silly!")
        return
    log_channel = client.get_channel(725438062296826027)
    await ctx.message.delete()
    embed = discord.Embed(
        title="You were banned from the Elevator Discord Server",
        description = "If you feel that any punishment was un-justified or unreasonable feel free to contact The Owner by direct messaging him/her or "
                      "someone on the staff team or sending a email to blank at `blankdev.th@gmail.com`"
                      ", you may appeal once per month with a maximum of 5 times. Should you abuse this privilege you may have your punishment increased" +
                      " and/or blocked from appealing in any manner for foreseeable future. Once you are unbanned you may rejoin using: https://discord.gg/Cr43nuF",
        colour=discord.Colour.red()
    )
    embed.add_field(name="Banned By:",value=ctx.message.author,inline=False)
    embed.add_field(name="Reason:",value=reason,inline=False)
    embed.set_image(url='https://i.imgur.com/YXndYr3.png')
    embed.set_footer(text=df)
    try:
        await user.send(embed=embed)
    except Exception as e:
        await ctx.message.channel.send("The user could not be DMed, they were still banned regardless.",
                                       embed=discord.Embed(description=repr(e)))
    log_embed = discord.Embed(
        title="Someone was banned!",
        colour=hc
    )
    log_embed.add_field(name="Person Banned:",value=user.display_name)
    log_embed.add_field(name="Banned By:", value=ctx.message.author)
    log_embed.add_field(name="User ID:",value=user.id)
    log_embed.add_field(name="Reason:", value=reason, inline=False)
    log_embed.set_footer(text=df)
    await log_channel.send(embed=log_embed)
    confirm_embed = discord.Embed(
        title="Ban Succeeded",
        colour=discord.Colour.green()
    )
    confirm_embed.add_field(name="Person Banned:", value=user.display_name)
    confirm_embed.add_field(name="Banned By:", value=ctx.message.author)
    confirm_embed.add_field(name="Reason:", value=reason, inline=False)
    confirm_embed.set_footer(text=df)
    confirm = await ctx.message.channel.send(embed=confirm_embed)
    await ctx.guild.ban(user,delete_message_days=0)
    await confirm.delete(delay=7)

@client.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx,user: discord.Member,*,reason="None"):
    log_channel = client.get_channel(725438062296826027)
    await ctx.message.delete()
    embed = discord.Embed(
        title="You were kicked from the Elevator Discord Server",
        description = "Before you rejoin, please consider what you have done and note that punishments will increase should you" +
                      " continue to do this. Once you have calmed down you may rejoin using: https://discord.gg/Cr43nuF." +
                      " If you think that this kick was unjustified, DM The Owner or someone on the staff team or send a email to blank at `blankdev.th@gmail.com`",
        colour=discord.Colour.orange()
    )
    embed.add_field(name="Kicked By:",value=ctx.message.author)
    embed.add_field(name="Reason:",value=reason,inline=False)
    embed.set_image(url='https://i.imgur.com/KUdbyB6.png')
    embed.set_footer(text=df)
    try:
        await user.send(embed=embed)
    except Exception as e:
        await ctx.message.channel.send("The user could not be DMed, they were still kicked regardless.",
                                       embed=discord.Embed(description=repr(e)))
    log_embed = discord.Embed(
        title="Someone was kicked!",
        colour=hc
    )
    log_embed.add_field(name="Person Kicked:",value=user.display_name,)
    log_embed.add_field(name="Kicked By:", value=ctx.message.author)
    log_embed.add_field(name="User ID:", value=user.id)
    log_embed.add_field(name="Reason:", value=reason, inline=False)
    log_embed.set_footer(text=df)
    await log_channel.send(embed=log_embed)
    confirm_embed = discord.Embed(
        title="Kick Succeeded",
        colour=discord.Colour.green()
    )
    confirm_embed.add_field(name="Person Kicked:", value=user.display_name)
    confirm_embed.add_field(name="Kicked By:", value=ctx.message.author)
    confirm_embed.add_field(name="Reason:", value=reason, inline=False)
    confirm_embed.set_footer(text=df)
    confirm = await ctx.message.channel.send(embed=confirm_embed)
    await confirm.delete(delay=7)
    await ctx.guild.kick(user)

@client.command()
@commands.has_role("Staff")
async def warn(ctx,user: discord.Member,*,reason):
    log_channel = client.get_channel(725438062296826027)
    await ctx.message.delete()
    embed = discord.Embed(
        title="You were warned in the Elevator Discord Server",
        description = "You were warned by a moderator in the Elevator Discord Server, please consider your actions before we are forced to take further"+
        " steps. If you think that this warning was unjustified, DM The Owner or someone on the staff team or send a email to `blankdev.th@gmail.com`.",
        colour=discord.Colour.gold()
    )
    embed.add_field(name="Warned By:",value=ctx.message.author)
    embed.add_field(name="Reason:",value=reason,inline=False)
    embed.set_image(url='https://i.imgur.com/1x4hFjz.gif')
    embed.set_footer(text=df)
    try:
        await user.send(embed=embed)
    except Exception as e:
        await ctx.message.channel.send("The user could not be warned, they might have DM's disabled",
                                       embed=discord.Embed(description=repr(e)))
        return
    else:
        log_embed = discord.Embed(
            title="Someone was warned!",
            colour=hc
        )
        log_embed.add_field(name="Person Warned:",value=user.display_name)
        log_embed.add_field(name="Warned By:", value=ctx.message.author)
        log_embed.add_field(name="User ID:", value=user.id)
        log_embed.add_field(name="Reason:", value=reason, inline=False)
        log_embed.set_footer(text=df)
        await log_channel.send(embed=log_embed)
        confirm_embed = discord.Embed(
            title="Warn Succeeded",
            colour=discord.Colour.green()
        )
        confirm_embed.add_field(name="Person Warned:", value=user.display_name)
        confirm_embed.add_field(name="Warned By:", value=ctx.message.author)
        confirm_embed.add_field(name="Reason:", value=reason, inline=False)
        confirm_embed.set_footer(text=df)
        confirm = await ctx.message.channel.send(embed=confirm_embed)
        await confirm.delete(delay=7)

@client.command(aliases=['sleepy'])
async def sleep(ctx):
    random_sleep_image_gif = ['https://i.imgur.com/XBkPjvb.jpg',
                              'https://i.imgur.com/i6FufIO.png',
                              'https://i.imgur.com/G0SHasR.jpg',
                              'https://i.imgur.com/OKwtZY9.jpg',
                              'https://i.imgur.com/KUBa7EZ.jpg',
                              'https://i.imgur.com/TnGjMde.jpg',
                              'https://i.imgur.com/1LdbybH.png',
                              'https://i.ibb.co/Fx6bSBv/sleep5.gif'
                            ]
    random_sleep_message = [f'{ctx.message.author.mention} is sleepy!',
                            f'{ctx.message.author.mention} wants to go to sleep!',
                            f'Someone help persuade {ctx.message.author.mention} to go to sleep!',
                            f'You should go to sleep {ctx.message.author.mention}, staying up is bad for you!'
                            ]
    rsi = choice(random_sleep_image_gif)
    rsm = choice(random_sleep_message)
    s_embed = discord.Embed(
        description=rsm,
        colour=hc
    )
    s_embed.set_footer(text=df)
    s_embed.set_image(url=rsi)

    await ctx.message.channel.send(embed=s_embed)

@client.command(aliases=["fr"])
async def finerant(ctx):
    await ctx.message.channel.send("https://www.youtube.com/watch?v=aS0-P4JR9PU")

@client.command()
async def fakeban(ctx,user:discord.Member,*,reason="No reason provided"):
    async def arange(a,b,reverse=False):
        if reverse:
            for i in reversed(range(a, b)):
                yield(i)
            return
        for i in range(a,b):
            yield(i)
    if user.id in [616032766974361640,707984419998269480]:
        await ctx.message.channel.send("You can't ban BLANK, you silly!")
        return
    await ctx.message.delete()
    confirm_embed = discord.Embed(
        title="Ban In Progress",
        colour=discord.Colour.gold()
    )
    confirm_embed.add_field(name="Person Banned:", value=user.display_name)
    confirm_embed.add_field(name="Banned By:", value="MegaHeadache")
    confirm_embed.add_field(name="Reason:", value=reason, inline=False)
    confirm_embed.set_footer(text=df)
    confirm = await ctx.message.channel.send("Banning in 10...",embed=confirm_embed)
    async for x in arange(1,10,True):
        await confirm.edit(content="Banning in {}...".format(str(x)),embed=confirm_embed)
        await asyncio.sleep(1.5)
    new_embed = discord.Embed(
        title="Ban Succeeded",
        colour=discord.Colour.green()
    )
    new_embed.add_field(name="Person Banned:", value=user.display_name)
    new_embed.add_field(name="Banned By:", value="MegaHeadache")
    new_embed.add_field(name="Reason:", value=reason, inline=False)
    new_embed.set_footer(text=df)
    await confirm.edit(content="Banned",embed=new_embed)
    await asyncio.sleep(3)
    try:
        await user.send("Just Kidding!")
    except Exception as e:
        await ctx.message.channel.send("{} Just Kidding!".format(user.mention),
                                       embed=discord.Embed(description=repr(e)))
        return

@client.command()
async def minesweeper(ctx,difficulty="medium",x:int=5,y:int=5):
    if x > 12 or y > 12:
        await ctx.message.channel.send("The maximum size of the grid is 12 x 12")
        return
    if x < 5 or y < 5:
        await ctx.message.channel.send("The minimum size of the grid is 5 x 5")
        return
    generator = minesweeperPy.mineGen(x,y)
    difficulties = {"easy":(10,20),"medium":(20,30),"hard":(30,40)}
    try:
        percentage_mine = randint(difficulties[difficulty.lower()][0],difficulties[difficulty.lower()][1])/100
    except KeyError:
        await ctx.message.channel.send("Please enter a valid difficulty, `easy`,`medium`,`hard`.")
    num_mine = round(x * y * percentage_mine)
    grid = generator.generateGrid(num_mine)['grid']
    emojis = {
        ' ':'0️⃣','1': '1️⃣', '2': '2️⃣', '3': '3️⃣', '4': '4️⃣', '5': '5️⃣',
        '6': '6️⃣', '7': '7️⃣', '8': '8️⃣', '9': '9️⃣','M':'💣'}
    strings = []
    strings.append("Difficulty: {} | Percentage of Mines: {}% | Grid Size {} x {}".format(
        difficulty.upper(),round(percentage_mine*100),str(x),str(y)))
    for row in grid:
        row_string = ""
        for box in row:
            box = box.replace(box,"||{}||".format(emojis[box]))
            row_string += box
        strings.append(row_string)
    msg = "\n".join(row for row in strings)
    await ctx.message.channel.send(msg)

@client.command()
@commands.has_role("Staff")
async def vote(ctx,text,timetoreact, *emojis:typing.Union[discord.Emoji, str]):
    v_embed = discord.Embed(
        title="A New Vote has been Started!",
        description=f"Vote: {text}",
        colour=hc
    )
    v_embed.set_footer(text=df)
    v_embed.add_field(name="Vote Host:",value=ctx.message.author.display_name)
    v_embed.add_field(name="You have until:",value=timetoreact)

    msg = await ctx.message.channel.send(embed=v_embed)

    for emoji in emojis:
        await msg.add_reaction(emoji)

@client.command()
async def eraselogs(ctx):
    if ctx.message.author.id != 616032766974361640:
        await ctx.message.channel.send("This command can only be used by the bot developer!")
        return
    success_counter = 0
    fail_counter = 0
    async with ctx.message.channel.typing():
        for file in repo.get_git_tree("logs").tree:
            sha = file.sha
            path = file.path
            try:
                repo.delete_file(path,"LogFilesDeleteMSG{}".format(str(ctx.message.id)),sha,branch="logs")
            except Exception as e:
                print("Error: " + str(e))
                fail_counter += 1
                continue
            success_counter += 1
    await ctx.message.channel.send("{} files have been successfully deleted. {} files have failed.".format(
        str(success_counter),str(fail_counter)))

@client.command()
async def erasecommands(ctx):
    if ctx.message.author.id != 616032766974361640:
        await ctx.message.channel.send("This command can only be used by the bot developer!")
        return
    success_counter = 0
    fail_counter = 0
    async with ctx.message.channel.typing():
        for file in repo.get_git_tree("commands").tree:
            sha = file.sha
            path = file.path
            try:
                repo.delete_file(path,"CommandFilesDeleteMSG{}".format(str(ctx.message.id)),sha,branch="commands")
            except Exception as e:
                print("Error: " + str(e))
                fail_counter += 1
                continue
            success_counter += 1
    await ctx.message.channel.send("{} files have been successfully deleted. {} files have failed.".format(
        str(success_counter),str(fail_counter)))

@client.command()
async def messagecount(ctx,countintensive=None):
    if ctx.message.author.id != 616032766974361640:
        await ctx.message.channel.send("Unfortuanately this command is not available to anyone except the developer as"
                                       " this command is extremely resource heavy and needs to be regulated.")
        return
    await ctx.message.channel.send("I am currently processing the messages. Be warned that this could take more than"
                                   " 4 minutes since there are a lot of messages to process. Channels like logs will"
                                   " not be included in this count to minimize the processing time required."
                                   " To include channels like those add any letter after the command. For example"
                                   " `s!messagecount a`. To cancel say"
                                   " `cancel`. To continue say anything.")
    def check(message):
        if message.author == ctx.message.author:
            return True
        return False
    try:
        msg = await client.wait_for('message',check=check,timeout=50)
    except asyncio.TimeoutError:
        await ctx.message.channel.send("You took too long to respond, the command has been canceled.")
        return
    if msg.content.lower() == "cancel":
        await ctx.message.channel.send("Request canceled")
        return
    await ctx.message.channel.send("Processing....")
    channel_num = {}
    intensive_channels = [725438062296826027,725085898160734271,685918906564608055,733442253669793902,
                          688457344664731649,695741363244761139,723275389115564133,735895556093902911,685932859097350160,
                          686693349545213977]
    async with ctx.message.channel.typing():
        for channel in ctx.guild.text_channels:
            if countintensive is None and channel.id in intensive_channels:
                continue
            channel_num[channel.name] = 0
            async for x in channel.history(limit=None):
                channel_num[channel.name] += 1
        total = 0
        for x in channel_num.values():
            total += x
        val = "Total: {}\n".format(str(total)) + '\n'.join(x + " : " + str(y) for x,y in channel_num.items())
        val += "\n\n\nExcluded Channel IDs: {}".format(", ".join(str(x) for x in intensive_channels))
        url = repo.create_file("ChannelListForMessageCountRequestMSG{}.txt".format(
        str(ctx.message.id)),
        "Requester ID: {} | Requester Name + Discriminator {}#{} | Message ID: {} | Message Link: {} | At: {}".format(
            str(ctx.message.author.id), ctx.message.author.name,
            ctx.message.author.discriminator, str(ctx.message.id), ctx.message.jump_url,
            ctx.message.created_at.strftime("%b %d %Y %H:%M UTC")),
        val,branch="commands")['content'].html_url
    await ctx.message.channel.send(embed=discord.Embed(
        description=f'Messages Per Channel In Server: [CLICK HERE]({url})',colour=hc))

@client.command()
async def captchagen(ctx,characters:int=5):
    url = urllib.request.urlopen("https://raw.githubusercontent.com/bevacqua/correcthorse/master/wordlist.json")
    words = json.loads(url.read())
    captcha_list = []
    async with ctx.message.channel.typing():
        for letter in choice(words).lower():
            captcha_list.append(letter)
        for num in str(randint(1000000, 1000000000)):
            captcha_list.append(num)
        captcha_text = ''.join(sample([x for x in captcha_list if x not in ["0","o","i","1","7"]], characters))
        print(captcha_text)
        img = ImageCaptcha()
        img_data = img.generate(captcha_text)
    await ctx.channel.send(file=discord.File(img_data,'captcha.png'))

@client.command(aliases=['r'])
async def report(ctx,user:discord.Member,*,reason):
    msgs = []
    staff_chat = client.get_channel(685919249864458386)
    staff_log = client.get_channel(725438062296826027)
    async def delete_msg():
        await asyncio.sleep(5)
        for msg in msgs:
            await msg.delete()
    msgs.append(ctx.message)
    embed = discord.Embed(
        title="Report",
        description=f"User Reported: {user.mention} | User Reporting: {ctx.message.author.mention}",
        colour=0xffb000
    )
    embed.set_footer(text=df)
    embed.add_field(name="Reportee Name + Discriminator:",value=f"{user.name}#{user.discriminator}")
    embed.add_field(name="Reportee ID:",value=user.id)
    embed.add_field(name="Reporter Name + Discriminator",value=f"{ctx.message.author.name}#{ctx.message.author.discriminator}")
    embed.add_field(name="Reporter ID:",value=ctx.message.author.id)
    embed.add_field(name="Report Channel Link:",value=ctx.message.channel.mention)
    embed.add_field(name="Report Channel ID:", value=ctx.message.channel.id)
    embed.add_field(name="Report Message Link:", value=ctx.message.jump_url)
    embed.add_field(name="Report Message ID:", value=ctx.message.id)
    embed.add_field(name="Report Reason:",value=reason)
    embed.add_field(name="Full Report Command:",value=ctx.message.content)
    cfrm_msg = await ctx.message.channel.send("Please react with a ✅ to confirm the report or a ❌ to cancel the report.",embed=embed)
    msgs.append(cfrm_msg)
    await cfrm_msg.add_reaction("✅")
    await cfrm_msg.add_reaction("❌")
    def check(reaction,user):
        return user == ctx.message.author
    reaction, user = await client.wait_for("reaction_add",check=check)
    if reaction.emoji == "❌":
        msgs.append(await ctx.message.channel.send("Report Canceled!"))
        await delete_msg()
        return
    msgs.append(await ctx.message.channel.send("Report Sent!"))
    await delete_msg()
    await staff_chat.send(embed=embed)
    await staff_log.send(embed=embed)

@client.command()
async def trivia(ctx):
    num_unicode = {1: '1️⃣', 2: '2️⃣', 3: '3️⃣', 4: '4️⃣', 5: '5️⃣', 6: '6️⃣', 7: '7️⃣', 8: '8️⃣', 9: '9️⃣'}
    api = Trivia(True)
    trivia = api.request(1,type_=Type.Multiple_Choice)["results"][0]
    answers = trivia['incorrect_answers']
    answers.append(trivia["correct_answer"])
    shuffle(answers)
    options = {}
    for index,option in enumerate(answers):
        options[num_unicode[index+1]] = option
    embed = discord.Embed(
        title = trivia['question'],
        description = "\n" + ("\n".join(x + ". " + y for x,y in options.items())),
        colour=hc
    )
    embed.set_footer(text=df)
    embed.set_author(name=ctx.message.author.name + '#' + ctx.message.author.discriminator,
                     icon_url=ctx.message.author.avatar_url)
    embed.add_field(name="Difficulty:",value=trivia["difficulty"].title())
    embed.add_field(name="Category:",value=trivia["category".replace("_","")])
    msg = await ctx.message.channel.send("You have 15 seconds to answer",embed=embed)
    for emoji in [*options]:
        await msg.add_reaction(emoji)
    def check(reaction,user):
        if user == ctx.message.author:
            return True
        return False
    try:
        reaction,user = await client.wait_for("reaction_add",check=check,timeout=15)
    except asyncio.TimeoutError:
        await ctx.message.channel.send("You took too long, the answer is `{}`".format(trivia["correct_answer"]))
        return
    if options[reaction.emoji] == trivia["correct_answer"]:
        await ctx.message.channel.send("You answered correctly, the answer is `{}`".format(trivia["correct_answer"]))
        return
    await ctx.message.channel.send("You answered incorrectly, the answer is `{}`. You answered `{}`".format(
        trivia["correct_answer"],options[reaction.emoji]))

@client.command(aliases=['qotd','qtd','questionotd','questionday'])
@commands.has_role("Staff")
async def questionoftheday(ctx,number:int,*,question):
    await ctx.message.delete()
    num_unicode= {1:'1️⃣',2:'2️⃣',3:'3️⃣',4:'4️⃣',5:'5️⃣',6:'6️⃣',7:'7️⃣',8:'8️⃣',9:'9️⃣'}
    emojis = []
    if number > 9:
        msg = await ctx.message.channel.send("Please put 9 or less choices.")
        await msg.delete(delay=10)
        return
    elif number < 2:
        msg = await ctx.message.channel.send("Please put 2 or more choices.")
        await msg.delete(delay=10)
        return
    for x in range(1,number + 1):
        emojis.append(num_unicode[x])
    creation_object = ctx.message.created_at
    creation_date = creation_object.strftime("%Y-%m-%d")
    creation_time = creation_object.strftime("%H:%M UTC")
    embed = discord.Embed(
        title="New Question of the Day!",
        description=f"**Question:** {question}",
        colour=hc
    )
    embed.set_footer(text=df)
    embed.add_field(name="Instructions:",
                    value="A question of the day is a daily (when possible) question that get's posted. These are all"
                    " hypothetical questions. This is optional and is just a fun activity to do, you don't have"
                    " to if you don't want to. If you do, pick which one you would pick by reacting with the"
                    " co-responding number.",
                    inline=False)
    embed.add_field(name="Date:",value=creation_date)
    embed.add_field(name="Time:",value=creation_time)
    msg = await ctx.message.channel.send(embed=embed)
    for emoji in emojis:
        await msg.add_reaction(emoji)

@client.command(aliases=['rc'])
async def reactioncount(ctx,message:discord.Message,bot_subtract="None"):
    await ctx.message.delete()
    reaction_list = message.reactions
    embed = discord.Embed(
        description=f"Reactions of message {str(message.id)}. If the bot"
                    f" reacted to the message, the reaction of any non-user account (bots)"
                    f" will be subtracted from the count. Add the parameter 'dns' to count the bot's reaction",
        colour=hc
    )
    embed.set_footer(text=df)
    embed.add_field(name="Message Link:", value=message.jump_url,inline=False)
    embed.add_field(name="Message ID:",value=str(message.id))
    embed.add_field(name="Channel ID:", value=str(message.channel.id))
    embed.add_field(name="Channel Link:",value=message.channel.mention)
    for reaction in reaction_list:
        count = reaction.count
        async for user in reaction.users():
            if user.bot and bot_subtract.lower() != 'dns':
                count -= 1
        embed.add_field(name=reaction.emoji,value=count)
    await ctx.message.channel.send(embed=embed)

@client.command()
async def emojitype(ctx,*,message):
    await ctx.message.delete()
    emojis = json.loads(urllib.request.urlopen(
        "https://raw.githubusercontent.com/BLANK-TH/elevator-bot-resources/bot-storage/emojis.json").read())
    message = "{}".format(message).lower()
    msg = []
    for x in message:
       try:
           msg.append(emojis[x])
           msg.append(" ")
       except KeyError:
           if x == " ":
               msg.append("    ")
               continue
           msg.append(x)
           msg.append(" ")
    embed = discord.Embed()
    if ctx.message.author.nick is not None:
        embed.set_author(name="{}#{} ({})".format(ctx.message.author.name, ctx.message.author.discriminator, ctx.message.author.nick),
                         icon_url=ctx.message.author.avatar_url)
    else:
        embed.set_author(name="{}#{}".format(ctx.message.author.name, ctx.message.author.discriminator),
                         icon_url=ctx.message.author.avatar_url)
    send_msg = "".join(x for x in msg)
    if len(send_msg) > 2000:
        await ctx.message.channel.send("The message is too long to send.")
        return
    await ctx.message.channel.send(send_msg,embed=embed)

@client.command()
async def verify(ctx):
    unverified_role = get(ctx.guild.roles, id=737092006349635706)
    if unverified_role not in ctx.message.author.roles:
        msg = await ctx.message.channel.send("You are already verified.")
        await asyncio.sleep(4)
        await msg.delete()
        await ctx.message.delete()
        return
    url = urllib.request.urlopen("https://raw.githubusercontent.com/bevacqua/correcthorse/master/wordlist.json")
    words = json.loads(url.read())
    captcha_list = []
    msg_list = []
    msg_list.append(ctx.message)
    async with ctx.message.channel.typing():
        for letter in choice(words).lower():
            captcha_list.append(letter)
        for num in str(randint(10000,100000)):
            captcha_list.append(num)
        captcha_text = ''.join(sample([x for x in captcha_list if x not in ["0","o","l","1","7"]], 5))
        img_gen = ImageCaptcha()
        captcha_img = img_gen.generate(captcha_text)
    msg_list.append(await ctx.channel.send("Please solve the attached captcha. If you wish to get a new captcha, enter `cancel` then run"
                           " the command again. You have 30 seconds to answer",file=discord.File(captcha_img,'captcha.png')))
    def check(msg):
        if msg.author == ctx.message.author:
            return True
        return False
    async def msg_del():
        await asyncio.sleep(4)
        for msg in msg_list:
            await msg.delete()
    try:
        response = await client.wait_for('message',check=check,timeout=30)
        msg_list.append(response)
    except asyncio.TimeoutError:
        msg_list.append(await ctx.channel.send("You took too long, the request has timed out. To try again use `s!verify`"))
        await msg_del()
        return
    if response.content.lower() == 'cancel':
        msg_list.append(await ctx.channel.send("You have canceled the verification, to try again use `s!verify`"))
        await msg_del()
        return
    if not response.content.lower().replace(" ","") == captcha_text.lower():
        msg_list.append(await ctx.channel.send("You didn't answer the captcha correctly, to try again use `s!verify`, "
                                               f"The correct answer is `{captcha_text.lower()}`"))
        await msg_del()
        return
    msg_list.append(await ctx.channel.send("You answered the captcha correctly. You should be able to see the channels shortly."))
    member_role = get(ctx.guild.roles,id=686702502472974338)
    await ctx.message.author.add_roles(member_role)
    await ctx.message.author.remove_roles(unverified_role)
    await msg_del()

@client.command()
@commands.has_role("Staff")
async def shadow(ctx,user: discord.Member,*,reason="N/A"):
    log_channel = client.get_channel(725438062296826027)
    role = get(ctx.guild.roles,id=737870509034831884)
    await ctx.message.delete()
    embed = discord.Embed(
        title="You were shadowed on the Elevator Discord Server",
        description="Shadow means that you cannot see or message on any channels except for a interview channel" +
        " where you will talk with Staff about what you did and possible further punishments. There may or may not" +
        " be a reason included with this notice, if there isn't you will be told in the interview channel soon.",
        colour=discord.Colour.dark_gold()
    )
    embed.add_field(name="Shadowed By:",value=ctx.message.author)
    embed.add_field(name="Reason:",value=reason)
    embed.set_image(url='https://i.imgur.com/Vc2VRnp.png')
    embed.set_footer(text=df)
    try:
        await user.send(embed=embed)
    except Exception as e:
        await ctx.message.channel.send("The user could not be DMed, they were still shadowed regardless.",
                                       embed=discord.Embed(description=repr(e)))
    log_embed = discord.Embed(
        title="Someone was shadowed!",
        colour=hc
    )
    log_embed.add_field(name="Person Shadowed:", value=user.display_name, )
    log_embed.add_field(name="Shadowed By:", value=ctx.message.author)
    log_embed.add_field(name="User ID:", value=user.id)
    log_embed.add_field(name="Reason:", value=reason, inline=False)
    log_embed.set_footer(text=df)
    await log_channel.send(embed=log_embed)
    confirm_embed = discord.Embed(
        title="Shadow Succeeded",
        colour=discord.Colour.green()
    )
    confirm_embed.add_field(name="Person Shadowed:", value=user.display_name)
    confirm_embed.add_field(name="Shadowed By:", value=ctx.message.author)
    confirm_embed.add_field(name="Reason:", value=reason, inline=False)
    confirm_embed.set_footer(text=df)
    confirm = await ctx.message.channel.send(embed=confirm_embed)
    await user.add_roles(role)
    await confirm.delete(delay=7)

@client.command()
@commands.has_role("Staff")
async def unshadow(ctx,user: discord.Member):
    log_channel = client.get_channel(725438062296826027)
    role = get(ctx.guild.roles,id=737870509034831884)
    await ctx.message.delete()
    embed = discord.Embed(
        title="You were unshadowed on the Elevator Discord Server",
        colour=discord.Colour.green()
    )
    embed.add_field(name="Unshadowed By:",value=ctx.message.author.display_name)
    embed.set_footer(text=df)
    try:
        await user.send(embed=embed)
    except Exception as e:
        await ctx.message.channel.send("The user could not be DMed, they were still unshadowed regardless.",
                                       embed=discord.Embed(description=repr(e)))
    log_embed = discord.Embed(
        title="Someone was unshadowed!",
        colour=hc
    )
    log_embed.add_field(name="Person Unshadowed:", value=user.display_name, )
    log_embed.add_field(name="Unshadowed By:", value=ctx.message.author)
    log_embed.add_field(name="User ID:", value=user.id)
    log_embed.set_footer(text=df)
    await log_channel.send(embed=log_embed)
    confirm_embed = discord.Embed(
        title="Unshadow Succeeded",
        colour=discord.Colour.green()
    )
    confirm_embed.add_field(name="Person Unshadowed:", value=user.display_name)
    confirm_embed.add_field(name="Unshadowed By:", value=ctx.message.author)
    confirm_embed.set_footer(text=df)
    confirm = await ctx.message.channel.send(embed=confirm_embed)
    await user.remove_roles(role)
    await confirm.delete(delay=7)

@client.command()
async def rule(ctx,rule_num="0"):
    url = urllib.request.urlopen("https://raw.githubusercontent.com/BLANK-TH/elevator-bot-resources/bot-storage/rules.json")
    rules = json.loads(url.read())
    if rule_num == "0":
        embed = discord.Embed(description="\n".join(x for x in rules.values()),colour=hc)
    else:
        try:
            embed = discord.Embed(description=rules[rule_num],colour=hc)
        except KeyError:
            embed = discord.Embed(description="Please enter a valid rule number",colour=discord.Colour.red())
    embed.set_footer(text=df)
    await ctx.message.channel.send(embed=embed)

@client.command()
async def punishments(ctx,type="strikes"):
    url = urllib.request.urlopen("https://raw.githubusercontent.com/BLANK-TH/elevator-bot-resources/bot-storage/punishments.json")
    punishment = json.loads(url.read())
    type = type.lower()
    if type not in punishment.keys():
        descrip = "That is an invalid option. Please choose one of the following:\n" + ", ".join("`{}`".format(x) for x in punishment.keys())
    else:
        descrip = punishment[type]
    embed = discord.Embed(description=descrip,colour=hc)
    embed.set_footer(text=df)
    await ctx.message.channel.send(embed=embed)

@client.command()
@commands.has_role("Staff")
async def mute(ctx,user: discord.Member,*,reason="N/A"):
    log_channel = client.get_channel(725438062296826027)
    role = get(ctx.guild.roles,id=738080614191857755)
    await ctx.message.delete()
    embed = discord.Embed(
        title="You were muted on the Elevator Discord Server",
        description="Mute means that you cannot message on any channels." +
        " There may or may not" +
        " be a reason included with this notice. You will be muted until manually unmuted by a staff member",
        colour=discord.Colour.dark_gold()
    )
    embed.add_field(name="Muted By:",value=ctx.message.author)
    embed.add_field(name="Reason:",value=reason)
    embed.set_image(url='https://i.imgur.com/q1zwHO8.png')
    embed.set_footer(text=df)
    try:
        await user.send(embed=embed)
    except Exception as e:
        await ctx.message.channel.send("The user could not be DMed, they were still muted regardless.",
                                       embed=discord.Embed(description=repr(e)))
    log_embed = discord.Embed(
        title="Someone was muted!",
        colour=hc
    )
    log_embed.add_field(name="Person Muted:", value=user.display_name, )
    log_embed.add_field(name="Muted By:", value=ctx.message.author)
    log_embed.add_field(name="User ID:", value=user.id)
    log_embed.add_field(name="Reason:", value=reason, inline=False)
    log_embed.set_footer(text=df)
    await log_channel.send(embed=log_embed)
    confirm_embed = discord.Embed(
        title="Mute Succeeded",
        colour=discord.Colour.green()
    )
    confirm_embed.add_field(name="Person Muted:", value=user.display_name)
    confirm_embed.add_field(name="Muted By:", value=ctx.message.author)
    confirm_embed.add_field(name="Reason:", value=reason, inline=False)
    confirm_embed.set_footer(text=df)
    confirm = await ctx.message.channel.send(embed=confirm_embed)
    await user.add_roles(role)
    await confirm.delete(delay=7)

@client.command()
@commands.has_role("Staff")
async def unmute(ctx,user: discord.Member):
    log_channel = client.get_channel(725438062296826027)
    role = get(ctx.guild.roles,id=738080614191857755)
    await ctx.message.delete()
    embed = discord.Embed(
        title="You were unmuted on the Elevator Discord Server",
        colour=discord.Colour.green()
    )
    embed.add_field(name="Unmuted By:",value=ctx.message.author.display_name)
    embed.set_footer(text=df)
    try:
        await user.send(embed=embed)
    except Exception as e:
        await ctx.message.channel.send("The user could not be DMed, they were still unmuted regardless.",
                                       embed=discord.Embed(description=repr(e)))
    log_embed = discord.Embed(
        title="Someone was unmuted!",
        colour=hc
    )
    log_embed.add_field(name="Person Unmuted:", value=user.display_name, )
    log_embed.add_field(name="Unmuted By:", value=ctx.message.author)
    log_embed.add_field(name="User ID:", value=user.id)
    log_embed.set_footer(text=df)
    await log_channel.send(embed=log_embed)
    confirm_embed = discord.Embed(
        title="Unmute Succeeded",
        colour=discord.Colour.green()
    )
    confirm_embed.add_field(name="Person Unmuted:", value=user.display_name)
    confirm_embed.add_field(name="Unmuted By:", value=ctx.message.author)
    confirm_embed.set_footer(text=df)
    confirm = await ctx.message.channel.send(embed=confirm_embed)
    await user.remove_roles(role)
    await confirm.delete(delay=7)
@client.command()
async def code(ctx):
    code_embed = discord.Embed(
       title='Code',
        description="Code for This Bot: [CLICK HERE]({})".format(
            "https://github.com/BLANK-TH/elevator-bot"
        ),
        colour=hc
    )
    code_embed.set_footer(text=df)
    await ctx.message.channel.send(embed=code_embed)

@client.command(aliases=["color"])
async def colour(ctx,*,colour_name:str):
    colour_name = colour_name.lower()
    active_role = get(ctx.guild.roles, id=740030930021908570)
    url = urllib.request.urlopen(
        "https://raw.githubusercontent.com/BLANK-TH/elevator-bot-resources/bot-storage/colourids.json")
    all_colours = json.loads(url.read())
    colours = all_colours["colours"]
    active_colours = all_colours["active colours"]
    if colour_name == "none":
        prev_colour = None
        for name, role_id in colours.items():
            role = get(ctx.guild.roles, id=role_id)
            if role in ctx.message.author.roles:
                await ctx.message.author.remove_roles(role)
                prev_colour = name
        for name, role_id in active_colours.items():
            role = get(ctx.guild.roles, id=role_id)
            if role in ctx.message.author.roles:
                await ctx.message.author.remove_roles(role)
                prev_colour = name
        await ctx.message.channel.send("The colour role `{}` has been removed successfully".format(prev_colour.title()))
    elif colour_name not in colours.keys() and colour_name not in active_colours.keys():
        await ctx.message.channel.send("You are trying to get a colour that doesn't exist. "
                                       "Here are the viable colour names: \n```Colours:\n{}``` \n\n```Active Colours:\n{}```".format(
            "\n".join(x.title() for x,y in colours.items()),"\n".join(x.title() for x,y in active_colours.items())
        ))
        return
    else:
        prev_colour = None
        for name,role_id in colours.items():
            role = get(ctx.guild.roles,id=role_id)
            if role in ctx.message.author.roles:
                await ctx.message.author.remove_roles(role)
                prev_colour = name
        for name,role_id in active_colours.items():
            role = get(ctx.guild.roles, id=role_id)
            if role in ctx.message.author.roles:
                await ctx.message.author.remove_roles(role)
                prev_colour = name
        if colour_name in active_colours.keys():
            if active_role not in ctx.message.author.roles:
                await ctx.message.channel.send(
                    "You are trying to get a Active Role only colour when you don't have the Active Member role.")
                return
            role = get(ctx.guild.roles,id=active_colours[colour_name])
        else:
            role = get(ctx.guild.roles, id=colours[colour_name])
        await ctx.message.author.add_roles(role)
        if prev_colour is None:
            await ctx.message.channel.send(
                "The colour role `{}` has been added successfully.".format(colour_name.title()))
        else:
            await ctx.message.channel.send(
                "The colour role `{}` has been added successfully. `{}` has been removed successfully.".format(
                    colour_name.title(),prev_colour.title()))

@client.command()
@commands.has_role("Staff")
async def promoteactive(ctx,user:discord.Member):
    embed = discord.Embed(
        description="You have been promoted to Active Member by **{}**! You now have access to the active-chat, "
                    "active member colours, a higher spot in the member list on the right, "
                    "and other special perks that will be coming soon in the future. If there "
                    "is a colour you think should be added to the active colour list, message BLANK in suggestions".format(
            ctx.message.author.display_name
        ),
        colour=hc
    )
    embed.set_footer(text=df)
    active_role = get(ctx.guild.roles, id=740030930021908570)
    if active_role in user.roles:
        await ctx.message.channel.send("The user already has the Active Member role. Ain't no such thing as double active member!")
        return
    try:
        await user.send(embed=embed)
    except Exception as e:
        await ctx.message.channel.send("The user could not be DMed, they were promoted to active member regardless.",
                                       embed=discord.Embed(description=repr(e)))
    await user.add_roles(active_role)
    await ctx.message.channel.send(embed=discord.Embed(
        description="{} has been successfully promoted to active member!".format(user.mention)))

@client.command(aliases=['devadd','devtodo'])
async def developeraddtodo(ctx,type,priority,bot,difficulty,*,title_description):
    dev_role = get(ctx.guild.roles,id=733854432978141227)
    if not dev_role in ctx.message.author.roles:
        await ctx.message.channel.send("You do not have permissions to do this, this is for the bot developers only. You "
                                       "can try the `suggestcommand` or `bugreport` command.")
        return
    if "|" in title_description:
        title = title_description.split("|")[0].strip()
        description = title_description.split("|")[1].strip()
    else:
        title = title_description.strip()
        description = None
    async with ctx.message.channel.typing():
        prioritys = all_labels["priority"]
        types = all_labels["type"]
        bots = all_labels["bot"]
        bots["none"] = None
        difficultys = all_labels["difficulty"]
        difficultys["none"] = None
        if priority.lower() not in prioritys.keys() and type.lower() not in types.keys() and \
            bot.lower() not in bots.keys() and difficulty.lower() not in difficultys.keys():
                await ctx.message.channel.send("Invalid Type/Priority/Bot/Difficulty")
                return
        lab = [{"id":prioritys[priority.lower()]},{"id":types[type.lower()]}]
        if difficultys[difficulty] is not None:
            lab.append({"id":difficultys[difficulty.lower()]})
        if bots[bot] is not None:
            lab.append({"id":bots[bot.lower()]})
        if description is not None:
            card = globoard.create_card(board_id,queue_column_id,title,description={"text":description},labels=lab)
        else:
            card = globoard.create_card(board_id, queue_column_id, title, labels=lab)
        globoard.create_comment(board_id, card.id,
                                "Long Link: https://app.gitkraken.com/glo/board/{}/card/{}\nID: {}".format(board_id,
                                                                                                         card.id,
                                                                                                         card.id))
    if type == "featureupdate":
        type = "feature update"
    if difficulty == "workintensive":
        difficulty = "work intensive"
    confirm_embed = discord.Embed(title="Developer Queue Addition Succeeded!",
                                  description='To view the card, visit this link:\n'
                                              + "https://app.gitkraken.com/glo/board/{}/card/{}".format(board_id,card.id),
                                  colour=discord.Colour.green())
    confirm_embed.add_field(name='Title:', value=title)
    confirm_embed.add_field(name='Description:', value=str(description))
    confirm_embed.add_field(name='Type:', value=type.title())
    confirm_embed.add_field(name='Priority:', value=priority.title())
    confirm_embed.add_field(name="Bot", value=bot.title())
    confirm_embed.add_field(name="Difficulty", value=difficulty.title())
    confirm_embed.add_field(name='Requester', value=ctx.message.author)
    confirm_embed.set_footer(text=df)
    await ctx.message.channel.send(embed=confirm_embed)

@client.command(aliases=['br'])
async def bugreport(ctx,*,title_description):
    if "|" in title_description:
        bug_title = title_description.split("|")[0].strip()
        bug_description = title_description.split("|")[1].strip()
    else:
        bug_title = title_description.strip()
        bug_description = "None"
    async with ctx.message.channel.typing():
        types = all_labels["type"]
        info = f"Bug Description: {str(bug_description)} | Reporter Name + Discriminator: {ctx.message.author.name}#" \
           f"{ctx.message.author.discriminator} | Reporter Nickname: {ctx.message.author.nick} | Reporter ID: " \
           f'{str(ctx.message.author.id)} | Reported At: {ctx.message.created_at.strftime("%Y-%m-%d %H:%M UTC")} | ' \
           f'Message Link: {ctx.message.jump_url} | Message ID: {str(ctx.message.id)} | Channel Name: ' \
           f'{ctx.message.channel.name} | Channel ID: {str(ctx.message.channel.id)}'
        card = globoard.create_card(board_id,approval_column_id,bug_title,description={"text":info},labels=[{"id":types["bug"]}])
        globoard.create_comment(board_id, card.id,
                                "Long Link: https://app.gitkraken.com/glo/board/{}/card/{}\nID: {}".format(board_id,
                                                                                                         card.id,
                                                                                                         card.id))
    confirm_embed = discord.Embed(title="Bug Report Succeeded!",
                                  description='To track the progress/state of your bug report, visit this link:\n'
                                              + "https://app.gitkraken.com/glo/board/{}/card/{}".format(board_id,card.id),
                                  colour=discord.Colour.green())
    confirm_embed.add_field(name='Bug Title:', value=bug_title)
    confirm_embed.add_field(name='Bug Description:', value=str(bug_description))
    confirm_embed.add_field(name='Requester', value=ctx.message.author)
    confirm_embed.set_footer(text=df)
    await ctx.message.channel.send(embed=confirm_embed)

@client.command(aliases=['sco'])
async def suggestcommand(ctx,*,title_description):
    if "|" in title_description:
        command_title = title_description.split("|")[0].strip()
        command_description = title_description.split("|")[1].strip()
    else:
        command_title = title_description.strip()
        command_description = "None"
    async with ctx.message.channel.typing():
        types = all_labels["type"]
        info = f"Command Description: {str(command_description)} | Requester Name + Discriminator: {ctx.message.author.name}#" \
           f"{ctx.message.author.discriminator} | Requester Nickname: {ctx.message.author.nick} | Requester ID: " \
           f'{str(ctx.message.author.id)} | Requested At: {ctx.message.created_at.strftime("%Y-%m-%d %H:%M UTC")} | ' \
           f'Message Link: {ctx.message.jump_url} | Message ID: {str(ctx.message.id)} | Channel Name: ' \
           f'{ctx.message.channel.name} | Channel ID: {str(ctx.message.channel.id)}'
        card = globoard.create_card(board_id, approval_column_id, command_title, description={"text":info},
                                    labels=[{"id": types["request"]}])
        globoard.create_comment(board_id, card.id,
                                "Long Link: https://app.gitkraken.com/glo/board/{}/card/{}\nID: {}".format(board_id,
                                                                                                         card.id,
                                                                                                         card.id))
    confirm_embed = discord.Embed(title="Command Suggestion Succeeded!",
                                  description='To track the progress/state of your suggestion, visit this link:\n'
                                              + "https://app.gitkraken.com/glo/board/{}/card/{}".format(board_id,card.id),
                                  colour=discord.Colour.green())
    confirm_embed.add_field(name='Command Title:', value=command_title)
    confirm_embed.add_field(name='Command Description:', value=str(command_description))
    confirm_embed.add_field(name='Requester', value=ctx.message.author)
    confirm_embed.set_footer(text=df)
    await ctx.message.channel.send(embed=confirm_embed)

@client.command(aliases=['fu'])
async def featureupdate(ctx,*,title_description_original):
    counter = 0
    for x in title_description_original:
        if "|" in x:
            counter += 1
    if counter >= 2:
        original_command = title_description_original.split("|")[0].strip()
        feature_title = title_description_original.split("|")[1].strip()
        feature_description = title_description_original.split("|")[2].strip()
    elif counter == 1:
        original_command = title_description_original.split("|")[0].strip()
        feature_title = title_description_original.split("|")[1].strip()
        feature_description = "None"
    else:
        await ctx.message.channel.send("You need to provide at least the command name and the feature you want to add."
                                       " In this format `s!featureupdate <command name> | <update title> [| update description]`"
                                       ". The update description is optional.")
        return
    async with ctx.message.channel.typing():
        types = all_labels["type"]
        info = f"Original Command: {original_command} | Feature Update Description: {str(feature_description)}" \
               f" | Reporter Name + Discriminator: {ctx.message.author.name}#" \
           f"{ctx.message.author.discriminator} | Reporter Nickname: {ctx.message.author.nick} | Reporter ID: " \
           f'{str(ctx.message.author.id)} | Reported At: {ctx.message.created_at.strftime("%Y-%m-%d %H:%M UTC")} | ' \
           f'Message Link: {ctx.message.jump_url} | Message ID: {str(ctx.message.id)} | Channel Name: ' \
           f'{ctx.message.channel.name} | Channel ID: {str(ctx.message.channel.id)}'
        card = globoard.create_card(board_id, approval_column_id, feature_title, description={"text":info},
                                    labels=[{"id": types["featureupdate"]}])
        globoard.create_comment(board_id, card.id,
                                "Long Link: https://app.gitkraken.com/glo/board/{}/card/{}\nID: {}".format(board_id,
                                                                                                         card.id,
                                                                                                         card.id))
    confirm_embed = discord.Embed(title="Feature Update Suggestion Succeeded!",
                                  description='To track the progress/state of your bug report, visit this link:\n'
                                              +card.short_url,
                                  colour=discord.Colour.green())
    confirm_embed.add_field(name="Original Command:",value=original_command)
    confirm_embed.add_field(name='Feature Update Title:', value=feature_title)
    confirm_embed.add_field(name='Feature Update Description:', value=str(feature_description))
    confirm_embed.add_field(name='Requester', value=ctx.message.author)
    confirm_embed.set_footer(text=df)
    await ctx.message.channel.send(embed=confirm_embed)

@client.command()
async def compilestory(ctx,limit:int=100):
    async with ctx.message.channel.typing():
        story_channel = client.get_channel(740675095005102153)
        words = []
        async for word in story_channel.history(limit=limit):
            if "//" != word.content[:2]:
                if "." in word.content:
                    words.append("\n")
                words.append(word.content)
        words.reverse()
        story = " ".join(words)
        story_url = repo.create_file("CompiledStoryForCompileStoryCmdMSG{}.txt".format(
        str(ctx.message.id)),
        "Requester ID: {} | Requester Name + Discriminator {}#{} | Message ID: {} | Message Link: {} | At: {}".format(
            str(ctx.message.author.id), ctx.message.author.name,
            ctx.message.author.discriminator, str(ctx.message.id), ctx.message.jump_url,
            ctx.message.created_at.strftime("%b %d %Y %H:%M UTC")),
        story,branch="commands")['content'].html_url
        embed = discord.Embed(title="Compiled One Word Story",description="[CLICK HERE]({})".format(story_url),colour=hc)
        embed.set_footer(text=df)
        embed.add_field(name="Limit",value=str(limit))
        await ctx.message.channel.send(embed=embed)

@client.command(aliases=['animemojiuser','aeu'])
async def animatedemojiuser(ctx,*,emoji_name):
    def similar(a,b):
        return SequenceMatcher(None,a,b).ratio()
    emoji_similaritys = {}
    for emoji in ctx.guild.emojis:
        if emoji.animated:
            emoji_similaritys[similar(emoji_name,emoji.name)] = emoji
    highest_emoji = max([*emoji_similaritys]),emoji_similaritys[max([*emoji_similaritys])]
    if highest_emoji[0] < 0.1:
        await ctx.message.channel.send("Could not find any emojis that match `{}`".format(emoji_name))
        return
    webhook = None
    for hook in await ctx.message.channel.webhooks():
        if hook.user.id == 699677108607123548:
            webhook = hook
            break
    if webhook is None:
        webhook = await ctx.message.channel.create_webhook(name="Elevator Bot Webhook")
    await ctx.message.delete()
    await webhook.send(content="<a:{}:{}>".format(highest_emoji[1].name,str(highest_emoji[1].id)),
                       username=ctx.message.author.display_name, avatar_url=ctx.message.author.avatar_url)
@client.command(aliases=["nc"])
async def noonecares(ctx):
    await ctx.message.channel.send("https://www.youtube.com/watch?v=BLUkgRAy_Vo")

@client.command(aliases=["hs"])
async def headsmash(ctx):
    text = ""
    for x in range(0,randint(5,20)):
        text += choice(ascii_lowercase)
    await ctx.message.channel.send(text)

@client.command(aliases=["hsu"])
async def headsmashuser(ctx):
    text = ""
    for x in range(0,randint(5,20)):
        text += choice(ascii_lowercase)
    webhook = None
    for hook in await ctx.message.channel.webhooks():
        if hook.user.id == 699677108607123548:
            webhook = hook
            break
    if webhook is None:
        webhook = await ctx.message.channel.create_webhook(name="Elevator Bot Webhook")
    await ctx.message.delete()
    await webhook.send(content=text,username=ctx.message.author.display_name, avatar_url=ctx.message.author.avatar_url)

@client.command()
async def welcome(ctx,user:discord.Member=None):
    sr_channel = client.get_channel(692521137166614570)
    c_channel = client.get_channel(686703151738519561)
    r_channel = client.get_channel(686700028399452181)
    b_channel = client.get_channel(690221900621676586)
    if user is not None:
        mem = user.mention
    else:
        mem = "there"
    w_embed = discord.Embed(
        description=f'Hey {mem}! Welcome to **elevator (F127)**! Make sure to read the {r_channel.mention} then head over to'
                    f' {sr_channel.mention}, {c_channel.mention}, and {b_channel.mention}! We hope you enjoy your time '
                    f'here :D',
        colour=hc
    )
    w_embed.set_footer(text=df)
    await ctx.message.channel.send(embed=w_embed)

@client.command()
async def bearspray(ctx,user:discord.Member=None):
    if user is None:
        msg = "{} didn't know who to spray so they just sprayed themself. They're now writhing in pain while coughing.".format(ctx.message.author.mention)
    else:
        if "bear" in user.display_name.lower():
            msg = "{} sprays their can of bear spray straight at {}, it works and the bear retreats and ends up ||dying|| " \
                  "a few hours later.".format(ctx.message.author.mention,user.mention)
        else:
            msg = "{} sprays their can of bear spray at {}, it didn't work because they aren't a bear. {} ||shoots|| {}" \
                  " with a ||gun|| and they ||die||.".format(ctx.message.author.mention,user.mention,user.mention,ctx.message.author.mention)
    embed = discord.Embed(description=msg,colour=hc)
    embed.set_footer(text=df)
    embed.set_image(url="https://i.imgur.com/YVuheFh.jpg")
    await ctx.message.channel.send(embed=embed)

@client.command()
async def revive(ctx,user:discord.Member):
    embed = discord.Embed(description="{} has revived {}!".format(ctx.message.author.mention,user.mention),colour=hc)
    embed.set_footer(text=df)
    embed.set_image(url="https://media.giphy.com/media/3o7TKSM3u36i6yG4CI/giphy.gif")
    await ctx.message.channel.send(embed=embed)

@client.command()
async def smallbrain(ctx,user:discord.Member=None):
    if user is None:
        user = ctx.message.author
    if user.id == 405498995520176140:
        brain_size = 0
    elif user.id == 616032766974361640:
        brain_size = 100
    elif user.id == 597391214765015081:
        brain_size = 100
    else:
        brain_size = randint(0,100)
    embed = discord.Embed(description="**{}'s Brain Size:**\n{}%".format(user.mention,str(brain_size)),
                          colour=hc)
    embed.set_footer(text=df)
    await ctx.message.channel.send(embed=embed)

@client.command()
async def pingmusic(ctx):
    await ctx.message.channel.send("https://www.youtube.com/watch?v=RKW6rjnYEkc")

@client.command(aliases=["ci"])
async def commandidea(ctx):
    embed = discord.Embed(colour=hc)
    embed.set_footer(text=df)
    embed.set_image(url="https://i.imgur.com/MN0kd7x.jpg")
    await ctx.message.channel.send(embed=embed)

@client.command(aliases=["gn"])
async def goodnight(ctx,user:discord.Member=None):
    if user is None:
        say_user = "Someone"
        user = ctx.message.author
    else:
        say_user = ctx.message.author.mention
    embed = discord.Embed(description="{} wishes goodnight to {}!".format(say_user,user.mention),colour=hc)
    embed.set_footer(text=df)
    embed.set_image(url="https://i.imgur.com/3RxNRwV.gif")
    await ctx.message.channel.send(embed=embed)

@client.command()
async def roleinfo(ctx,role:discord.Role):
    embed = discord.Embed(description=role.mention,colour=hc)
    embed.set_footer(text=df)
    embed.add_field(name="Role Name",value=role.name)
    embed.add_field(name="Role ID:",value=str(role.id))
    embed.add_field(name="Hoisted:",value=str(role.hoist))
    embed.add_field(name="Managed:",value=str(role.managed))
    embed.add_field(name="Mentionable:",value=str(role.mentionable))
    embed.add_field(name="Colour/Color:",value=f"RGB: {role.colour.to_rgb()}\nHEX: {str(role.colour)}")
    embed.add_field(name="Created At:",value=role.created_at.strftime("%Y-%m-%d %H:%M UTC"))
    if len(", ".join(x.mention for x in role.members)) >= 1024:
        member_url = repo.create_file("RoleMemberListMSG{}.txt".format(
            str(ctx.message.id)),
            "Author ID: {} | Author Name + Discriminator {}#{} | Message ID: {} | Message Link: {} | At: {}".format(
                str(ctx.message.id), ctx.message.author.name,
                ctx.message.author.discriminator, str(ctx.message.id), ctx.message.jump_url,
                ctx.message.created_at.strftime("%b %d %y %H:%M UTC")),
            "\n".join(x.display_name for x in role.members), branch="commands")['content'].html_url
        embed.add_field(name="Members With Role:", value=f"[CLICK HERE]({member_url})", inline=False)
    elif len(role.members) == 0:
        embed.add_field(name="Members With Role:", value="None", inline=False)
    else:
        embed.add_field(name="Members With Role:", value=", ".join(x.mention for x in role.members), inline=False)
    await ctx.message.channel.send(embed=embed)

@client.command()
async def torture(ctx,user:discord.Member=None):
    if user is None:
        user = ctx.message.author
        action_user = "Someone"
    else:
        action_user = ctx.message.author.mention
    embed = discord.Embed(description="{} is torturing {}...".format(action_user,user.mention),colour=discord.Colour.red())
    embed.add_field(name="Disclaimer",value="No intense/extremely graphic images were used in this command to avoid "
                                            "triggering panic attacks and other similar events. If this comes anywhere "
                                            "close to triggering any panic attack, please contact <@616032766974361640>.")
    embed.set_footer(text=df)
    embed.set_image(url="https://i.imgur.com/Hsbd7jo.gif")
    await ctx.message.channel.send(embed=embed)

@client.command()
async def lyrics(ctx,*,song_name):
    async with ctx.message.channel.typing():
        try:
            data = lyrics_extractor.get_lyrics(song_name)
        except LyricScraperException as e:
            await ctx.message.channel.send("An error has occurred, the most likely reason is that you entered a non-existent"
                                        " song name. If you are sure that the name is correct, please contact BLANK to have"
                                        " him take a look at the (attached) error.",embed=discord.Embed(description=repr(e)))
        else:
            if len(data["lyrics"]) >= 2048:
                wrapper = TextWrapper(width=2040,break_long_words=False,replace_whitespace=False)
                wrapped_lyric = wrapper.wrap(data["lyrics"])[0] + "\n**...**"
                embed = discord.Embed(title=data["title"],description=wrapped_lyric,colour=hc)
            else:
                embed = discord.Embed(title=data["title"],description=data["lyrics"].replace("\n","\n\n"),colour=hc)
            await ctx.message.channel.send(embed=embed)

@client.command(aliases=["ss"])
async def soulsuck(ctx,user:discord.Member):
    if ctx.message.author.id not in [616032766974361640,597391214765015081]:
        await ctx.message.channel.send(embed=discord.Embed(description="Sorry hun, this command only works for demons "
                                                                       "and demon cult members (<@597391214765015081> "
                                                                       "and <@616032766974361640>), try again when you"
                                                                       " have a place in hell (and don't have a soul)!",
                                                           colour=hc))
        return
    embed = discord.Embed(description="I'm glad to inform you {}, you no longer have a soul! {} has sucked it. You no "
                                      "longer have to feel the pain of life. Enjoy eternity!"
                          .format(user.mention,ctx.message.author.mention),colour=0x8B0000)
    embed.set_footer(text=df)
    images = ["https://i.imgur.com/wecJcMc.gif","https://i.imgur.com/kkfc7Nv.gif"]
    embed.set_image(url=choice(images))
    await ctx.message.channel.send(embed=embed)

@client.command()
async def donkey(ctx):
    await ctx.message.delete()
    role = get(ctx.guild.roles,id=743829242412007496)
    if role in ctx.message.author.roles and ctx.message.author.id != 616032766974361640:
        msg = await ctx.message.channel.send("{} you are not allowed to use the donkey emote!".format(ctx.message.author.mention))
        await msg.delete(delay=10)
        return
    webhook = None
    for hook in await ctx.message.channel.webhooks():
        if hook.user.id == 699677108607123548:
            webhook = hook
            break
    if webhook is None:
        webhook = await ctx.message.channel.create_webhook(name="Elevator Bot Webhook")
    await webhook.send(content="<:donkey:743826956256149585>", username=ctx.message.author.display_name,
                       avatar_url=ctx.message.author.avatar_url)

@client.command()
async def toggledonkey(ctx):
    role = get(ctx.guild.roles, id=743829242412007496)
    user = ctx.guild.get_member(405498995520176140)
    if ctx.message.author.id == user.id:
        await ctx.message.channel.send("You are not allowed to use this command!")
        return
    if role not in user.roles:
        await user.add_roles(role)
        msg = "{} is no longer allowed to use the donkey emote!".format(user.mention)
    else:
        await user.remove_roles(role)
        msg = "{} is now allowed to use the donkey emote!".format(user.mention)
    embed = discord.Embed(description=msg,colour=hc)
    embed.set_footer(text=df)
    await ctx.message.channel.send(embed=embed)

@client.command(aliases=["ttt"])
async def tictactoe(ctx,player2:discord.Member=None):
    if player2 is None:
        def check(message):
            return message.channel.id == ctx.message.channel.id and message.content.lower() == "accept" and \
                   message.author.id != ctx.message.author.id
        await ctx.message.channel.send("Would anyone like to play tic tac toe with {}? Type `accept` to join the game."
                                       .format(ctx.author.mention))
        try:
            msg = await client.wait_for("message",check=check,timeout=60)
        except asyncio.TimeoutError:
            await ctx.message.channel.send("No-one has joined, the game has been canceled.")
            return
        await ctx.message.channel.send("{}, {} has accepted the game will start soon.".format(
            ctx.author.mention,msg.author.mention))
        player2 = msg.author
    else:
        def check(message):
            return message.channel.id == ctx.message.channel.id and message.content.lower() == "accept" and \
                   message.author.id != ctx.message.author.id

        await ctx.message.channel.send("{} would you like to play tic tac toe with {}? Type `accept` to join the game."
                                       .format(player2.mention,ctx.author.mention))
        try:
            msg = await client.wait_for("message", check=check, timeout=60)
        except asyncio.TimeoutError:
            await ctx.message.channel.send("No-one has joined, the game has been canceled.")
            return
        await ctx.message.channel.send("{}, {} has accepted the game will start soon.".format(
            ctx.author.mention, msg.author.mention))
    def embed_gen(descrip,colour):
        em = discord.Embed(description=descrip,colour=colour)
        em.set_footer(text=df)
        em.set_author(name="{} and {}'s Tic Tac Toe Game".format(p1[0].display_name, p2[0].display_name))
        em.add_field(name="Instructions", value="The tic tac toe grid is in the description of the embed. All squares with"
                                                " numbers are not taken. Click the corresponding number emoji reaction to"
                                                " play that square. Once you click the emoji the number will be replaced"
                                                " with your marked then the reaction will be removed."
                                                " The first player is chosen at random and is noted in"
                                                " the Current Player field. The requesting player is `X` and the requested"
                                                " player is `O`. The rest is general tic tac toe rules."
                     ,inline=False)
        em.add_field(name="Current Player", value=cur_player.display_name)
        em.add_field(name="Turn Number",value=str(turn_num))
        return em
    def descrip_gen():
        counter = 1
        descrip = ""
        for square in grid:
            descrip += square
            if counter == 3:
                counter = 0
                descrip += "\n"
            counter += 1
        return descrip.rstrip()
    def replace_val(emote, grid):
        old_grid = grid
        grid = []
        for square in old_grid:
            if square != emote:
                grid.append(square)
            else:
                if cur_player.id == ctx.author.id:
                    grid.append(emojis["x"])
                else:
                    grid.append(emojis["o"])
        return grid
    def get_other_player():
        if cur_player == p1[0]:
            return p2[0]
        else:
            return p1[0]
    def check_win(emote):
        sets = [[0,1,2],[3,4,5],[6,7,8],[0,4,8],[2,4,6],[0,3,6],[1,4,7],[2,5,8]]
        for set in sets:
            set_status = True
            for index in set:
                if grid[index] != emote:
                    set_status = False
                    break
            if set_status:
                return True
        return False
    def check_tie():
        for square in grid:
            if square != emojis["x"] and square != emojis["o"]:
                return False
        return True
    p1 = [ctx.author]
    p2 = [player2]
    cur_player = choice([p1[0],p2[0]])
    turn_num = 1
    url = urllib.request.urlopen("https://raw.githubusercontent.com/BLANK-TH/elevator-bot-resources/bot-storage/"
                                 "emojis.json")
    emojis = json.loads(url.read())
    emojis["x"] = ":x:"
    emojis["o"] = ":o:"
    grid = [emojis["1"],emojis["2"],emojis["3"],emojis["4"],emojis["5"],emojis["6"],emojis["7"],emojis["8"],emojis["9"]]
    self_reacts = {}
    game_embed = embed_gen(descrip_gen(),discord.Colour.gold())
    game_message = await ctx.send(embed=game_embed)
    for emoji in grid:
        self_reacts[emoji] = await game_message.add_reaction(emoji)
    if cur_player.id == ctx.author.id:
        col = discord.Colour.blue()
    else:
        col = discord.Colour.orange()
    await game_message.edit(embed=embed_gen(descrip_gen(),col))
    winner = None
    while True:
        def chk(reaction, user):
            if user.bot:
                return False
            if reaction.message.id != game_message.id:
                return False
            if user.id != cur_player.id:
                return False
            if reaction.emoji not in grid:
                return False
            return True
        try:
            react = await client.wait_for("reaction_add",check=chk,timeout=60)
        except asyncio.TimeoutError:
            em = discord.Embed(title="{} Wins".format(cur_player.display_name), description=descrip_gen(),
                               colour=discord.Colour.blue())
            em.set_footer(text=df)
            em.set_author(name="{} and {}'s Tic Tac Toe Game".format(p1[0].display_name, p2[0].display_name))
            em.add_field(name="Turn Number", value=str(turn_num))
            await game_message.edit(embed=em)
            await ctx.send("{} has abandoned the match, {} has won".format(cur_player.mention,get_other_player().mention))
            return
        grid = replace_val(react[0].emoji,grid)
        async for user in react[0].users():
            await react[0].remove(user)
            await asyncio.sleep(0.2)
        if cur_player.id == ctx.author.id:
            col = discord.Colour.blue()
        else:
            col = discord.Colour.orange()
        if check_tie():
            break
        if cur_player.id == ctx.author.id:
            if check_win(emojis["x"]):
                winner = p1[0]
                break
        else:
            if check_win(emojis["o"]):
                winner = p2[0]
                break
        cur_player = get_other_player()
        turn_num += 1
        await game_message.edit(embed=embed_gen(descrip_gen(), col))
    if winner is None:
        em = discord.Embed(title="Tie",description=descrip_gen(), colour=discord.Colour.gold())
        em.set_footer(text=df)
        em.set_author(name="{} and {}'s Tic Tac Toe Game".format(p1[0].display_name, p2[0].display_name))
        em.add_field(name="Turn Number", value=str(turn_num))
    elif winner.id == p1[0].id:
        em = discord.Embed(title="{} Wins".format(p1[0].display_name), description=descrip_gen(), colour=discord.Colour.blue())
        em.set_footer(text=df)
        em.set_author(name="{} and {}'s Tic Tac Toe Game".format(p1[0].display_name, p2[0].display_name))
        em.add_field(name="Turn Number", value=str(turn_num))
    elif winner.id == p2[0].id:
        em = discord.Embed(title="{} Wins".format(p2[0].display_name), description=descrip_gen(), colour=discord.Colour.orange())
        em.set_footer(text=df)
        em.set_author(name="{} and {}'s Tic Tac Toe Game".format(p1[0].display_name, p2[0].display_name))
        em.add_field(name="Turn Number", value=str(turn_num))
    else:
        em = discord.Embed(title="Error",description="Game exited without definite winner.",colour=discord.Colour.red())
        em.set_footer(text=df)
    await game_message.edit(embed=em)

@client.command(aliases=["ct"])
async def claptext(ctx,*,message):
    embed = discord.Embed(description=message.replace(" "," 👏 "),colour=hc)
    embed.set_footer(text=df)
    await ctx.message.channel.send(embed=embed)

@client.command()
async def sarcasm(ctx,*,message):
    msg = ""
    for index,letter in enumerate(message):
        if not letter.isalpha():
            msg += letter
        else:
            if index % 2 == 0 and letter != "i":
                msg += letter.upper()
            else:
                msg += letter.lower()
    embed = discord.Embed(description=msg, colour=hc)
    embed.set_footer(text=df)
    await ctx.message.channel.send(embed=embed)

@client.command()
async def choose(ctx,*args):
    embed = discord.Embed(description="I choose `{}`!".format(choice(args)),colour=hc)
    embed.set_footer(text=df)
    await ctx.send(embed=embed)

@client.command()
async def bully(ctx,user:discord.Member=None):
    if user is None:
        user_id = None
        user = "themselves?"
    else:
        user_id = user.id
        user = user.mention + "!"
    if user_id != 616032766974361640:
        embed = discord.Embed(description="{} is bullying {}".format(ctx.author.mention,user),colour=hc)
    else:
        embed = discord.Embed(description=f"How dare you bully my owner. {ctx.author.mention} go f*ck yourself!",colour=hc)
    embed.set_footer(text=df)
    if user_id != 616032766974361640:
        embed.set_image(url="https://i.ibb.co/GFzTQf9/bully.gif")
    else:
        embed.set_image(url='https://i.imgur.com/t96AqDf.png')
    await ctx.send(embed=embed)

client.run(BOT_TOKEN)
