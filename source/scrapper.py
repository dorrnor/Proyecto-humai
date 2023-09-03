import requests
from lxml import html
import re
import pandas as pd
import os
import subprocess
import webbrowser 

# Función para obtener los datos de análisis de videojuegos desde una URL
def get_data_url(url):

    # Pesos para los diferentes factores de recomendación
    peso_positivo = 0.3
    peso_negativo = 0.1
    peso_precio = 0.05
    peso_rating = 1

    # Realizar una solicitud HTTP para obtener el contenido de la página
    response = requests.get(url)
    tree = html.fromstring(response.content)
    # Encontrar los enlaces a las páginas individuales de los juegos
    urls = tree.xpath('//div[@class="span4"]//a/@href')
    data = []
    for relative_url in urls:
        full_url = f"{relative_url}"
        response = requests.get(full_url)
        if response.status_code == 200:
            inner_tree = html.fromstring(response.content)
            # Extraer información específica de la página individual del juego
            title = inner_tree.xpath('//div[@class="titulojuego"]/a/text()')[0]
            score = inner_tree.xpath('//*[@id="globalwrap"]/div[4]/article/div/div[3]/div/div[1]/div[1]/div[2]/text()')[0]
            version = inner_tree.xpath('//div[1]/h3[@class="h3ficha"]/b/text()')[0]
            analysis = inner_tree.xpath('//div[@class="textart"]//p/text()')
            analysis_text = ' '.join(analysis)
            Positive_points = inner_tree.xpath('//*[@id="globalwrap"]/div[4]/article/div/div[3]/div/div[2]/div/text()')
            negative_points = inner_tree.xpath('//*[@id="globalwrap"]/div[4]/article/div/div[3]/div/div[3]/div/text()')
            positive_count = len(Positive_points)
            negative_count = len(negative_points)
            price_element = inner_tree.xpath('//div[@class="fichatecnica"]//li[starts-with(., "Precio")]/text()')
            genero = inner_tree.xpath('//div[@class="mt1 tcenter t11"]/a/text()')
            genero = ' '.join(genero)

            # Limpiar y procesar el precio
            if price_element:
                price_text = price_element[0]
                price_text_cleaned = clean_price_text(price_text)
            
            if price_text_cleaned == "":
                price_text_cleaned = 0

            # Calcular la recomendación basada en diferentes factores
            data.append({
                "Titulo": title,
                "Genero": genero,
                "Puntaje": score,
                "Comentarios positivos": positive_count,
                "Comentarios negativos": negative_count,
                "Version": version,
                "Analisis": analysis_text,
                "Precio": price_text_cleaned,
                "Recomendacion": (peso_precio * float(price_text_cleaned)) + 
                                 (peso_positivo * positive_count) + 
                                 (peso_negativo * negative_count) + 
                                 (peso_rating * float(score))
            })
        else:
            print(f"Error al acceder a {full_url}. Código de estado: {response.status_code}")
    return pd.DataFrame(data)

# Función para limpiar el texto del precio
def clean_price_text(price_text):
    price_text_cleaned = re.sub(r'^Precio:\s*', '', price_text).replace("€", "").strip()
    price_text_cleaned = price_text_cleaned.replace(',','. ')
    price_text_cleaned = price_text_cleaned.strip('.')
    price_text_cleaned = re.sub(r'[^\d.]', '', price_text_cleaned)
    return price_text_cleaned

# Función para enviar un mensaje de notificación a través de Telegram
def enviar_mensaje():
    bot_token = '6363521525:AAHU6ooDJmi-JLhDvgYxdjJdZclh_FyJxy4'
    chat_id = '-966069482'  
    message = "Los datos ya fueron scrappeados y se pueden visualizar en el siguiente dashboard http://127.0.0.1:8050/"
    requests.post(f'https://api.telegram.org/bot{bot_token}/sendMessage',
                  data={'chat_id': chat_id, 'text': message})

# Punto de entrada del programa
if __name__ == "__main__":
    url = "https://vandal.elespanol.com/analisis/videojuegos"
    df = get_data_url(url)
    
    # Obtener la ruta actual del archivo
    current_file_path = os.path.abspath(__file__)
    source_directory = os.path.dirname(current_file_path)
    project_directory = os.path.dirname(source_directory)

    # Crear una carpeta para guardar los resultados si no existe
    folder_name = "datos"
    new_folder_path = os.path.join(project_directory, folder_name)
    if not os.path.exists(new_folder_path):
        os.makedirs(new_folder_path)
    csv_file_path = os.path.join(new_folder_path, "resultados.csv")

    # Abrir la URL del servidor del dashboard en el navegador
    server_address = "http://127.0.0.1:8050/"
    server_port = 8050
    server_url = f"{server_address}:{server_port}"
    webbrowser.open_new(server_url)

    # Guardar los datos en un archivo CSV
    df.to_csv(csv_file_path, sep="\t", encoding="utf-8-sig", index=False)

    # Enviar mensaje de notificación a través de Telegram
    enviar_mensaje()

    # Llamar y ejecutar el script del dashboard
    print("Ejecutando dashboard.py... ")
    subprocess.run(["python", "dashboard.py"])