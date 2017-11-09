import os
import sys
import discord
import re, json
import html
import datetime

from discord.ext import commands
from bs4 import BeautifulSoup
from urlbreak import get_item, skill_info
import urllib.request

###-- Invitation Link --###
#https://discordapp.com/api/oauth2/authorize?client_id=336363921466195968&scope=bot&permissions=0

bot = commands.Bot(command_prefix='!rawr ', description='this is rawr test!', pm_help = True)

bot.remove_command("help")


###-- prep --###
@bot.event
async def on_ready():
    await bot.change_presence(game=discord.Game(name="Trial Run"), status=discord.Status("dnd"))
    print('-----------------------')
    print('> Are you ready Rawr?!')
    print('> ' + bot.user.name)
    print('-----------------------')
    print('     Let\'s Rawr!!')
    print('-----------------------')
#####


###-- on server join --###
@bot.event
async def on_server_join(server):
    
    ##-- send msg to the server owner --##
    owner = server.owner

    welcome = """
_`Hello there!`_

Nice to meet you, I am Rawr!!
I'm a simple Tree of Savior Discord bot that can help you and your community find and gather information regarding ToS.

Here, I am request permission to stay in your server.
- Rawr
    """
    await bot.send_message(owner, welcome)

    ##-- send msg to the 1st text channel on the server --##
    chch = server.channels

    spawn = """
```css
"When you meet someone for the first time, that's not the whole book. That's just the first page."
``` 
:ghost: Hello Hooman! I'm **Rawr!**

I am a simple bot that aims to help Tree of Savior players find information related to ToS.
Use `!rawr help` to find out more commands.
Alright Boys, Rawr at your service!! :sunglasses:
================================================================
    """   
    for channel in server.channels:
        if channel.type == discord.ChannelType.text:
            try:
                await bot.send_message(channel, spawn)
                break
            except discord.errors.Forbidden:
                continue
                break


###-- help --###
@bot.command(pass_context=True)
async def help(ctx):

    halpme = """

**Rawr Help**
```md
<prefix : !rawr>
<format : prefix command>
    e.g : !rawr 
```
**List of commands:**
```md
# help :
  this message

# hello:
  greets the bot

# news: 
  get latest news/updates from Tree of Savior official website

# ping:
  ping the bot

# ktest:
  get link for ktest version of tos.neet

# update:
  get link for latest datamined file(s)

# planner:
  get link for class/build planner

# inv:
  get my invitation link

# get item info:
  cmd: get "item name"
  < e.g. : !rawr get solmiki >
  /* important: only use this command to find info for crafted item(s) and not cards, materials, recipes etc. *

# get skill info:
  scommand: skill "class name"
  < e.g. : !rawr skill diev >
  /* you may use shorten class name (e.g. sr, pd, diev etc.) *
```
    """

    await bot.whisper(halpme)
    # await bot.send_message(ctx.message.author, halpme)
    # await bot.send_message(ctx.message.author, content=halpme)


###-- hello --###
@bot.command()
async def hello():
    await bot.say(":laughing: Hello!")

###-- who --###
@bot.command()
async def who():
    await bot.say("Full-fledged Hero!!")

###-- ping --###
@bot.command()
async def ping(*args):
    await bot.say(":ping_pong: Pong!")

###-- die --###
@bot.command(hidden=True, no_pm=True)
async def die():
    sys.exit(0)

###-- ktest --###
@bot.command()
async def ktest():
    await bot.say("Let's see the future!!  " + "https://tos-ktest.neet.tv/")

###-- update --###
@bot.command()
async def update():
    await bot.say("Check what is new!!  " + "https://tos.neet.tv/changes")

###-- planner --###
@bot.command()
async def planner():
    await bot.say("Plan your character build!!  " + "https://tos.neet.tv/skill-planner")

###-- invite --###
@bot.command()
async def inv():
    invt = "https://discordapp.com/api/oauth2/authorize?client_id=336363921466195968&scope=bot&permissions=0"
    await bot.say("**Use this link to invite me to your server.**\n\n" + invt)


###-- get / item --###
def get_choice(r):
    return (r.content.isdigit() and int(r.content) >= 1 and int(r.content) <= len(result_search))

