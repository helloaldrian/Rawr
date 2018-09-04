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
from paginator import Pages

###-- Invitation Link --###
#https://discordapp.com/api/oauth2/authorize?client_id=336363921466195968&scope=bot&permissions=0

bot = commands.Bot(command_prefix='!rawr ', description='just another silly tree of savior bot', pm_help = True)

bot.remove_command("help")


VERSION='0.3.1'
CHANGELOG="""
```md
[Changelog](version: 0.3.1)
```
```md
# Change:
* Fix:
    - Tidy up some stuff

# Extra:
* Contact @Jiyuu#6312 for err... w/e(?)
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
    #         # channel = get_first_text_channel(server)

    #         # if channel is not None:
    #         #     await bot.send_message(channel, CHANGELOG)

    #         for channel in server.channels:
    #             if channel.type == discord.ChannelType.text:
    #                 try:
    #                     await bot.send_message(channel, CHANGELOG)
    #                     break
    #                 except discord.errors.Forbidden:
    #                     continue
    #                     break

    #         db['servers'][server.id] = VERSION

    # with open(os.path.join(__location__, 'db.json'), 'w') as f:
    #     json.dump(db, f, indent=4)

    await bot.change_presence(game=discord.Game(name="MONSTER HUNTER: WORLD"), status=discord.Status("online"))

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

**[Rawr Help]**
```md
<prefix : !rawr>
<format : prefix command>
    e.g : !rawr news
          !rawr get masinios
```
**[List of commands:]**
```md
# help /halp:
  this message

# hello:
  greets the bot

# news:
  get latest news/updates from Tree of Savior official website

# ping:
  ping the bot

# ktest: (404)
  get link for ktest version of tos.neet

# update / updates: (404)
  get link for latest datamined file(s)

# planner:
  get link for class/build planner

# inv / invite:
  get my invitation link

# pccu:
  get tos's player statistics

# lv / leveling:
  get link for leveling guide (reddit)

# rank:
  get class build rankings (based on itos official website)

# explo:
  get link for explorer's gimmick & new collections guide (made by TerminalEssence and friends)
  
# build
  get builds compilation docs made by Palemoon.
  
# unlock / hidden
  Get hidden class/rank 8 class unlock guides doc made by Awoomoon.
  
# faq
  get reddit link for newbie/returning player discussion
  
# addon
  get link to download latest addon manager, by MizukiBelhi. 
  
# guide
  get link for guide and class breakdown, by Mr pudding lover. 

# pnt:
  get pastebin link for ktos/ktest patch notes translation from Greyhiem & Gwenyth.

# get / item:
  - get item info
  command: get "item name"
  < e.g. : !rawr get solmiki >
  /* important: now you can search any item(s) information *

# skill:
  - get skill info
  command: skill "class name"
  < e.g. : !rawr skill diev >
  /* you may use class name abbreviation/alias (e.g. sr, pd, diev etc.) *
```
    """

    await bot.whisper(halpme)
    # await bot.send_message(ctx.message.author, halpme)
    # await bot.send_message(ctx.message.author, content=halpme)


