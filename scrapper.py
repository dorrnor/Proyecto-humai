import requests
from lxml import html
import re
import pandas as pd
import os
import dash
from dash import dcc, html as htmll
from dash.dependencies import Input, Output
import plotly.express as px
def get_data_url(url):
    response = requests.get(url)
    tree = html.fromstring(response.content)
    urls = tree.xpath('//div[@class="span4"]//a/@href')
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
            Positive_points = inner_tree.xpath('//*[@id="globalwrap"]/div[4]/article/div/div[3]/div/div[2]/div/text()')
            negative_points = inner_tree.xpath('//*[@id="globalwrap"]/div[4]/article/div/div[3]/div/div[3]/div/text()')
            positive_count = len(Positive_points)
            negative_count = len(negative_points)
            price_element = inner_tree.xpath('//div[@class="fichatecnica"]//li[starts-with(., "Precio")]/text()')
            if price_element:
                price_text = price_element[0]
                price_text_cleaned = clean_price_text(price_text)
             #   print(price_text_cleaned)
            data.append({
                "Titulo": title,
                "Puntaje": score,
                "Comentarios positivos":positive_count,
                "Comentarios negativos":negative_count,
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
    df = get_data_url(url)
    folder_name = "datos"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    csv_file_path = os.path.join(folder_name, "resultados.csv")
    df.to_csv(csv_file_path, sep="\t", encoding="utf-8-sig", index=False)
    # Cargar los datos desde el archivo CSV
    df = pd.read_csv("datos/resultados.csv", sep="\t", encoding="utf-8-sig")
    # Inicializar la aplicación Dash
    app = dash.Dash(__name__)
    # Diseño de la aplicación
    app.layout = htmll.Div([
        htmll.H1("Dashboards de analisis de Vandal"),
        dcc.Dropdown(
            id='game-dropdown',
            options=[{'label': titulo, 'value': titulo} for titulo in df['Titulo']],
            multi=True,
            value=list(df['Titulo']),  # Todos los juegos seleccionados por defecto
        ),
        dcc.Graph(id='price-bar-chart'),
        dcc.Graph(id='score-bar-chart'),
        dcc.Dropdown(
            id='prueba-dropdown',
            options=[{'label': titulo, 'value': titulo} for titulo in df['Titulo']],
            multi=True,
            value=[df['Titulo'][0]],
            placeholder="Seleccione uno o más juegos"
        ),
        dcc.Graph(id='commentPositive-bar-chart'),
    ])
    # Callback para actualizar el gráfico en función de la selección del usuario
    @app.callback(
        Output('price-bar-chart', 'figure'),
        [Input('game-dropdown', 'value')]
    )
    def update_price_bar_chart(selected_games):
        filtered_df = df[df['Titulo'].isin(selected_games)]
        fig = px.bar(filtered_df, x='Titulo', y='Precio', title='Precios de Videojuegos')
        fig.update_xaxes(categoryorder='total descending')
        return fig
    @app.callback(
        Output('score-bar-chart', 'figure'),
        [Input('game-dropdown', 'value')]
    )
    def update_rating_bar_chart(selected_games):
        filtered_df = df[df['Titulo'].isin(selected_games)]
        fig = px.bar(filtered_df, x='Titulo', y='Puntaje', title='Puntaje de Videojuegos')
        fig.update_xaxes(categoryorder='total descending')
        return fig
    @app.callback(
        Output('commentPositive-bar-chart', 'figure'),
        [Input('prueba-dropdown', 'value')]
    )
    def update_coment_bar_chart(selected_games):
        filtered_df = df[df['Titulo'].isin(selected_games)]
        # Crear un DataFrame con las columnas 'Titulo' y 'Comentarios positivos' y 'Comentarios negativos'
        rating_df = filtered_df[['Titulo', 'Comentarios positivos', 'Comentarios negativos']]
        # Configurar colores personalizados para las barras
        color_discrete_map = {'Comentarios positivos': 'green', 'Comentarios negativos': 'red'}
        fig = px.bar(rating_df, x='Titulo', y=['Comentarios negativos', 'Comentarios positivos'],
                     title='Comentarios Positivos y Negativos de Videojuegos',
                     barmode='stack',
                     color_discrete_map=color_discrete_map)  # Asignar colores personalizados
        fig.update_xaxes(categoryorder='total descending')
        return fig
    # Ejecutar la aplicación
    app.run_server(debug=True)