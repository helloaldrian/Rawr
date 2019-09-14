import asyncio
import datetime
import json
import re
from inspect import cleandoc
from pathlib import Path

import aiohttp
import discord
import feedparser
from bs4 import BeautifulSoup
from discord.ext import commands

from urlbreak import get_item, skill_info
from urlbreak import format_embed_description as FED


NEWLINE = '\n'

# Rawr-specific

FOOTER = "Rawr | Tree of Savior | IMC Games Co.,Ltd"

# Game - images

TOS_THUMBNAIL = (
    "http://bestonlinegamesreview.com/wp-content/uploads/2016/04"
    "/p1_2006411_5eae6fd9.png"
    )

EMBED_THUMBNAIL = (
    "https://tos.neet.tv/images/hairacc/hairacc_80_fez.png"
    )

TOS_STEAM_IMG = (
    "http://cdn.akamai.steamstatic.com/steam/apps/372000/header.jpg"
    )

# Game - external

STEAM_CHARTS = 'http://steamcharts.com/app/372000'

# Game - news

TOS_NEWS = "https://treeofsavior.com/page/news/"

NEWS_ALL = " | ".join(
    [
        f"[All]({TOS_NEWS}?n=1)",
        f"[Event]({TOS_NEWS}?c=33&n=1)",
        f"[Patch Notes]({TOS_NEWS}?c=3&n=1)",
        f"[Dev's Blog]({TOS_NEWS}?c=31&n=1)",
        f"[Known Issues]({TOS_NEWS}?c=32&n=1)"
        ]
    )

TOS_DESC = "\n".join(
    [
        (
            "Tree of Savior (abbreviated as TOS thereafter) is an MMORPG in "
            "which you embark on a journey to search for the goddesses in the "
            "world of chaos. Fairy-tale like colors accompanied with "
            "beautiful graphics in TOS will have you reminiscing about "
            "precious moments all throughout the game.\n"
            ),
        "[steamdb.info](https://steamdb.info/app/372000/graphs/)",
        "[steamspy.com](https://steamspy.com/app/372000)",
        f"[steamcharts.com]({STEAM_CHARTS})",
        ]
    )

# Game - external - tos.guru

TOSGURU_FEEDBACK = (
    "https://feedback.userreport.com/e23e275c-deb8-4560-9434-070fc22b6208/"
    )

TOSGURU_DESC = " | ".join(
    [
        "[Home](https://tos.guru/)",
        "[rjgtav's](https://www.twitch.tv/rjgtav)",
        "[Rawrr](https://github.com/helloaldrian/Rawr)",
        "[Guide](https://wizardguidetreeofsavior.blogspot.com)",
        (
            f"[Feedback]({TOSGURU_FEEDBACK})\n"
            "Welcome to Tree of Savior Database.\n"
            "The Database's goal is to provide you with the most complete, "
            "accurate and up-to-date information about the game."
            ),
        ]
    )

TOSGURU_LINKS = """
    [Maps - WIP](https://tos.guru/)
    [kTest](https://tos.guru/ktest/database/equipment)
    [Items](https://tos.guru/itos/database/items)
    [Build Simulator](https://tos.guru/itos/simulator)
    [Anvil & Transcendence Calculator](https://tos.guru/itos/database/equipment)
    """

# Etc

WARNING_502 = """
    :warning: **__502 BAD GATEWAY__** :warning:
    **ReadMe**
    ```css
    [ Hi there, this is Rawr! ]
    Since #tos.neet.tv are no longer maintained and/or accessible by Rawr, I can no longer provide a quick search & dispaly both #items and #skills information for you.
    This feature will be disabled for the time being.
    [ I am sorry for the inconvenience! ]
    ```
    **Alternative:**
    ```cpp
    #use new cmd: !rawr db
    ```
    """

file  = Path('Rawr').resolve() / 'classes2.json'
with file.open() as f:
    content = f.read()
all_classes = json.loads(content)
for tos_class in all_classes:
    tos_class['regex'] = re.compile(tos_class['regex'], re.IGNORECASE)


async def get_class(job: str):
    """Gets a class given `job`.

    Args:
        job (str): the user-supplied job to retrieve

    Returns:
        tuple (code, name): if successful
        None: otherwise

    """
    for tos_class in all_classes:
        if tos_class['regex'].match(job):
            return (tos_class['code'], tos_class['name'])
    return


async def get_results(table, start: int, links: list):
    """Gets results by slices defined by `start` and `end`.

    Args:
        table: the table
        start (int): the starting index
        links (list): contains URLs to the entries

    """
    results = []
    # Offset is currently defined at 7
    end = start + 7
    for number, row in enumerate(table[start:end], start = 0):
        columns = row.find_all('td')
        links.append(columns[1].find('a').get('href'))
        iname = columns[2].get_text()
        itype = columns[3].get_text()
        results.append(
            f'{number + 1}. {iname} - [{itype}]'
            )
    return results


