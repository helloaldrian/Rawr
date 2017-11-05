import bs4, sys
from bs4 import BeautifulSoup
import urllib.request
import pprint


##--------- Item Info ---------##
def get_item(item_links):

    r = urllib.request.urlopen(item_links).read()
    soup = BeautifulSoup(r, 'html.parser')
    tables = soup.find_all('table')

    data = {'stats': {}, 'additional': {}, 'bonus': [], 'setbonus': {}}

    data['title'] = soup.find(id='title').get_text()
    data['description'] = soup.find(class_='item-desc').get_text()
    data['thumbnail'] = 'https://tos.neet.tv' + soup.find('img').get('src')
    data['min_level'] = tables[2].find('td').get_text()
    data['grade'] = tables[0].find('span')['data-tip']

    ##----- stats -----##
    names = tables[3].find_all('th')
    values = tables[3].find_all('td')

    for name, value in zip(names, values):
        data['stats'][name.get_text()] = value.get_text()

    names = tables[4].find_all('th')
    values = tables[4].find_all('td')

    ##----- addditional & bonus stats -----##
    for name, value in zip(names, values):
        if name.get_text() != ' - ':
           data['additional'][name.get_text()] = value.get_text()
        else:
            data['bonus'].append(value.get_text())

    rows = tables[6].find_all('tr')
    
    ##----- set bonus stats -----##
    for row in rows[2:]:
        name = row.find('th').get_text()
        values = row.find('td').find_all('li')
        values = [value.get_text().strip() for value in values]

        value =', '.join(values)
        data['setbonus'][name] = value

    return data


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

    ##----- alternate for info -----##
    # names = tables[0].find_all('th')
    # values = tables[0].find_all('td')

    # for name, value in zip(names[5:], values[5:]):
    #     data['info'][name.get_text()] = value.get_text()
    ## ----- ##

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