@bot.command(pass_context=True, no_pm=True)
async def get(ctx, *name):

    await bot.type()

    # get keyword #
    name = '+'.join(name)

    r = urllib.request.urlopen('https://tos.neet.tv/items?name=' + name + '&f=1').read()
    soup = BeautifulSoup(r, 'html.parser')
    result_table = soup.find('table', {"class": 'results-table'}).find('tbody').find_all('tr')

    item_names = []
    item_types = []
    item_links = []
    result_search = ''
    res_len = len(result_table)
    start = 0
    end = 7

    for no, row in enumerate(result_table[start:end], start=0):
        columns = row.find_all('td')
        item_links.append(columns[1].find('a').get('href'))
        item_names.append(columns[2].string)
        item_types.append(columns[3].string)

        result_search += str(no + 1) + '. ' + columns[2].get_text() + ' - [' + columns[3].get_text() + ']' + '\n'

    # send search result - multiple choice #
    await bot.say(content=ctx.message.author.mention + "  **Please choose one by giving its number**, type `next` or `>` to display more result." + "\n" + str(result_search))

    # waiting for response from user #
    while True:
        choice = await bot.wait_for_message(timeout=30.0, author=ctx.message.author)

        if choice is None:
            await bot.say('too slow...:smirk:')
            break

        elif choice.content == 'next' or choice.content == '>':

                    start += 7
                    end += 7
                    result_search = ""
                    for no, row in enumerate(result_table[start:end], start=start):
                        columns = row.find_all('td')
                        item_links.append(columns[1].find('a').get('href'))
                        item_names.append(columns[2].string)
                        item_types.append(columns[3].string)

                        result_search += str(no + 1) + '. ' + columns[2].get_text() + ' - [' + columns[3].get_text() + ']' + '\n'

                    await bot.say(content=ctx.message.author.mention + "  **Please choose one by giving its number**, type `next` or `>` to display more result." + "\n" + str(result_search))

    # send search result - embed #
        elif choice.content.isdigit() and int(choice.content) >= 1 and int(choice.content) <= len(result_search):

            choice = int(choice.content)
            items = get_item('https://tos.neet.tv' + item_links[choice - 1])

            embed = discord.Embed(colour=discord.Colour(0xF16F9B), description=items['description'], timestamp=datetime.datetime.utcfromtimestamp(1507360237))
            embed.set_thumbnail(url=items['thumbnail'])
            embed.set_author(name=items['title'], url='https://tos.neet.tv' + item_links[choice - 1], icon_url="http://bestonlinegamesreview.com/wp-content/uploads/2016/04/p1_2006411_5eae6fd9.png")
            embed.set_footer(text="tos.neet.tv", icon_url="https://tos.neet.tv/images/hairacc/hairacc_80_fez.png")
            embed.add_field(name="Requirement", value=items['min_level'], inline=True)
            embed.add_field(name="Grade", value=items['grade'], inline=True)
            for name, value in items['stats'].items():
                embed.add_field(name=name, value=value, inline=True)

            addsts = '```' + '\n'.join(["{}: {}".format(*item) for item in items['additional'].items()]) + '```'
            embed.add_field(name="Additional Stats", value=addsts, inline=False)
            if len(items['bonus']) > 0:
                embed.add_field(name="Bonus Stats", value='```' + '\n'.join(items['bonus']) + '```', inline=False)

            setbns = '\n'.join(["{}: {}".format(*item) for item in items['setbonus'].items()])
            if setbns != '':
                embed.add_field(name="Set Bonus", value='```' + setbns + '```', inline=True)

            await bot.say(content=ctx.message.author.mention + "\nThis is your search result!\n_Click the item name to open it on your browser._", embed=embed)
            break
#####


