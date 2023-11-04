import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import joblib
import requests
from bs4 import BeautifulSoup

st.set_page_config(layout="wide")

st.title("Page Type Prediction - Demo")
st.markdown("""
_This demo page is a deployed version of an ML model that detects whether the URL of [Hepsiburada](https://www.hepsiburada.com/), [Trendyol](https://www.trendyol.com/) and [n11](https://www.n11.com/) sites is a **product**, **store** or **category** page._
""")
st.markdown("""
Bu demo sayfası [Hepsiburada](https://www.hepsiburada.com/), [Trendyol](https://www.trendyol.com/) ve [n11](https://www.n11.com/) sitelerine ait URL'nin **ürün**, **mağaza** ya da **kategori** sayfası mı olduğunu tespit eden bir ML modelinin deploy edilmiş halidir.
""")


main_page, data_page = st.tabs(["Ana Sayfa", "Hakkında"])

#@st.cache_data
#def get_data():
#    df = pd.read_csv("web_sites.csv")
#    return df

@st.cache_data
def get_pipeline():
    pipeline = joblib.load("testinium.joblib")
    return pipeline

data_page.write("Loading...")
#df = get_data()
#data_page.dataframe(df, use_container_width=True)

#data_page.divider()

#data_page_col1, data_page_col2 = data_page.columns(2)

#fig = plt.figure(figsize=(6,4))
#n_categories = len(df['Output'].unique())
#colors = sns.color_palette("Set1", n_categories)
#ax = sns.countplot(data=df, x="Output", palette=colors)
#ax.set(xlabel="Tür", ylabel="Sayı")
#data_page_col1.subheader("Türlerine Göre Sayfa Sayısı")
#data_page_col1.pyplot(fig)

pipeline = get_pipeline()


def scraper(link):
    global soup
    global url
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


initial_value = ""
user_input = main_page.text_input("URL'yi aşağıdaki kutuya yapıştırın 👇", value=initial_value, )


def check(user_input):
    title, meta_description_content = scraper(user_input)
    text_predictions = title + " " + meta_description_content
    prediction = pipeline.predict({text_predictions})

    if prediction == 2:
        return "Ürün"
    elif prediction == 1:
        return "Mağaza"
    else:
        return "Kategori"

main_page_col1, main_page_col2 = main_page.columns(2)

product_name = ""
price = ""

if user_input != initial_value:
    result = check(user_input)
    if result == "Ürün":
        if "www.n11.com" in url:
            image_div = soup.find("div", {"class": "imgObj"})
            img_tag = image_div.find("img")
            image_url = img_tag['data-original']
            product_name = soup.find("h1", {"class": "proName"}).get_text(strip=True)
            price = soup.find("div", {"class": "unf-p-summary-price"}).get_text(strip=True)

        elif "www.hepsiburada.com" in url:
            image_div = soup.find("source", {"class": "product-image"})
            srcset = image_div["srcset"]
            urls = srcset.split(',')
            highest_resolution_url = urls[-1].strip().split()[0]
            image_url = highest_resolution_url.split('/format:')[0]
            product_name = soup.find("h1", {"class": "product-name best-price-trick"}).get_text(strip=True)
            price = soup.find("span", {"class": "variant-property-price"}).get_text(strip=True)

        elif "www.trendyol.com" in url:
            image_div = soup.find("meta", {"name": "twitter:image:src"})
            image_url = image_div["content"]
            product_name = soup.find("h1", {"class": "pr-new-br"}).get_text(strip=True)
            price = soup.find("span", {"class": "prc-dsc"}).get_text(strip=True)

        main_page_col1.image(image_url,width=600)

    if result == "Mağaza":
        if "www.n11.com" in url:
            image_div = soup.find("div", {"class": "sellerAvatar"})
            img_tag = image_div.find("img")
            image_url = img_tag['src']
            product_name = soup.title.string.strip()

        elif "www.hepsiburada.com" in url:
            image_div = soup.find("section", {"class": "mcontent-MerchantRow-2GUPv mcontent-MerchantRow-YDKz1"})
            img_tag = image_div.find("img")
            image_url = img_tag['src']
            product_name = soup.title.string.strip()


        elif "www.trendyol.com" in url:
            image_url = "https://www.entegi.com/wp-content/themes/entegi/assets/src/img/brand/trendyol.png"
            product_name = soup.title.string.strip()


        main_page_col1.image(image_url,width=300)

    if result == "Kategori":
        if "www.n11.com" in url:
            image_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/6/60/N11_logo.svg/2560px-N11_logo.svg.png"
            product_name = soup.title.string.strip()

        elif "www.hepsiburada.com" in url:
            image_url = "https://www.entegi.com/wp-content/themes/entegi/assets/src/img/brand/hepsiburada.png"
            product_name = soup.title.string.strip()


        elif "www.trendyol.com" in url:
            image_url = "https://www.entegi.com/wp-content/themes/entegi/assets/src/img/brand/trendyol.png"
            product_name = soup.title.string.strip()


        main_page_col1.image(image_url,width=300)

else:
    result = "Henüz bir URL girişi yapılmadı."

main_page_col2.markdown(f'<p style="font-size: 34px;color: red;">{result}</p>', unsafe_allow_html=True)
main_page_col2.write(product_name)
main_page_col2.markdown(f'<p style="font-weight: bold; font-size: 20px; color: white;">{price}</p>', unsafe_allow_html=True)




