import json
import os
import pandas as pd
import re
from io import StringIO

CLEANR = re.compile('<.*?>')

directory = 'marvelsdb-json-data\pack'

def strip_packs(headers):
    dataset = []

    for filename in os.listdir(directory):
        f = open(os.path.join(directory, filename))
        data = json.load(f)
        for i in data:
            row = []
            for index in range(0, len(headers)):
                name = headers[index]
                if name == 'text' or name == 'attack_text' or name == 'scheme_text':
                    try:
                        row.append(re.sub(CLEANR, '', i[name]))
                    except:
                        row.append(None)
                else:
                    try: 
                        row.append(i[name])
                    except:
                        row.append(None)
            dataset.append(row)
    
    return dataset


def get_json_headers(key_data):

    df_keys = pd.DataFrame(key_data)
    df_keys.columns = ['code','keys','key_count']
    max_len = df_keys[['key_count']].sort_values(by='key_count', ascending=False).max()
    df_headers = df_keys[df_keys['key_count'] >= int(max_len.iloc[0])].iloc[0]['keys']

    df_keys = df_keys['keys']
    for i in range(0,df_keys.shape[0]):
        vals = df_keys.iloc[i]
        for j in range(len(vals)):
            if vals[j] in df_headers:
                pass
            else:
                df_headers.append(vals[j])

    return df_headers


def get_key_data():
    key_data = []

    for filename in os.listdir(directory):
        f = open(os.path.join(directory, filename))
        data = json.load(f)
        for i in data:
            key_row = (i['code'], list(i.keys()), len(list(i.keys())))
            key_data.append(key_row)
    return key_data


def write_to_json():
    key_data = get_key_data()
    headers = get_json_headers(key_data)
    dataset  = strip_packs(headers)

    df = pd.DataFrame(dataset)
    df.columns = headers
    df.to_json('cards.json', orient='records')
    return print(df)


def write_to_parquet():
    f = open('cards.json')
    df2 = pd.read_json(f, orient='records')
    df2.to_parquet('cards.parquet')
    return print(df2)


def main():
    write_to_json()
    write_to_parquet()
    return print('done!')


if __name__=='__main__':
    main()

#print(df_keys)
    

