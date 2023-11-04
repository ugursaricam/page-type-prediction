import requests
from bs4 import BeautifulSoup
import pandas as pd
from URLs import URL_list
import random
import time

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)
pd.set_option('display.expand_frame_repr', False)
pd.set_option('display.float_format', lambda x: '%.2f' % x)

def scraper(link):
    url = link
    headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36'}
    response = requests.get(url, headers=headers)

    soup = BeautifulSoup(response.content, 'html.parser')

    title = soup.title.string.strip().lower() if soup.title else ""

    meta_description = soup.find("meta", {"name": "description"})
    meta_description_content = meta_description["content"].strip().lower() if meta_description else ""
    store = [1 if "mağaza" in meta_description_content else 0]

    canonical_link = soup.find("link", {"rel": "canonical"})["href"].strip() if soup.find("link", {"rel": "canonical"}) else ""
    return title, meta_description_content, store, canonical_link

def dataset_maker():

    data_list = []

    for i in URL_list:
        title, meta_description_content, store, canonical_link = scraper(i)

        data_dict = {
            "title": title,
            "content": meta_description_content,
            "store": store,
            "URL": canonical_link,
            "Output": None
        }

        data_list.append(data_dict)
        wait = random.randint(1, 30) * 0.1
        time.sleep(wait)
        print(i)

    df = pd.DataFrame(data_list)
    return df

df = dataset_maker()

def labeller():
    for i in range(len(df["Output"])):
        if i % 3 == 0:
            df.at[i, "Output"] = "ürün"
        elif i % 3 == 1:
            df.at[i, "Output"] = "mağaza"
        else:
            df.at[i, "Output"] = "kategori"

labeller()

df.head()

df.to_csv("web_sites.csv", index=False)
