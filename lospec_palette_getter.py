from random import randint
import requests
import json
from bs4 import BeautifulSoup
import os

json_data = []
palettes=[]

#Check if you already have lospec palettes downloaded
#To create or update your palette run get_lospect_data() and to_json_file

if os.path.exists("lospec_palettes.json"):
    with open("lospec_palettes.json") as file:
        palettes = json.load(file)
        print("lospec_palettes.json loaded in palettes")

def get_lospec_data():
    with requests.Session() as s:
        print('requesting page...')
        url='https://lospec.com/palette-list/load?colorNumberFilterType=any&colorNumber=8&page=0&tag=&sortingType=default'
        r = s.get(url)
    rj = r.json()
    json_data.append(rj)

    print('downloading...')

    i = 1
    while rj['palettes']:
        r = s.get(f'https://lospec.com/palette-list/load?colorNumberFilterType=any&colorNumber=8&page={i}&tag=&sortingType=default')
        rj = r.json()
        json_data.append(rj)
        i+=1
        print(f'page {i} complete')


    for json_page in json_data:
        for j in json_page['palettes']:
            palettes.append({
            'name': j['title'],
            'author': j.get('user', {}).get('name', 'None'),
            'colors': j['colorsArray']
        })

    
#Get a random palette
def random_palette():
    i = randint(0, len(palettes))
    return palettes[i]

#Get a palette by it's title (obtained by browsing lospec.com/palettes)
def get_palette(name):
    for p in palettes:
        if p['name'].lower()==name.lower():
            return p

#write to file for use in anything or as a cache for this program
def to_json_file():
    j = json.dumps(palettes, indent=4)

    with open('lospec_palettes.json', 'w') as outfile:
        outfile.write(j)
    