###-- hello --###
@bot.command(pass_context=True)
async def hello():
    me = """
Hello, I am **Rawrr**

I'm a simple discord bot born to help Tree of Savior's Discord community members find info about items, skills, ~~maps~~ and etc.
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
#@bot.command(hidden=True, no_pm=True)
#async def die():
    #sys.exit(0)

###-- ktest --###
#@bot.command()
#async def ktest():
    #await bot.say("**[Let's see the future!!]**\n" + "https://tos-ktest.neet.tv/")

###-- build --###
@bot.command(aliases=['builds'])
async def build():
    await bot.say("**[Compilation of Practical Class Build Guide!!]**\n_- builds made by reddit community & compiled by Palemoon_\n" + "https://docs.google.com/document/d/1SF3CeTi9umcI9tFmZmRCNUHEJQwtgSMmVKqq9sCjnPY/edit?usp=sharing")    
    
###-- update --###
#@bot.command(aliases=['updates'])
#async def update():
    #await bot.say("**[Check what is new!!]**\n" + "https://tos.neet.tv/changes")
    
###-- addon manager --###
@bot.command()
async def addon():
    await bot.say("**[Grab your Tree of Savior addons manager!!]**\n_- by MizukiBelhi_\n" + "https://github.com/MizukiBelhi/Tree-of-Savior-Addon-Manager/releases/tag/v0.3.1-alpha.2")

###-- faq --###
@bot.command(aliases=['faq', 'return'])
async def newbie():
    await bot.say("**[FAQ for newbie and returning player!!]**\n_- by Palemoon_\n" + "https://reddit.com/r/treeofsavior/comments/8g78qr/read_first_new_or_returning_players_info_inside/"  + "\n\n**[Official Newbie & Returning Player Guide!!]**\n" + "https://treeofsavior.com/page/news/view.php?n=1450" + "\nhttps://treeofsavior.com/page/news/view.php?n=1454") 

###-- holy guides --###
@bot.command()
async def guide():
    await bot.say("**[Guide blog based on ktos/ktest!!]**\n" + "https://wizardguidetreeofsavior.blogspot.com" + "\n\n**[Various class overview by Ritsu!!]**\n" + "http://kiyoshiro-ritsu.tumblr.com/")
    
###-- unlock guide --###
@bot.command(aliases=['hidden'])
async def unlock():
    await bot.say("**[Hidden class/rank 8 class unlock guides!!]**\n_- by Palemoon_\n" + "https://docs.google.com/document/d/1aEOF-WjTiKr1WE-bYHNIyl0_JnVX8_rUzCoclFDVQrY/edit?usp=sharing" + "\n\n**[Tree of Savior Hidden Secrets & Lores!!]**\n_- by Ximi_\n" + "http://toshidden.blog.fc2.com/")

###-- planner --###
@bot.command()
async def planner():
    await bot.say("**[Plan your character build!!]**\n" + "https://tos.neet.tv/skill-planner" + "\nhttp://toscamp.com/tos/ranksimul/" + "\nhttp://tos-th.com/skill-simulator.html")

###-- gimmick --###
@bot.command()
async def explo():
     await bot.say("**[Explorer's Gimmick & New Collections Guide]**\n[*credits : TerminalEssence & Friends*]\n\n" + "https://docs.google.com/document/d/1ihOzgxe8SrV8aRwYq1xMUwiTvsTNHGibJ6yBXFATaTg/edit?usp=sharing")

###-- leveling --###
# @bot.command(aliases=['leveling'])
# async def lv():
#     await bot.say("**[Leveling Guide]**\n[based on shion@inven.co.kr]\n\n" + "https://www.reddit.com/r/treeofsavior/comments/8bg0mb/updated_levelling_guide/")

##-- leveling (2) --###
@bot.command(pass_context=True, aliases=['leveling', 'lvl', 'level'])
async def lv(ctx):
    pages = [
"**Read :** FAQ for newbie and returning player!! \n**Command :** !rawr faq \n\n_- Navigate using the reaction emotes._\n_- Navigation buttons/reactions can only be used by individual who input the **!rawr lv** command._\n_- Guide start from page 2._\n_- Press_ \N{INFORMATION SOURCE} _if you're confused._",
"***Lvl 1 ~ 50:***\n\nKill **Hanamings** and other mobs at **East Siauliai Woods** and **West Siauliai Woods** for abit until you have enough silver to get Blessing and Sacrament buffs from pardoners in Klaipeda (usually about 3000 silver is enough). Get the buffs then run all the way to **Tenet Garden** and kill the mobs above the goddess statue there, they are plentiful and have fast respawn times. You can also choose to go inside **Tenet Church B1** and kill stuff there if you wish.",
"***Lvl 50 ~ 114:***\n\nGo to **Feretory Hills** and kill the **Hallowventers** there along with other mobs. The current state of game makes it so that it is difficult to find matches in lower level dungeon queues unless you shout or are in a guild. therefore grinding here is more effective than waiting in town for a queue pop. You can also continue to grind here if you have already ran out of dungeon runs if you were able to get a match. Once you get closer to lvl 100ish, you may also choose to go grind at **Sicarius 1f**. From **level 100**, you can start to level up using the Challenge mode feature, it is best to go with a party around your level when attempting Challenge mode.",
"***Lvl 114 ~ 202:***\n\nMake your way to **Demon Prison District 2** and kill the mobs there, they are plentiful and respawn quickly. You will be able to grind here for quite a while due to the sheer number of mobs and the fast respawn rate. If you find that there are too many people at Demon Prison District 2, around level 130ish you can make your way to **2nd Demon Prison** and grind the mobs there instead. **(The maps 2nd Demon Prison and Demon Prison District 2 are different maps, do not confuse them as the same map)**, An alternate path is to try the Challenge Mode feature around maps of your level.",
"***Lvl 202 ~ 230:***\n\nGrind around **Cranto Coast** and do the Challenge mode there. If you still need abit more exp to reach 230 then consider doing some quests too. **Neighport Church East Building** is a great place to grind too once your daily challenge modes are done.",
"***Lvl 230 ~ 270:***\n\nGo to **Kalejimas Visiting Room** and grind the various mobs there for exp. Remember to keep up with your daily dungeon runs and Challenge mode entries. If you still need exp in this stage, then consider doing a few quests around that area or 100 percent explore the maps for exp cards which you can redeem at the **Wings of Viboria NPC at Klaipeda**.",
"***Lvl 270 ~ 315:***\n\nKeep up with Daily dungeons around your level and make your way to **Timerys Temple**. This will be your new home for grinding and Challenge modes until lvl 315. Make sure to use up to date equipment for your level because the mobs will hurt. Timerys Temple also happens to be a great map for gem farming and silver farming.",
"***Lvl 315 ~ 360:***\n\nYou can now start to level at **Sausys Room 9**, this is a great place to grind and do your daily challenge modes until you are max level and even at max level, you can continue to do Challenge modes here for silver and loot. Remember to keep up to date with your equipment and work towards better equips. If you are around lvl 340ish and you are getting bored of Sausys Room 9, you can go to **Narvas Temple** for a change of scenery and do the Challenge mode or grind there.", 
"***Lvl 350 ~ 390:***\n\nHead over to **Spell Tome Town** and do the Challenge modes there, it is a great place for this due to the narrow areas and high level monsters. Supplement your Challenge Mode grinds by questing around areas of **Astral Tower, Barynwell Waters, Spell Tome Town and Starry Town**. Monsters will be abit tough so it is reccomended to attempt the Challenge mode grinds and such with a party. It is also a great area to farm for high level loot."
    ]

    for index, page in enumerate(pages):
        pages[index] = 'click title for reddit post\n \n' + page

    pages = Pages(bot, message=ctx.message, entries=pages, per_page=1, with_number=False)
    await pages.paginate()

###-- invite --###
@bot.command(aliases=['invite'])
async def inv():
    invt = "https://discordapp.com/api/oauth2/authorize?client_id=336363921466195968&scope=bot&permissions=0"
    await bot.say("**[Use this link to invite me to your server.]**\n\n" + invt)

###-- ranking --###
@bot.command(aliases=['rankings'])
async def rank():
    await bot.say("**[The most popular TOS class builds of all time]**\n[Update periodically]\n\n" + "https://treeofsavior.com/page/class/ranking.php")

###-- patch notes translation --###
@bot.command()
async def pnt():
    patch = """
