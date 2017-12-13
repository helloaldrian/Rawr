import bs4, sys
from bs4 import BeautifulSoup
import urllib.request
import pprint
import discord
import datetime


def find_tables_after_header(soup, h2_text):
    h2 = soup.find('h2', text=h2_text)

    if h2 is not None:
        els = h2.find_next_siblings()
        tables = None

        for el in els:
            if el.name == 'table':
                if tables == None:
                    tables = []
                tables.append(el)
            else:
                break
        return tables
    else:
        return None
    

##--------- Item Info ---------##
def get_item(item_links):

    r = urllib.request.urlopen(item_links).read()
    soup = BeautifulSoup(r, 'html.parser')
    tables = soup.find_all('table')
    item_type = soup.find('table', {'class': 'pure-table'}).find('td')

    if item_type is not None:
        item_type = item_type.get_text()
    else:
        item_type = ''
        

    #-- description --#
    description = 'No Description'
    if soup.find(class_='item-desc') != None:
        description = soup.find(class_='item-desc').get_text()
    
    embed = discord.Embed(colour=discord.Colour(0xF16F9B), description=description, timestamp=datetime.datetime.now())


    #-- title --#
    title = soup.find(id='title').get_text()
    embed.set_author(name=title, url=item_links, icon_url="http://bestonlinegamesreview.com/wp-content/uploads/2016/04/p1_2006411_5eae6fd9.png")


    #-- thumbnail --#
    visualheader = soup.find('h2', text='Visual')
    if visualheader is not None:
        table = visualheader.find_next_sibling('img').get('src')
        thumbnail = 'https://tos.neet.tv' + table
        embed.set_thumbnail(url=thumbnail)


    #-- gem info --#
    if item_type == 'Gems':
        info_table = soup.find('table', {'class', 'list-table'})
        infos = []

        for row in info_table.find_all('tr'):
            name = row.find('th').get_text()
            value = row.find('td').get_text()

            infos.append('{:<7}: {}'.format(name, value))

        embed.add_field(name="Info", value='```' + '\n'.join(infos) + '```', inline=True)


    #-- grade --#
    if tables[0].find('span') is not None:
        name = 'Grade'
        grade = tables[0].find('span')['data-tip']

        if item_type == 'Card':
            name = 'Card Group'

        embed.add_field(name=name, value=grade, inline=False)


    #-- requirements --#
    req_tables = find_tables_after_header(soup, 'Requirements')
    if req_tables is not None:
        requirements = req_tables[0].find('td').get_text()
        embed.add_field(name="Requirement", value=requirements, inline=False)


    #-- stats --#
    stats_tables = find_tables_after_header(soup, 'Stats')
    if stats_tables is not None:
        stats = {}

        names = stats_tables[0].find_all('th')
        values = stats_tables[0].find_all('td')

        for name, value in zip(names, values):
            stats[name.get_text()] = value.get_text()

        stats = '```' + '\n'.join(["{:<20}: {}".format(*item) for item in stats.items()]) + '```'
        embed.add_field(name="Stats", value=stats, inline=True)


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

            if additional != {}:
                addsts = '```' + '\n'.join(["{:<27}: {}".format(*item) for item in additional.items()]) + '```'
                embed.add_field(name="Additional Stats", value=addsts, inline=False)

            if len(bonus) != 0:
                embed.add_field(name="Bonus Stats", value='```' + '\n'.join(bonus) + '```', inline=False)


    #-- stats (set bonus) --#
    set_tables = find_tables_after_header(soup, 'Set')
    if set_tables is not None:
        setbonus = {}
        rows = set_tables[0].find_all('tr')
        
        for row in rows[2:]:
            name = row.find('th').get_text()
            values = row.find('td').find_all('li')
            values = [value.get_text().strip() for value in values]

            value =', '.join(values)
            setbonus[name] = value

        if setbonus != {}:
            setbns = '\n'.join(["{}: {}".format(*item) for item in setbonus.items()])
            embed.add_field(name="Set Bonus", value='```' + setbns + '```', inline=True)


    #-- produces --#
    produces_tables = find_tables_after_header(soup, 'Produces')
    if produces_tables is not None:
        name = produces_tables[0].find('a').get_text()
        produces = name
        embed.add_field(name="Produces", value=produces, inline=False)


    # -- references --#
    ref_tables = find_tables_after_header(soup, 'References')
    if ref_tables is not None:
        ref = {}

        names = ref_tables[0].find_all('th')
        values = ref_tables[0].find_all('td')

        for name, value in zip(names, values):
            ref[name.get_text()] = value.get_text().replace('\n ', '\n')

        refs = '```' + '\n'.join(["{}: {}".format(*item) for item in ref.items()]) + '```'
        embed.add_field(name="References", value=refs, inline=True)


    #----- material -----#
    mats_tables = find_tables_after_header(soup, 'Materials')
    if mats_tables is not None:
        rows = mats_tables[0].find_all('tr')
        materials = {}

        for row in rows:   
            name = row.find('a').get_text()
            value = row.find_all('td')[2].get_text()   

            materials[name] = value

        if len(materials) != 0:
            mats = '```' + '\n'.join(['{:<20}: {}'.format(name, value) for name, value in materials.items()]) + '```'
            embed.add_field(name="Materials", value=mats, inline=False)

    return embed
    

##--------- Skill Info ---------##
def skill_info(skill_id):

    r = urllib.request.urlopen(skill_id).read()
    soup = BeautifulSoup(r, 'html.parser')
    tables = soup.find_all('table')

    data = {'info': {}, 'addsinfo': {}, 'skillfact': {}, 'attribs': [], 'adin': {}}

    data['title'] = soup.find(id='title').get_text()
    data['description'] = soup.find(class_='item-desc').get_text()
    data['requirement'] = "stance :" + tables[2].find('td').get_text()
    data['efx'] = soup.find(id='js-skill-effect').get_text()

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
       data['addsinfo'][(name.get_text())] = value.get_text()

    data['adin'] = dict(list(data['info'].items()) + list(data['addsinfo'].items()))

    ##----- skill factor -----##
    sfact = soup.find(id='js-skill-funcs')

    names = sfact.find_all('th')
    values = sfact.find_all('td')

    for name, value in zip(names, values):
        data['skillfact'][(name.get_text())] = value.get_text()

    ##----- attributes -----##
    attribHeader = soup.find('h2', text='Attributes')
    if attribHeader is not None:
        table = attribHeader.find_next_sibling('table')
        rows = table.find_all('tr')
        
        for row in rows:   
            names = row.find('a').get_text()
            values = row.find(class_='cell-500 item-desc').get_text()
            mod = row.find(class_='cell-center').get_text()
           
            data['attribs'].append({'name': names, 'value': values, 'mod': mod})
    ## ----- ##

    ##----- thumbnail -----##
    visualheader = soup.find('h2', text='Visual')
    if visualheader is not None:
        table = visualheader.find_next_sibling('img').get('src')
        data['thumbnail'] = 'https://tos.neet.tv' + table

    return data