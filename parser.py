import json
import requests

print('1 - heroes, 2 - items, 3 - abilities')

HEROES_ITEMS_ABILITIES = {'1': 'heroes',
                          '2': 'items',
                          '3': 'abilities'}

TYPE_IMG = {'1': 'full',
            '2': 'lg',
            '3': 'sb'}

json_name = ''


def open_json():
    while True:
        s = input('Select which images you want to download: ')
        global json_name
        json_name = HEROES_ITEMS_ABILITIES.get(s)
        try:
            my_json = open(f'{json_name}.json')
            return my_json
        except FileNotFoundError:
            print('You selected a parameter that does not exist.')


def check_type_img(i=None):
    if i == 'heroes':
        print('1 - full, 2 - lg, 3 - sb, 4 - icons')
        TYPE_IMG.update({'4': 'icon'})
    else:
        print('1 - full, 2 - lg, 3 - sb')
    while True:
        img_type = input('Select image size: ')
        try:
            img_type = TYPE_IMG[img_type]
            return img_type
        except KeyError:
            print('You selected a parameter that does not exist.')


try:
    json_file = open_json()
    data = json.load(json_file)

    if json_name == 'heroes':
        type_img = check_type_img(json_name)
        if type_img == 'icon':
            path = 'icons'
        else:
            path = 'images'
        for hero in data:
            img = f"http://cdn.dota2.com/apps/dota2/images/heroes/{hero.replace('npc_dota_hero_', '')}_{type_img}.png"
            p = requests.get(img)
            out = open(f"{path}/heroes/{hero}.png", "wb")
            out.write(p.content)
            out.close()

    elif json_name == 'items':
        type_img = check_type_img()
        for id, name in data.items():
            img = f"http://cdn.dota2.com/apps/dota2/images/items/{name}_{type_img}.png"
            p = requests.get(img)
            out = open(f"images/items/{name}.png", "wb")
            out.write(p.content)
            out.close()

    else:
        type_img = check_type_img()
        for _, value in data.items():
            for name in value['abilities']:
                img = f"http://cdn.dota2.com/apps/dota2/images/abilities/{name}_{type_img}.png"
                p = requests.get(img)
                out = open(f"images/abilities/{name}.png", "wb")
                out.write(p.content)
                out.close()
    json_file.close()

except KeyboardInterrupt:
    print('\nThe program was stopped prematurely.')
