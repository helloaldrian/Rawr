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
import urllib.parse
from urllib.parse import urlencode

###-- Invitation Link --###
#https://discordapp.com/api/oauth2/authorize?client_id=336363921466195968&scope=bot&permissions=0

bot = commands.Bot(command_prefix='!rawr ', description='this is rawr test!', pm_help = True)

bot.remove_command("help")


VERSION='0.1.7'
CHANGELOG="""
```md
[Changelog](version: 0.1.7)
```
```md
# Added Features:
* Changelog created
* New commands:
    - pccu, TOS stats.
    - pnt, ktos/ktest patch notes translation from Greyhiem & Gwenyth.

# Changes:
* Rank reset event, Rawrr! change its build.
    - Rawrr now can farming at tos.neet more efficiently.
    - Rawrr farming equipments upgraded, search more items & information!
* Contents of hello command changed, know Rawrr better!!
* Auto delete choices dialog, i heard people hate spammy chats.

# Incoming:
* Beautification of help formatting.
* Learn ability to farming at ktest & ktos, Rawrr is taking Korean Language Class now!

# Extra:
* Blame @Jiyuu#6312 for broken grammar & commands.
```
"""

db = {'servers': {}}

def get_first_text_channel(server):
    for channel in server.channels:
        if channel.type == discord.ChannelType.text:
            return channel
    return None


###-- prep --###
@bot.event
async def on_ready():
    # global db

    # __location__ = os.path.realpath( os.path.join(os.getcwd(), os.path.dirname(__file__)))

    # if os.path.isfile(os.path.join(__location__, 'db.json')):
    #     with open(os.path.join(__location__, 'db.json')) as f:
    #         db = json.loads(f.read())

    # for server in bot.servers:
    #     if server.id not in db['servers'].keys() or (server.id in db['servers'].keys() and db['servers'][server.id] != VERSION):
    #         channel = get_first_text_channel(server)

    #         if channel is not None:
    #             await bot.send_message(channel, CHANGELOG)

    #         db['servers'][server.id] = VERSION

    # with open(os.path.join(__location__, 'db.json'), 'w') as f:
    #     json.dump(db, f, indent=4)

    await bot.change_presence(game=discord.Game(name="[!rawr help]"), status=discord.Status("online"))
    
    print('=============================')
    print('     Are you ready Rawr?!'    )
    print('         '+ bot.user.name     )
    print('-----------------------------')
    print('        Let\'s Rawr!!        ')
    print('-----------------------------')
    print("  _____                      ")
    print(" |  __ \                     ")
    print(" | |__) |__ ___      ___ __  ")
    print(" |  _  // _` \ \ /\ / / '__| ")
    print(" | | \ \ (_| |\ V  V /| |    ")
    print(" |_|  \_\__,_| \_/\_/ |_|    ")
    print('                             ')
    print('=============================')


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
@bot.command(pass_context=True, aliases=['halp'])
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

# pccu:
  get tos's player statistics

# pnt:
  get pastebin link for ktos/ktest patch notes translation from Greyhiem & Gwenyth.

