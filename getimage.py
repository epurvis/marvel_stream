import requests as r
import pandas as pd
import json

url = 'https://marvelcdb.com/api/public/cards/'

cards_json = r.get(url=url).text
cards_dict = json.loads(cards_json)

dataset = []

f = open('cards.json')
cards_dict1 = json.load(f)

for i in range(len(cards_dict1)):
    for j in range(len(cards_dict)):
        if cards_dict[j]['code'] == cards_dict1[i]['code']:
            try:
                image_url = 'https://marvelcdb.com{0}'.format(cards_dict[j]['imagesrc'])
            except:
                image_url = None
            vals = list(cards_dict1[i].values())
            vals.append(image_url)
            dataset.append(vals)
        else:
            pass

headers = list(cards_dict1[0].keys())
headers.append('image_url')

df = pd.DataFrame(dataset)
df.columns = headers

df.to_json('cards_img_fix.json', orient='records')

df2 = pd.read_json('cards_img_fix.json', orient='records')
df2.to_parquet('cards_img_fix.parquet')


    