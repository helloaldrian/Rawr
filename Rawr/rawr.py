import html
import os
import sys

import discord
from discord.ext import commands

from urlbreak import get_item, skill_info
from paginator import Pages


bot = commands.Bot(
    command_prefix = '!rawr ',
    description = 'just another silly tree of savior bot',
    dm_help = True
    )

bot.remove_command("help")

initial_extensions = [
    'cogs.commands',
    'cogs.guildonly',
    ]

if __name__ == '__main__':
    for extension in initial_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            print(
                f'Failed to load extension {extension}: {e}',
                file = sys.stderr
                )


# Rawr-specific

VERSION = '0.4.11'
CHANGELOG = """
```md
[Changelog](version: 0.4.11)
```
```md
# Added:
* Reformated time in `!rawr time`

* Contact @Jiyuu#6312
```
"""

WELCOME = """
_`Hello there!`_

Nice to meet you, I am Rawr!!
I'm a simple Tree of Savior Discord bot that can help you and your community find and gather information regarding ToS.

Here, I am request permission to stay in your server.
- Rawr
"""

SPAWN = """
```css
"When you meet someone for the first time, that's not the whole book. That's just the first page."
```
:ghost: Hello Hooman! I'm **Rawr!**

I am a simple bot that aims to help Tree of Savior players find information related to ToS.
Use `!rawr help` to find out more commands.
Alright Boys, Rawr at your service!! :sunglasses:
================================================================
"""


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

    await bot.change_presence(
        activity = discord.Game(
            name = "Tree of Savior 2.0 - Re:Build",
            ),
        status = discord.Status.online,
        )

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
async def on_guild_join(guild):
    ##-- send msg to the server owner --##
    await guild.owner.send(WELCOME)

    ##-- send msg to the 1st text channel on the server --##
    for channel in guild.channels:
        if channel.type == discord.ChannelType.text:
            try:
                await channel.send(SPAWN)
                return
            except discord.errors.Forbidden:
                continue

if __name__ == '__main__':
    bot.run(os.environ['BOT_TOKEN'])