# get / item:
  - get item info
  command: get "item name"
  < e.g. : !rawr get solmiki >
  /* important: only use this command to find info for crafted item(s) and not cards, materials, recipes etc. *

# skill:
  - get skill info
  command: skill "class name"
  < e.g. : !rawr skill diev >
  /* you may use shorten class name (e.g. sr, pd, diev etc.) *
```
    """

    await bot.whisper(halpme)
    # await bot.send_message(ctx.message.author, halpme)
    # await bot.send_message(ctx.message.author, content=halpme)


###-- hello --###
@bot.command(pass_context=True)
async def hello():
    me = """
Hello, I am **Rawr**
I'm a simple discord bot born to help Tree of Savior's Discord community members find info about items, skills, maps and etc.
I am created by the desire of my creator to obtain basic information regarding ToS items or skills without having to open the browser.

If you have any feedback or suggestion to improve **Rawrr!**.
**Please touch,**  @Jiyuu#6312
**Visit us,**  https://github.com/helloaldrian/Rawr
"""
    await bot.say(me)

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
@bot.command(aliases=['updates'])
async def update():
    await bot.say("Check what is new!!  " + "https://tos.neet.tv/changes")

###-- planner --###
@bot.command()
async def planner():
    await bot.say("Plan your character build!!  " + "https://tos.neet.tv/skill-planner")

###-- invite --###
@bot.command(aliases=['invite'])
async def inv():
    invt = "https://discordapp.com/api/oauth2/authorize?client_id=336363921466195968&scope=bot&permissions=0"
    await bot.say("**Use this link to invite me to your server.**\n\n" + invt)

###-- patch notes translation --###
@bot.command()
async def pnt():
    patch = """
```Ktest/Ktos - Patch Notes Translation:```
**Greyhiem's**      : https://pastebin.com/u/Greyhiem
**Gwenyth's**       : https://pastebin.com/u/sunhwapark
    """
    await bot.say(patch)


###-- get / item --###
def get_choice(r):
    return (r.content.isdigit() and int(r.content) >= 1 and int(r.content) <= len(result_search))

@bot.command(pass_context=True, aliases=['item'], no_pm=True)
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
    msg = await bot.say(content=ctx.message.author.mention + "\n**Please choose one by giving its number**,\n_type `next` or `>` to display more result._" + "```" + str(result_search) + "```" + "\n")


    # waiting for response from user #
    while True:
        choice = await bot.wait_for_message(timeout=30.0, author=ctx.message.author)

        if choice is None:
            await bot.say('_**too slow...**_   **(╯°□°）╯︵ ┻━┻**')
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

                    await bot.delete_message(msg)

                    msg = await bot.say(content=ctx.message.author.mention + "\n**Please choose one by giving its number**,\n_type `next` or `>` to display more result._" + "```" + str(result_search) + "```" + "\n")


    # send search result - embed #
        elif choice.content.isdigit() and int(choice.content) >= 1 and int(choice.content) <= len(result_search):
            choice_number = int(choice.content)
            embed = get_item('https://tos.neet.tv' + item_links[choice_number - 1])

            # await bot.delete_message(choice)
            await bot.delete_message(msg)
            # await bot.delete_message(ctx.message)

            await bot.say(content=ctx.message.author.mention + "\n**This is your search result!**\n_Click the item name to see more info on your browser._", embed=embed)
            break

##-- eol --##


### get skill ###
@bot.command(pass_context=True, no_pm=True)
async def skill(ctx, *job):

    await bot.type()

    # get keyword #
    __location__ = os.path.realpath( os.path.join(os.getcwd(), os.path.dirname(__file__)))

    with open(os.path.join(__location__, 'classes2.json')) as f:
    # with open('classes2.json') as f:
        content = f.read()

    tos_classes2 = json.loads(content)

    for tos_class in tos_classes2:
        tos_class['regex'] = re.compile(tos_class['regex'], re.IGNORECASE)

    response = "\nNot Found\n"

    keyword = ' '.join(job)

    for tos_class in tos_classes2:
        if tos_class['regex'].match(keyword):
            code, name = tos_class['code'], tos_class['name']
            # print('Founded?: ' + name + " :" + code)
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
    await bot.say(content=ctx.message.author.mention + "\n**Please choose one by giving its number:**" + "```" + (skill_res) + "```" + "\n")

    # waiting for response from user #
    while True:
        choice = await bot.wait_for_message(timeout=30.0, author=ctx.message.author)

        if choice is None:
            await bot.say('_**too slow...**_   **(╯°□°）╯︵ ┻━┻**')
            break

    # send search result - embed #
        elif choice.content.isdigit() and int(choice.content) >= 1 and int(choice.content) <= len(result_search):
            choice = int(choice.content)
            items = skill_info('https://tos.neet.tv' + skill_links[choice - 1])

            embed = discord.Embed(colour=discord.Colour(0xD2EE8A), description=items['description'], timestamp=datetime.datetime.now())

            # embed.set_image(url="https://tos.neet.tv/images/equip/icon_item_shirts_acolyte_silver.png")
            embed.set_thumbnail(url=items['thumbnail'])

            embed.set_author(name=items['title'], url='https://tos.neet.tv' + skill_links[choice - 1], icon_url="http://bestonlinegamesreview.com/wp-content/uploads/2016/04/p1_2006411_5eae6fd9.png")

            embed.set_footer(text="tos.neet.tv", icon_url="https://tos.neet.tv/images/hairacc/hairacc_80_fez.png")

            sklinfo = '```' + '\n'.join(["{:<15}: {}".format(*item) for item in items['adin'].items()]) + '```'

            embed.add_field(name="Skill Info", value=sklinfo, inline=True)

            if len(items['attribs']) > 0:
                sklatrb = '```' +'\n\n'.join(["{}\n{}".format(*item.values()) for item in items['attribs']]) + '```'
                embed.add_field(name="Attributes", value=sklatrb, inline=False)

            await bot.say(content=ctx.message.author.mention + "\n**This is your search result!**\n_Click the skill name to see more info on your browser._", embed=embed)
            break

#####


### get news - official website ###
@bot.command(pass_context=True, no_pm=True)
async def news(ctx):

    await bot.type()

    r = urllib.request.urlopen('https://treeofsavior.com/page/news/').read()
    soup = BeautifulSoup(r, 'html.parser')
    resnews = soup.find(id= 'news_box_wrap').find_all('div', {"class": 'news_box'}, limit = 7)


    news_list = ""
    for n, news in enumerate(resnews, start=1):
        title = news.find('h3').get_text()
        link = 'https://treeofsavior.com' + news.find('a').get('href')

        news_list +=  "{}. [{}]({})\n".format(str(n), title, link)

    embed = discord.Embed(colour=discord.Colour(0x1abc9c), description="[All](https://treeofsavior.com/page/news/?n=1) | [Event](https://treeofsavior.com/page/news/?c=33&n=1) | [Patch Notes](https://treeofsavior.com/page/news/?c=3&n=1) | [Dev's Blog](https://treeofsavior.com/page/news/?c=31&n=1) | [Known Issues](https://treeofsavior.com/page/news/?c=32&n=1)", timestamp=datetime.datetime.now())

    embed.set_thumbnail(url="https://treeofsavior.com/img/common/logo.png")
    embed.set_author(name="Tree Of Savior News & Update", url="https://treeofsavior.com/page/news/", icon_url="http://bestonlinegamesreview.com/wp-content/uploads/2016/04/p1_2006411_5eae6fd9.png")
    embed.set_footer(text="tree of savior - a buggy mmorpg")

    nlist = "".join(news_list)# for item in news_list
    embed.add_field(name="Patch Notes & News", value=nlist, inline = False)

    await bot.say(embed=embed)

### get PCCU from steamspy ###
@bot.command(pass_context=True, no_pm=True)
async def pccu(ctx):

    await bot.type()

    url = 'https://steamdb.info/app/372000/graphs/'

    user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
    headers = { 'User-Agent' : user_agent }

    req = urllib.request.Request(url, headers=headers)

    r = urllib.request.urlopen(req).read()
    soup = BeautifulSoup(r, 'html.parser')
    sta = soup.find('ul', {"class": 'steamspy-stats'}).find_all('li')

    list1 = []
    for req in sta:
        player = req.find('strong').get_text()
        list1.append(player)

    embed = discord.Embed(colour=discord.Colour(0x1abc9c), title="Tree of Savior (English Ver.)", description="Tree of Savior (abbreviated as TOS thereafter) is an MMORPG in which you embark on a journey to search for the goddesses in the world of chaos. Fairy-tale like colors accompanied with beautiful graphics in TOS will have you reminiscing about precious moments all throughout the game.\n\n[steamdb.info](https://steamdb.info/app/372000/graphs/)\n[steamspy.com](https://steamspy.com/app/372000)", timestamp=datetime.datetime.now())

    embed.set_image(url="https://steamdb.info/static/camo/apps/372000/header.jpg")
    embed.set_thumbnail(url="http://bestonlinegamesreview.com/wp-content/uploads/2016/04/p1_2006411_5eae6fd9.png")
    embed.set_author(name="Online Player Tracker", url="https://treeofsavior.com", icon_url="http://bestonlinegamesreview.com/wp-content/uploads/2016/04/p1_2006411_5eae6fd9.png")
    embed.set_footer(text="tree of savior - a buggy mmorpg")

    # nlist = "".join(news_list)# for item in news_list
    # embed.add_field(name="Right Now", value=sta[0].find('strong').get_text(), inline = False)
    embed.add_field(name="Right Now", value=list1[0], inline = True)
    embed.add_field(name="24 Hour Peak", value=list1[1], inline = False)
    embed.add_field(name="All The Time Peak (2 yrs ago)", value=list1[2], inline = False)

    await bot.say(embed=embed)









bot.run(os.environ['BOT_TOKEN'])