class GuildOnlyCog(commands.Cog):
    """All of Rawr's guild-only commands."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases = ['item'])
    async def get(self, ctx, *name):
        #await bot.type()
        #await ctx.send(WARNING_502)
        name = '+'.join(name)
        async with aiohttp.ClientSession() as cs:
            url = f'https://tos.neet.tv/items?name={name}&f=1'
            async with cs.get(url) as r:
                soup = BeautifulSoup(await r.text(), 'html.parser')

        table = soup.find(
            'table',
            {"class": 'results-table'}
            ).find('tbody').find_all('tr')
        links = []
        results = []
        start = 0

        results = await get_results(table, start, links)

        # send search result - multiple choice #
        msg = await ctx.send(
            # This is really awkward, but I couldn't think of a way to force
            # indentation on the code block. Maybe something to improve.
            cleandoc(
                f"""
                {ctx.message.author.mention}
                **Please choose one by entering its number**
                _type `next` or `>` to display more result._
                """
                ) + cleandoc(
                f"""
                ```{NEWLINE.join(results)}
                ```
                """
                )
            )

        def pred(m):
            return m.author == ctx.author and m.channel == ctx.channel

        # waiting for response from user #
        while True:
            results = []
            try:
                choice = await self.bot.wait_for(
                    'message',
                    check = pred,
                    timeout = 30.0,
                    )
            except asyncio.TimeoutError:
                await ctx.send('_**too slow...**_   **(╯°□°）╯︵ ┻━┻**')
                return
            if choice.content == 'next' or choice.content == '>':
                start += 7
                results = await get_results(table, start, links)
                await msg.delete()
                if results:
                    msg = await ctx.send(
                        cleandoc(
                            f"""
                            {ctx.message.author.mention}
                            **Please choose one by entering its number**
                            _type `next` or `>` to display more result._
                            ```{NEWLINE.join(results)}
                            ```
                            """
                            )
                        )
                    continue
                else:
                    await ctx.send(
                        "**No more results were found.**"
                        )
                    return
            # send search result - embed #
            elif (
                choice.content.isdigit()
                and int(choice.content) in range(1, len(results) + 1)
                ):
                choice_number = int(choice.content)
                embed = await get_item(
                    f'https://tos.neet.tv{links[choice_number - 1]}'
                    )
                await msg.delete()
                await ctx.send(
                    cleandoc(
                        f"""
                        {ctx.message.author.mention}
                        **This is your search result!**
                        _Click the item name to see more info on your browser._
                        """
                        ),
                    embed = embed
                    )
                return
            else:
                continue

    ### get skill ###
    @commands.command()
    async def skill(self, ctx, *job):
        #await bot.type()
        try:
            code, name = await get_class(' '.join(job))
        except TypeError: # None
            await ctx.send('You entered an invalid class!')
            return

        async with aiohttp.ClientSession() as cs:
            url = f'https://tos.neet.tv/skills?cls={code}&f=1'
            async with cs.get(url) as r:
                soup = BeautifulSoup(await r.text(), 'html.parser')

        result_table = soup.find(
            'table',
            {"class": 'results-table'}
            ).find('tbody').find_all('tr')
        links = []
        results = []
        for number, row in enumerate(result_table):
            columns = row.find_all('td')
            link = columns[1].find('a').get('href')
            links.append(link)
            skill_name = columns[2].get_text()
            results.append(
                f"{number + 1}. {skill_name}"
                )
        # send search result - multiple choice #
        msg = await ctx.send(
            # See note around line 194.
            cleandoc(
                f"""
                {ctx.message.author.mention}
                **Please choose one by entering its number**
                """
                ) + cleandoc(
                f"""
                ```{NEWLINE.join(results)}
                ```
                """
                )
            )

        def pred(m):
            return m.author == ctx.author and m.channel == ctx.channel

        # waiting for response from user #
        while True:
            try:
                choice = await self.bot.wait_for(
                    'message',
                    check = pred,
                    timeout = 30.0,
                    )
            except asyncio.TimeoutError:
                await ctx.send('_**too slow...**_   **(╯°□°）╯︵ ┻━┻**')
                return
            # send search result - embed #
            if (
                choice.content.isdigit()
                and int(choice.content) in range(1, len(results) + 1)
                ):
                choice = int(choice.content)
                current_url = f'https://tos.neet.tv{links[choice - 1]}'
                items = await skill_info(current_url)
                embed = discord.Embed(
                    colour = discord.Colour(0xD2EE8A),
                    description = items['description'],
                    timestamp = datetime.datetime.now()
                    )
                # embed.set_image(url="https://tos.neet.tv/images/equip/icon_item_shirts_acolyte_silver.png")
                embed.set_thumbnail(url = items['thumbnail'])
                embed.set_author(
                    name = items['title'],
                    url = current_url,
                    icon_url = TOS_THUMBNAIL
                    )
                embed.set_footer(
                    text = "tos.neet.tv",
                    icon_url = EMBED_THUMBNAIL
                    )
                embed.add_field(
                    name = "Skill Info",
                    value = await FED(items['adin'], "{:<15}: {}"),
                    inline = True
                    )
                sklatrb = []
                try:
                    for attrib in items['attribs']:
                        sklatrb.append(attrib['name'])
                        sklatrb.append(attrib['value'])
                        sklatrb.append(attrib['mod'])
                except Exception as e:
                    pass
                else:
                    if sklatrb:
                        embed.add_field(
                            name = "Attributes",
                            value = '```{}```'.format(
                                '\n'.join(sklatrb)
                                ),
                            inline = False
                            )
                await msg.delete()
                await ctx.send(
                    cleandoc(
                        f"""
                        {ctx.message.author.mention}
                        **This is your search result!**
                        _Click the skill name to see more info on your browser._
                        """
                        ),
                    embed = embed
                    )
                return
            else:
                # Ignore invalid input
                continue

    ### get news - official website ###
    @commands.command()
    async def news(self, ctx):
        #await bot.type()
        async with aiohttp.ClientSession(headers = headers) as cs:
            async with cs.get(TOS_NEWS) as r:
                soup = BeautifulSoup(await r.text(), 'html.parser')

        resnews = soup.find(id= 'news_box_wrap').find_all(
            'div',
            {"class": 'news_box'},
            limit = 7
            )

        news_list = []
        for n, news in enumerate(resnews, start = 1):
            title = news.find('h3').get_text()
            link = 'https://treeofsavior.com' + news.find('a').get('href')

            news_list.append(f"{n}. [{title}]({link})")

        embed = discord.Embed(
            colour = discord.Colour(0x1abc9c),
            description = NEWS_ALL,
            timestamp = datetime.datetime.now()
            )

        embed.set_thumbnail(
            url = "https://treeofsavior.com/img/common/logo.png"
            )
        embed.set_author(
            name= "Tree of Savior News & Update",
            url = TOS_NEWS,
            icon_url = TOS_THUMBNAIL
            )
        embed.set_footer(
            text = FOOTER
            )

        #nlist = "\n".join(news_list)# for item in news_list
        embed.add_field(
            name = "Patch Notes & News",
            value = "\n".join(news_list),
            inline = False
            )

        await ctx.send(embed = embed)

    ### get PCCU from steamspy ###
    @commands.command()
    async def pccu(self, ctx):
        #await bot.type()

        user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
        headers = { 'User-Agent' : user_agent }

        async with aiohttp.ClientSession(headers = headers) as cs:
            async with cs.get(STEAM_CHARTS) as r:
                soup = BeautifulSoup(await r.text(), 'html.parser')

        sta = soup.find_all('div', {"class": 'app-stat'})

        fields = []
        for req in sta:
            nplayers = int(req.find('span', {"class": 'num'}).get_text())
            fields.append(f'{nplayers:,}')

        players_now, players_day, players_all = fields

        embed = discord.Embed(
            colour = discord.Colour(0x1abc9c),
            title = "Tree of Savior (English Ver.)",
            description = TOS_DESC,
            timestamp = datetime.datetime.now()
            )

        embed.set_image(
            url = TOS_STEAM_IMG
            )
        embed.set_thumbnail(
            url = TOS_THUMBNAIL
            )
        embed.set_author(
            name = "Online Player Tracker",
            url = "https://treeofsavior.com",
            icon_url = TOS_THUMBNAIL)
        embed.set_footer(
            text = FOOTER
            )

        embed.add_field(
            name = "Right Now",
            value = players_now,
            inline = True
            )
        embed.add_field(
            name = "24 Hour Peak",
            value = players_day,
            inline = False
            )
        embed.add_field(
            name = "All The Time Peak",
            value = players_all,
            inline = False
            )

        await ctx.send(embed = embed)


    ###-- wiki --###
    @commands.command(aliases = ['wiki', 'database'])
    async def db(self, ctx):
        #await bot.type()

        embed = discord.Embed(
            colour = discord.Colour(0x1abc9c),
            description = TOSGURU_DESC,
            timestamp = datetime.datetime.now()
            )

        embed.set_image(
            url = TOS_STEAM_IMG
            )
        embed.set_thumbnail(
            url = TOS_THUMBNAIL
            )
        embed.set_author(
            name = "tos.guru",
            url = "https://tos.guru/",
            icon_url = TOS_THUMBNAIL
            )
        embed.set_footer(
            text = "Tree of Savior | rjgtav | Rawrr"
            )

        #embed.add_field(name="Placeholder", value="placeholder")
        embed.add_field(
            name = "Features",
            value = cleandoc(TOSGURU_LINKS),
            inline = False
            )

        await ctx.send(embed = embed)


    @commands.command()
    async def rss(self, ctx):
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://dark-nova.me/tos/feed.xml") as r:
                NewsFeed = feedparser.parse(await r.text())

        entry = NewsFeed.entries[0]

        await ctx.send(
            cleandoc(
                f"""
                {entry.published}
                ******
                {entry.summary}
                ------Link--------
                {entry.link}
                """
                )
            )

    async def cog_check(self, ctx):
        return ctx.guild is not None


def setup(bot):
    bot.add_cog(GuildOnlyCog(bot))
