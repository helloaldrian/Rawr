from inspect import cleandoc

import discord
from discord.ext import commands

from paginator import Pages


# Rawr-specific

HELP = """
    **[Rawr Help]**
    ```md
    <prefix : !rawr>
    <format : prefix command>
        e.g : !rawr news
              !rawr get masinios
    ```
    **[List of commands:]**
    ```md
    # help / halp:
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

    # db / wiki / database
      get TOS database link (TOS.guru)

    # pccu:
      get TOS player statistics

    # lv / leveling:
      get link for leveling guide (reddit)

    # rank:
      get class build rankings (based on iTOS official website)

    # explo:
      get link for Explorer Gimmicks & New Collections Guide (made by TerminalEssence and friends)

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
      get pastebin link for kTOS/kTEST patch notes translation from Greyhiem & Gwenyth.

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

HELLO = """
    Hello, I am **Rawrr**

    I'm a simple Discord bot born to help Tree of Savior's Discord community members find info about items, skills, ~~maps~~ and etc.
    I am created by the desire of my creator to obtain basic information regarding TOS items or skills without having to open the browser.

    If you have any feedback or suggestion to improve **Rawrr!**.
    **Please keep in touch,**  @Jiyuu#6312
    **Visit us,**  https://github.com/helloaldrian/Rawr
    """

PING = """
    **__Server Ping__**

    **How to perform the ping test:**
    ```md
    1. Open a Command Prompt window
       - Press the (Windows key + R) and type cmd,
       - Press Enter.

    2. Type: ping <server_address> -t
       - Press Enter
    ```
    **Server address:**
    ```diff
    + For [NA]  Klaipeda, type: s3.us-east-1.amazonaws.com
    + For [EU]  Fedimian, type: s3.eu-central-1.amazonaws.com
    + For [SEA] Telsiai,  type: s3.ap-southeast-1.amazonaws.com
    + For [SA]  Silute,   type: s3.sa-east-1.amazonaws.com

    - to stop, press: Ctrl+C on the CMD.
    ```
    **Alternative:**
    ```cpp
    #in-game ping (not reliable)
    type in chat: //ping
    ```
    """

INVITE = (
    "https://discordapp.com/api/oauth2/authorize"
    "?client_id=336363921466195968&scope=bot&permissions=0"
    )

PONG = """
     H
    　 O
    　　 O
    　　　 o
    　　 　　o
    　　　    o
    　　　　　o
    　　　　 。
    　　　 。
    　　　.
    　　　.
    　　　 .
    　　　　LY SHIT (╯°□°）╯︵ ┻━┻
    """

# Resources - guides

GUIDE = (
    "https://wizardguidetreeofsavior.blogspot.com"
    )

GUIDE_RITSU = (
    "http://kiyoshiro-ritsu.tumblr.com/"
    )

GUIDE_LEVELING = [
    (
        """click title for reddit post

        """
        "**Read :** FAQ for newbie and returning player!!\n"
        "**Command :** !rawr faq\n\n"

        "_- Navigate using the reaction emotes._\n"
        "_- Navigation buttons/reactions can only be used by individual who input the **!rawr lv** command._\n"
        "_- Guide start from page 2._\n"
        "_- Press_ \N{INFORMATION SOURCE} _if you're confused._\n"
        ),

    (
        """click title for reddit post

        """
        """***Lvl 1 ~ 50:***

        """
        "Start off by completing all the main(yellow/gold) quests from **East "
        "Siauliai Woods** all the way to **West Siauliai Woods**. You can "
        "then complete the main quest chains from **Miner's Village > Crystal "
        "Mines > Strautas Gorge > Gele Plateau > Nefritas Cliff > Tenet "
        "Garden**. Once you have enough silver to get Blessing and Sacrament "
        "buffs from pardoners in Klaipeda town (usually about 1600 silver is "
        "enough), you will want to get the buffs whenever you want to level. "
        "Make sure you refresh your buffs if they run out by purchasing them "
        "again in town. Once you arrive at **Tenet Garden**, you can kill the "
        "mobs above the goddess statue there; they are plentiful and have fast "
        "respawn times. You will also need to go inside **Tenet Church B1** "
        "and complete the entire main questline there until **Tenet Church "
        "2F** in order to acquire the **Seal of Space** quest item."
        ),

    (
        """click title for reddit post

        """
        """***Lvl 50 ~ 114:***

        """
        "Once you are lvl 50, you will be able to attempt the **lvl 50 "
        "dungeon in Klaipeda** town. Be sure to use your megaphones brought "
        "from the TP store using free daily tp to shout for people to queue up "
        "for it or join a guild so that it is easier to find parties. Go to "
        "**Feretory Hills** and kill the **Hallowventers** there along with "
        "other mobs. Be sure to complete the quests in **Feretory Hills**, "
        "**Mochia Forest**, and **Sutatis Trade Route** for some easy exp. "
        "You can continue to return to **Feretory Hills** and grind the mobs "
        "if you've already run out of dungeon runs for the day and have "
        "completed the previous quests. Once you get closer to lvl 90ish, "
        "you may also start to grind at **Sicarius 1F**."
        ),

    (
        """click title for reddit post

        """
        """***Lvl 114 ~ 202:***

        """
        "Make your way to **Aqueduct Bridge Area** and start the main quest "
        "chain there. It will bring you into the **Demon Prison** maps in "
        "which you can follow the entire quest chain until **Demon Prison "
        "District 5**. Once you have done so, you may choose to return to "
        "**Demon Prison District 2** and kill the mobs there. They are "
        "plentiful and respawn quickly. You will be able to grind here for "
        "quite a while due to the sheer number of mobs and the fast respawn "
        "rate. you will also want to try the Challenge Mode feature (lvl 100+) "
        "around maps of your level. An alternate path is to go to **Dina Bee "
        "Farm** and kill the bees in the **Akasya Field** and **Rododun "
        "Apiary** areas when you are around lvl 140+. (You can also do the "
        "quests in this map too!)"
        ),

    (
        """click title for reddit post

        """
        """***Lvl 202 ~ 230:***

        """
        "Make your way to **Alemeth Forest** and complete the quests there. "
        "Continue on and complete the quests in **Barha Forest**, **Nahash "
        "Forest**, **Cranto Coast**, and **Igti Coast**. **Cranto Coast** is "
        "also an excellent map to do Challenge modes in; be sure to attempt "
        "challenge modes in a party from now on. (You can get party members "
        "from shouting a party link via megaphone.) If you still need a bit "
        "more exp to reach 230 then consider visiting **Neighport Church East "
        "Building**. It is a great place to grind once your daily challenge "
        "modes and previous quests are done."
        ),

    (
        """click title for reddit post

        """
        """***Lvl 230 ~ 270:***

        """
        "Go to **Kalejimas Visiting Room** and start to complete the main "
        "quests in that area. You can actually follow the entire quest route "
        "from **Kalejimas Visiting Room > Storage > Solitary Cells > Workshop "
        "> Investigation Room** killing all the monsters you encounter on the "
        "way. Remember to keep up with your daily dungeon runs of appropriate "
        "level and Challenge mode entries. If you still require additional "
        "exp to reach lvl 270 you can consider returning to **Workshop** and "
        "grinding the monsters there, it features a relatively small map along "
        "with a decent amount of monster spawns."
        ),

    (
        """click title for reddit post

        """
        """***Lvl 270 ~ 315:***

        """
        "Keep up with Daily dungeons around your level and make your way to "
        "**Timerys Temple.** This will be your new home for grinding and "
        "Challenge modes until lvl 315. Make sure to use up to date equipment "
        "for your level because the mobs will start to hurt a lot. **Timerys "
        "Temple** also happens to be a great map for gem farming and silver "
        "farming. An alternative path to this would be to go to **Inner Wall "
        "District 8** and complete the main quests there. You can continue to "
        "follow the questchain around **City Wall 8**, **Jeromel Commemorative "
        "Park**, and **Jonael Commemoratie Orb**. If you feel like you require "
        "some addition exp, you can consider returning to **Jeromel "
        "Commemorative Park** to grind the plentiful mobs there."
        ),

    (
        """click title for reddit post

        """
        """***Lvl 315 ~ 357:***

        """
        "You can now start to level at **Sausys Room 9,** this is a great "
        "place to grind and do your daily challenge modes for silver, loot "
        "and exp. Remember to keep up to date with your equipment and work "
        "towards better equips. Complete all the quests from **Sausys Room 9** "
        "all the way to **Valandis Room 91**. When you are around lvl 340ish "
        "and you are getting bored of grinding at **Sausys Room 9,** you can "
        "go to **Narvas Temple** for a change of scenery and do the Challenge "
        "modes, quests and grind there."
        ),

    (
        """click title for reddit post

        """
        """***Lvl 357 ~ 390:***

        """
        "You will want to complete most of the higher level quests in this "
        "bracket range for their great exp amounts. Start from "
        "**Lanko 26 Waters** and complete all the quests from there until "
        "**Barynwell 87 Waters**, then head into **Astral Tower 1F**. "
        "**Astral Tower 1F** happens to be a great place for challenge modes "
        "with its narrow corridors forcing mobs to spawn in close proximity "
        "running towards you. Complete all the quests within "
        "**Astral Tower 1F** until **Astral tower 21F** then make your way to "
        "**Starry Town.** You will want to follow the quest chain here and "
        "complete all the quests in **Starry Town, Feline Post Town** and "
        "finally **Spell Tome Town**. **Spell Tome Town** is also an excellent "
        "place to do challenge modes due to specific narrow areas and high "
        "level monsters. Remember to keep up with your dungeon runs of "
        "appropriate levels. If you still require additional exp, you may "
        "choose to grind around any of the higher level maps in this bracket "
        "range or spam challenge mode runs with reset vouchers from events "
        "and from purchasing them off other players in the market. (The profit "
        "from a single CM run is usually greater than the cost of purchasing a "
        "reset voucher.)"
        ),

    ]

# Resources - addon managers

ADDON_MIZUKIBELHI = (
    "https://github.com/MizukiBelhi/Tree-of-Savior-Addon-Manager/releases"
    )

ADDON_JTOS = (
    "https://github.com/JToSAddon/Tree-of-Savior-Addon-Manager/releases/latest"
    )

# Resources - documents

G_DOC = "https://docs.google.com/document/d"

DOC_BUILD = (
    f"{G_DOC}/1SF3CeTi9umcI9tFmZmRCNUHEJQwtgSMmVKqq9sCjnPY/edit?usp=sharing"
    )

DOC_GIMMICKS = (
    f"{G_DOC}/1ihOzgxe8SrV8aRwYq1xMUwiTvsTNHGibJ6yBXFATaTg/edit?usp=sharing"
    )

DOC_UNLOCK = (
    f"{G_DOC}/1aEOF-WjTiKr1WE-bYHNIyl0_JnVX8_rUzCoclFDVQrY/edit?usp=sharing"
    )

# Resources - miscellaneous posts

POST_PATCH = """
    **[Ktest/Ktos - Patch Notes Translation]**
    _(no longer maintained)_
    **Greyhiem's**  https://pastebin.com/u/Greyhiem
    **Gwenyth's**  https://pastebin.com/u/sunhwapark
    """

POST_LORE = (
    "http://toshidden.blog.fc2.com/"
    )

NEW_OR_RETURN = (
    "https://www.reddit.com/r/treeofsavior/comments/af1evf"
    "/read_first_NEW_OR_RETURNing_players_version_20/"
    )

# Resources - latest news message for Rawr

LATEST = (
    "**[The Re:Build Survival Guide, DevBlog & FAQ!!]**\n"
    "https://treeofsavior.com/news/?n=1584\n"
    "https://treeofsavior.com/page/news/view.php?n=1534"
    )

# Resources - skill planners

PLANNER_TOSG = (
    "https://tos.neet.tv/skill-planner"
    )

PLANNER_TOSCAMP = (
    "http://toscamp.com/tos/ranksimul/"
    )

CLASS_RANKING = (
    "https://treeofsavior.com/page/class/ranking.php"
    )


class CommandsCog(commands.Cog):
    """Rawr's commands."""

    def __init__(self, bot):
        self.bot = bot

    ###-- help --###
    @commands.command(aliases=['halp'])
    async def help(self, ctx):
        await ctx.author.send(cleandoc(HELP))

    ###-- hello --###
    @commands.command()
    async def hello(self, ctx):
        await ctx.send(cleandoc(HELLO))

    ###-- who --###
    @commands.command()
    async def who(self, ctx):
        await ctx.send("Full-fledged Hero!!")

    ###-- ping --###
    @commands.command()
    async def ping(self, ctx):
        await ctx.send(cleandoc(PING))

    ###-- pong --###
    @commands.command()
    async def pong(self, ctx):
        await ctx.send(cleandoc(PONG))

    ###-- ktest --###
    @commands.command()
    async def ktest(self, ctx):
        await ctx.send(
            cleandoc(
                f"""
                **[Let's see the future!!]**
                https://tos-ktest.neet.tv/"
                """
                )
            )

    ###-- build --###
    @commands.command(aliases = ['builds'])
    async def build(self, ctx):
        await ctx.send(
            cleandoc(
                f"""
                **[Compilation of Practical Class Build Guide!!]**
                _- builds made by reddit community & compiled by Palemoon_
                {DOC_BUILD}
                """
                )
            )

    ###-- update --###
    @commands.command(aliases = ['updates', 'change', 'changes'])
    async def update(self, ctx):
        await ctx.send(
            cleandoc(
                f"""
                **[Check what is new!!]**
                https://tos.neet.tv/changes
                """
                )
            )

    ###-- addon manager --###
    @commands.command()
    async def addon(self, ctx):
        await ctx.send(
            cleandoc(
                f"""
                **[Grab your Tree of Savior addons manager!!]**
                _- by MizukiBelhi_
                {ADDON_MIZUKIBELHI}

                {ADDON_JTOS}
                """
                )
            )

    ###-- faq --###
    @commands.command(aliases = ['faq', 'return'])
    async def newbie(self, ctx):
        await ctx.send(
            cleandoc(
                f"""
                **[FAQ for newbie and returning player!!]**
                _- by Palemoon_
                {NEW_OR_RETURN}

                {LATEST}
                """
                )
            )

    ###-- holy guides --###
    @commands.command()
    async def guide(self, ctx):
        await ctx.send(
            cleandoc(
                f"""
                **[Guide blog based on kTOS/kTEST!!]**
                {GUIDE}

                **[Various class overview by Ritsu!!]**
                {GUIDE_RITSU}
                """
                )
            )

    ###-- unlock guide --###
    @commands.command(aliases = ['hidden'])
    async def unlock(self, ctx):
        await ctx.send(
            cleandoc(
                f"""
                **[Hidden class unlock guides!!]**
                _- by Palemoon_
                {DOC_UNLOCK}

                **[Tree of Savior Hidden Secrets & Lore!!]**
                _- by Ximi_
                {POST_LORE}
                """
                )
            )

    ###-- planner --###
    @commands.command()
    async def planner(self, ctx):
        await ctx.send(
            cleandoc(
                f"""
                **[Plan your character build!!]**
                {PLANNER_TOSG}

                {PLANNER_TOSCAMP}
                """
                )
            )
        # tos-th.com is no longer available.

    ###-- gimmick --###
    @commands.command(aliases = ['exploration', 'gimmick'])
    async def explo(self, ctx):
         await ctx.send(
            cleandoc(
                f"""
                **[Explorer Gimmicks & New Collections Guide]**
                *[credits : TerminalEssence & Friends]*

                {DOC_GIMMICKS}
                """
                )
            )

    ###-- timezone --###
    @commands.command()
    async def time(self, ctx):
        fmt = "%H:%M:%S %Y-%m-%d"

        utc = timezone('UTC')
        est = timezone('EST')
        brst = timezone('America/Noronha')
        cet = timezone('CET')
        sgt = timezone('Asia/Singapore')

        now = datetime.datetime.now(tz = utc)

        # Current time in UTC
        await ctx.send(
            cleandoc(
                f"""
                ```cs
                UTC : {now.strftime(fmt)}
                EST : {now.astimezone(est).strftime(fmt)}
                BRST: {now.astimezone(brst).strftime(fmt)}
                CET : {now.astimezone(cet).strftime(fmt)}
                SGT : {now.astimezone(sgt).strftime(fmt)}
                ```
                """
                )
            )

        # Convert to Asia/Singapore time zone
        #now_sgt = now_utc.astimezone(timezone('Asia/Singapore'))
        #await ctx.send (now_sgt.strftime(fmt) + " (SGT)")


    ###-- leveling --###
    @commands.command(aliases = ['leveling', 'lvl', 'level'])
    async def lv(self, ctx):
        pages = Pages(
            bot,
            message = ctx.message,
            entries = GUIDE_LEVELING,
            per_page = 1,
            with_number = False
            )
        await pages.paginate()

    ###-- invite --###
    @commands.command(aliases = ['invite'])
    async def inv(self, ctx):
        await ctx.send(
            cleandoc(
                f"""
                **[Use this link to invite me to your server.]**

                {INVITE}"
                """
                )
            )

    ###-- ranking --###
    @commands.command(aliases = ['rankings'])
    async def rank(self, ctx):
        await ctx.send(
            cleandoc(
                f"""
                **[The most popular TOS class builds of all time]**
                *[Updated periodically]*

                {CLASS_RANKING}
                """
                )
            )

    ###-- patch notes translation --###
    @commands.command()
    async def pnt(self, ctx):
        await ctx.send(cleandoc(POST_PATCH))


def setup(bot):
    bot.add_cog(CommandsCog(bot))
