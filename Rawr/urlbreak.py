import asyncio
import datetime

import discord
from bs4 import BeautifulSoup


TOS_THUMBNAIL = (
    "http://bestonlinegamesreview.com/wp-content/uploads/2016/04"
    "/p1_2006411_5eae6fd9.png"
    )


async def format_embed_description(records: dict, format_str: str):
    """Formats an embed description to use.

    Args:
        records (dict): records to convert to description
        format_str (str, optional): the format string to use;
            do not pass a F-String!

    Returns:
        str: the formatted description

    """
    return (
        '```'
        '\n'.join(
            [
                format_str.format(*record)
                for record
                in records.items()
                ]
            )
        '```'
        )


async def find_tables_after_header(soup, h2_text):
    h2 = soup.find('h2', text = h2_text)

    if h2 is not None:
        els = h2.find_next_siblings()
        tables = []

        for el in els:
            if el.name == 'table':
                tables.append(el)
            else:
                break
        return tables
    else:
        return None


##--------- Item Info ---------##
async def get_item(link):
    async with aiohttp.ClientSession() as cs:
        async with cs.get(link) as r:
            soup = BeautifulSoup(await r.text(), 'html.parser')

    tables = soup.find_all('table')
    item_type = soup.find(
        'table',
        {'class': 'pure-table'}
        ).find('td').get_text()

    #-- description --#
    description = 'No Description'
    if soup.find(class_ = 'item-desc'):
        description = soup.find(class_ = 'item-desc').get_text()

    embed = discord.Embed(
        colour = discord.Colour(0xF16F9B),
        description = description,
        timestamp = datetime.datetime.now()
        )

    #-- title --#
    title = soup.find(id = 'title').get_text()
    embed.set_author(
        name = title,
        url = link,
        icon_url = TOS_THUMBNAIL
        )

    #-- thumbnail --#
    visualheader = soup.find('h2', text = 'Visual')
    if visualheader is not None:
        table = visualheader.find_next_sibling('img').get('src')
        thumbnail = f'https://tos.neet.tv{table}'
        embed.set_thumbnail(url = thumbnail)

    #-- gem info --#
    if item_type == 'Gems':
        info_table = soup.find('table', {'class', 'list-table'})
        info = []

        for row in info_table.find_all('tr'):
            name = row.find('th').get_text()
            value = row.find('td').get_text()

            info.append(f'{name:<7}: {value}')

        embed.add_field(
            name = "Info",
            value = (
                '```'
                '\n'.join(info)
                '```'
                ),
            inline = True
            )

    #-- grade --#
    if tables[0].find('span') is not None:
        name = 'Grade'
        grade = tables[0].find('span')['data-tip']

        if item_type == 'Card':
            name = 'Card Group'

        embed.add_field(
            name = name,
            value = grade,
            inline = False
            )

    #-- requirements --#
    req_tables = await find_tables_after_header(soup, 'Requirements')
    if req_tables is not None:
        requirements = req_tables[0].find('td').get_text()
        embed.add_field(
            name = "Requirement",
            value = requirements,
            inline = False
            )

    #-- stats --#
    stats_tables = await find_tables_after_header(soup, 'Stats\n')
    if stats_tables is not None:
        stats = {}

        names = stats_tables[0].find_all('th')
        values = stats_tables[0].find_all('td')

        for name, value in zip(names, values):
            stats[name.get_text()] = value.get_text()

        embed.add_field(
            name = "Stats",
            value = await format_embed_description(stats, "{:<20}: {}"),
            inline = True
            )

        #-- stats (additional & bonus) --#
        if len(stats_tables) > 1:
            additional = {}
            bonus = []

            names = stats_tables[1].find_all('th')
            values = stats_tables[1].find_all('td')

            ##----- addditional & bonus stats -----##
            for name, value in zip(names, values):
                if name.get_text() != ' - ':
                    additional[name.get_text()] = value.get_text()
                else:
                    bonus.append(value.get_text())

            if additional:
                embed.add_field(
                    name = "Additional Stats",
                    value = await format_embed_description(
                        additional, "{:<27}: {}"
                        ),
                    inline = False
                    )

            if bonus:
                embed.add_field(
                    name = "Bonus Stats",
                    value = (
                        '```'
                        '\n'.join(bonus)
                        '```'
                        ),
                    inline = False
                    )

    #-- stats (set bonus) --#
    set_tables = await find_tables_after_header(soup, 'Set')
    if set_tables is not None:
        set_bonus = {}
        rows = set_tables[0].find_all('tr')

        for row in rows[2:]:
            name = row.find('th').get_text()
            values = row.find('td').find_all('li')
            values = [value.get_text().strip() for value in values]

            value =', '.join(values)
            set_bonus[name] = value

        if set_bonus:
            embed.add_field(
                name = "Set Bonus",
                value = await format_embed_description(set_bonus, "{}: {}")
                inline = True
                )

    #-- produces --#
    produces_tables = await find_tables_after_header(soup, 'Produces')
    if produces_tables:
        embed.add_field(
            name = "Produces",
            value = produces_tables[0].find('a').get_text(),
            inline = False
            )

    # -- references --#
    ref_tables = await find_tables_after_header(soup, 'References')
    if ref_tables is not None:
        ref = {}

        names = ref_tables[0].find_all('th')
        values = ref_tables[0].find_all('td')

        for name, value in zip(names, values):
            ref[name.get_text()] = value.get_text().replace('\n ', '\n')

        embed.add_field(
            name = "References",
            value = await format_embed_description(ref, "{}: {}"),
            inline = True
            )


    #----- material -----#
    mats_tables = await find_tables_after_header(soup, 'Materials')
    if mats_tables is not None:
        rows = mats_tables[0].find_all('tr')
        materials = {}

        for row in rows:
            name = row.find('a').get_text()
            value = row.find_all('td')[2].get_text()

            materials[name] = value

        if materials:
            embed.add_field(
                name = "Materials",
                value = await format_embed_description(materials, '{:<20}: {}'),
                inline = False
                )

    return embed