### get skill ###
@bot.command(pass_context=True, no_pm=True)
async def skill(ctx, *job):

    await bot.type()

    # get keyword #
    with open('classes2.json') as f: classes2.json
        content = f.read()

    tos_classes2 = json.loads(content)

    for tos_class in tos_classes2:
        tos_class['regex'] = re.compile(tos_class['regex'], re.IGNORECASE)

    response = "\nNot Found\n"

    keyword = ' '.join(job)

    for tos_class in tos_classes2:
        if tos_class['regex'].match(keyword):
            code, name = tos_class['code'], tos_class['name']
            print('Founded?: ' + name + " :" + code)
            break

    jobs = code

    r = urllib.request.urlopen('https://tos.neet.tv/skills?cls=' + jobs + '&f=1').read()
    soup = BeautifulSoup(r, 'html.parser')
    result_table = soup.find('table', {"class": 'results-table'}).find('tbody').find_all('tr')

    skill_names = []
    skill_types = []
    skill_links = []
    result_search = ''
    skill_res = ''
    res_len = len(result_table)

    for no, row in enumerate(result_table):
        columns = row.find_all('td')
        skill_links.append(columns[1].find('a').get('href'))
        skill_names.append(columns[2].string)
        skill_types.append(columns[3].string)

        result_search += str(no + 1) + '. ' + columns[2].get_text() + ' - [' + columns[3].get_text() + ']' + ' ------ ' + columns[1].find('a').get('href') + '\n'
        skill_res += str(no + 1) + '. ' + columns[2].string + '\n'

    # send search result - multiple choice #
    await bot.say(content=ctx.message.author.mention + "\n**Please choose one by giving its number:**" + "\n" + (skill_res))

    # waiting for response from user #
    while True:
        choice = await bot.wait_for_message(timeout=30.0, author=ctx.message.author)

        if choice is None:
            await bot.say('too slow...:smirk:')
            break

    # send search result - embed #
        elif choice.content.isdigit() and int(choice.content) >= 1 and int(choice.content) <= len(result_search):
            choice = int(choice.content)
            items = skill_info('https://tos.neet.tv' + skill_links[choice - 1])

            embed = discord.Embed(colour=discord.Colour(0xD2EE8A), description=items['description'], timestamp=datetime.datetime.utcfromtimestamp(1507360237))

            # embed.set_image(url="https://tos.neet.tv/images/equip/icon_item_shirts_acolyte_silver.png")
            embed.set_thumbnail(url=items['thumbnail'])

            embed.set_author(name=items['title'], url='https://tos.neet.tv' + skill_links[choice - 1], icon_url="http://bestonlinegamesreview.com/wp-content/uploads/2016/04/p1_2006411_5eae6fd9.png")

            embed.set_footer(text="tos.neet.tv", icon_url="https://tos.neet.tv/images/hairacc/hairacc_80_fez.png")

            sklinfo = '```' + '\n'.join(["{:<15}: {}".format(*item) for item in items['adin'].items()]) + '```'

            embed.add_field(name="Skill Info", value=sklinfo, inline=True)

            if len(items['attribs']) > 0:
                sklatrb = '```' +'\n\n'.join(["{}\n{}".format(*item.values()) for item in items['attribs']]) + '```'
                embed.add_field(name="Attributes", value=sklatrb, inline=False)

            await bot.say(content=ctx.message.author.mention + " This is your search result!", embed=embed)
            break

#####


### get news - official website ###
@bot.command(pass_context=True, no_pm=True)
async def news(ctx):

    await bot.type()

    r = urllib.request.urlopen('https://treeofsavior.com/page/news/').read()
    soup = BeautifulSoup(r, 'html.parser')
    resnews = soup.find(id= 'news_box_wrap').find_all('div', {"class": 'news_box'}, limit = 5)


    news_list = ""
    for n, news in enumerate(resnews, start=1):
        title = news.find('h3').get_text()
        link = 'https://treeofsavior.com' + news.find('a').get('href')

        news_list +=  "{}. [{}]({})\n".format(str(n), title, link)

    embed = discord.Embed(colour=discord.Colour(0x1abc9c), description="[All](https://treeofsavior.com/page/news/?n=1) | [Event](https://treeofsavior.com/page/news/?c=33&n=1) | [Patch Notes](https://treeofsavior.com/page/news/?c=3&n=1) | [Dev's Blog](https://treeofsavior.com/page/news/?c=31&n=1) | [Known Issues](https://treeofsavior.com/page/news/?c=32&n=1)", timestamp=datetime.datetime.utcfromtimestamp(1509378412))

    embed.set_thumbnail(url="https://treeofsavior.com/img/common/logo.png")
    embed.set_author(name="Tree Of Savior News & Update", url="https://treeofsavior.com/page/news/", icon_url="http://bestonlinegamesreview.com/wp-content/uploads/2016/04/p1_2006411_5eae6fd9.png")
    embed.set_footer(text="tree of savior - a buggy mmorpg")

    nlist = "".join(news_list)# for item in news_list
    embed.add_field(name="Patch Notes & News", value=nlist, inline = False)

    await bot.say(embed=embed)

bot.run(os.environ['BOT_TOKEN'])
