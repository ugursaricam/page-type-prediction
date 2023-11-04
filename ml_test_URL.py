import requests
from bs4 import BeautifulSoup
import joblib

pipe = joblib.load("testinium.joblib")

def scraper(link):
    url = link
    headers = {
        'User-Agent':
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36'}
    response = requests.get(url, headers=headers)

    soup = BeautifulSoup(response.content, 'html.parser')

    title = soup.title.string.strip().lower() if soup.title else ""

    meta_description = soup.find("meta", {"name": "description"})
    meta_description_content = meta_description["content"].strip().lower() if meta_description else ""

    return title, meta_description_content

def check():
    user_input = input("Lütfen bir URL girin: ")
    title, meta_description_content = scraper(user_input)
    text_predictions = title + " " + meta_description_content
    prediction = pipe.predict({text_predictions})

    if prediction == 2:
        return "Ürün"
    elif prediction == 1:
        return "Mağaza"
    else:
        return "Kategori"

check()