##--------- Skill Info ---------##
async def skill_info(link):
    async with aiohttp.ClientSession() as cs:
        async with cs.get(link) as r:
            soup = BeautifulSoup(await r.text(), 'html.parser')
    tables = soup.find_all('table')

    data = {
        'info': {},
        'addsinfo': {},
        'skillfact': {},
        'attribs': [],
        'adin': {}
        }

    data['title'] = soup.find(id = 'title').get_text()
    data['description'] = soup.find(class_ = 'item-desc').get_text()
    data['requirement'] = f"stance :{tables[2].find('td').get_text()}"
    data['efx'] = soup.find(id = 'js-skill-effect').get_text()

    ##----- info -----##
    rows = tables[0].find_all('tr')

    names = rows[0].find_all('th')[5:]
    values = rows[1].find_all('td')[5:]

    for name, value in zip(names, values):
        data['info'][name.get_text()] = value.get_text()

    ##----- additional info / adin -----##
    names = tables[1].find_all('th')
    values = tables[1].find_all('td')

    for name, value in zip(names, values):
        if not value.find(class_ = 'cat-toggle'):
            data['addsinfo'][(name.get_text())] = value.get_text()

    data['adin'] = dict(
        list(data['info'].items()) + list(data['addsinfo'].items())
        )

    ##----- skill factor -----##
    sfact = soup.find(id = 'js-skill-funcs')

    names = sfact.find_all('th')
    values = sfact.find_all('td')

    for name, value in zip(names, values):
        data['skillfact'][(name.get_text())] = value.get_text()

    ##----- attributes -----##
    attribHeader = soup.find('h2', text = 'Attributes')
    if attribHeader:
        table = attribHeader.find_next_sibling('table')
        rows = table.find_all('tr')

        for row in rows:
            names = row.find('a').get_text()
            values = row.find(class_ = 'item-desc').get_text()
            mod = '\n'.join(
                (f'* {tooltip.get_text()}')
                for tooltip
                in row.find_all('span', {'data-tip': True})
                )

            data['attribs'].append(
                {
                    'name': names,
                    'value': values,
                    'mod': mod
                    }
                )
    ## ----- ##

    ##----- thumbnail -----##
    visualheader = soup.find('h2', text = 'Visual')
    if visualheader:
        table = visualheader.find_next_sibling('img').get('src')
        data['thumbnail'] = f'https://tos.neet.tv{table}'

    return data