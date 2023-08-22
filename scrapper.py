import requests
from lxml import html
import re
import pandas as pd



def get_data_url(url):
    response = requests.get(url)

    tree = html.fromstring(response.content)

    urls = tree.xpath('//div[@class="span4"]//a/@href')
    print(urls)
    data = []

    for relative_url in urls:
        full_url = f"{relative_url}"
        
        response = requests.get(full_url)
    
        
        if response.status_code == 200:
            inner_tree = html.fromstring(response.content)
            
            title = inner_tree.xpath('//div[@class="titulojuego"]/a/text()')[0]
            #print("Título:", title)
            
            score = inner_tree.xpath('//*[@id="globalwrap"]/div[4]/article/div/div[3]/div/div[1]/div[1]/div[2]/text()')[0]
            #print("Puntaje:", score)

            version = inner_tree.xpath('//div[1]/h3[@class="h3ficha"]/b/text()')[0]
            #print("Ficha técnica de la versión:", version)

            analysis = inner_tree.xpath('//div[@class="textart"]//p/text()')
            analysis_text = ' '.join(analysis)
            #print("Análisis:", analysis_text)

            price_element = inner_tree.xpath('//div[@class="fichatecnica"]//li[starts-with(., "Precio")]/text()')
            if price_element:
                price_text = price_element[0]
                price_text_cleaned = clean_price_text(price_text)
                



             #   print(price_text_cleaned)


            data.append({
                "Titulo": title,
                "Puntaje": score,
                "Version": version,
                "Analisis": analysis_text,
                "Precio": price_text_cleaned
            })
            
                

        else:
            print(f"Error al acceder a {full_url}. Código de estado: {response.status_code}")

    return pd.DataFrame(data)

def clean_price_text(price_text):
    price_text_cleaned = re.sub(r'^Precio:\s*', '', price_text).replace("€", "").strip()
    price_text_cleaned = price_text_cleaned.replace(',','. ')
    price_text_cleaned = price_text_cleaned.strip('.')
    price_text_cleaned = re.sub(r'[^\d.]', '', price_text_cleaned)
    return price_text_cleaned
if __name__ == "__main__":

    url = "https://vandal.elespanol.com/analisis/videojuegos"

    df= get_data_url(url)

    df.to_csv("resultados.csv", sep="\t", encoding="utf-8-sig", index=False)