**[Ktest/Ktos - Patch Notes Translation]**
_(no longer maintained)_

**Greyhiem's**  https://pastebin.com/u/Greyhiem
**Gwenyth's**  https://pastebin.com/u/sunhwapark
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
    msg = await bot.say(content=ctx.message.author.mention + "\n**Please choose one by giving its number:**" + "```" + (skill_res) + "```" + "\n")

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

            await bot.delete_message(msg)

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

    url = 'http://steamcharts.com/app/372000'

    user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
    headers = { 'User-Agent' : user_agent }

    req = urllib.request.Request(url, headers=headers)

    r = urllib.request.urlopen(req).read()
    soup = BeautifulSoup(r, 'html.parser')
    sta = soup.find_all('div', {"class": 'app-stat'})

    list1 = []
    for req in sta:
        player = int(req.find('span', {"class": 'num'}).get_text())
        list1.append('{:,}'.format(player))

    embed = discord.Embed(colour=discord.Colour(0x1abc9c), title="Tree of Savior (English Ver.)", description="Tree of Savior (abbreviated as TOS thereafter) is an MMORPG in which you embark on a journey to search for the goddesses in the world of chaos. Fairy-tale like colors accompanied with beautiful graphics in TOS will have you reminiscing about precious moments all throughout the game.\n\n[steamdb.info](https://steamdb.info/app/372000/graphs/)\n[steamspy.com](https://steamspy.com/app/372000)\n[steamcharts.com](http://steamcharts.com/app/372000)\n", timestamp=datetime.datetime.now())

    embed.set_image(url="http://cdn.akamai.steamstatic.com/steam/apps/372000/header.jpg")
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
