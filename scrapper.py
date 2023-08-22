import requests
from lxml import html

url = "https://vandal.elespanol.com/analisis/videojuegos"
response = requests.get(url)

tree = html.fromstring(response.content)

urls = tree.xpath('//div[@class="span4"]//a/@href')

for relative_url in urls:
    full_url = f"{relative_url}"
    print("Procesando:", full_url)
    
    response = requests.get(full_url)
    
    if response.status_code == 200:
        inner_tree = html.fromstring(response.content)
        
       
        title = inner_tree.xpath('//div[@class="titulojuego"]/a/text()')
        print("Título:", title)
        score = inner_tree.xpath('//*[@id="globalwrap"]/div[4]/article/div/div[3]/div/div[1]/div[1]/div[2]/text()')
    
        print("Puntaje:",score)

        


        version = inner_tree.xpath('/html/body/div[5]/div[2]/div/section/div[4]/div[1]/h3/b')
        print("Ficha técnica de la versión:",version)


        price_element = inner_tree.xpath('//*[@id="fichatecnica2_13"]/ul/li[5]/text()')
        if price_element:
            price_text = price_element[0]
            price_text_cleaned = price_text.replace("Precio:", "").strip().replace("€", "").replace(",", "")
            
            price_number = ''.join(filter(lambda x: x.isdigit() or x == ".", price_text_cleaned))
            
            if price_number:
                if "." in price_number:
                    price_value = float(price_number)
                else:
                    price_value = int(price_number)
            else:
                price_value = None
        else:
            price_value = None

        print("Precio:", price_value)

        
        
    else:
        print(f"Error al acceder a {full_url}. Código de estado: {response.status_code}")
