# Importar las bibliotecas necesarias
import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

# Definir la función para diseñar el layout del dashboard
def dashboardDiseño(app):
    # Diseño de la aplicación utilizando componentes de Dash
    app.layout = html.Div([
        html.H1("Dashboards de análisis de Vandal"),
        
        # Dropdown para seleccionar los juegos
        dcc.Dropdown(
            id='game-dropdown',
            options=[{'label': titulo, 'value': titulo} for titulo in df['Titulo']],
            multi=True,
            value=list(df['Titulo']),  # Todos los juegos seleccionados por defecto
        ),
        
        # Gráfico de barras para la recomendación
        dcc.Graph(id='recomendation-bar-chart'),
        dcc.RangeSlider(
         id='price-slider',
         min=df['Precio'].min(),
         max=df['Precio'].max(),
         step=1,
         marks={
             0: {'label': f'${df["Precio"].min()}', 'style': {'transform': 'translateX(-50%)'}},
             df['Precio'].max(): {'label': f'${df["Precio"].max()}'}
         },
         value=[df['Precio'].min(), df['Precio'].max()]
        ),
        html.Div(id='price-range-output'),
        
        # Dropdown dinámico para seleccionar juegos para otros gráficos
        dcc.Dropdown(
            id='dinamic-dropdown',
            options=[{'label': titulo, 'value': titulo} for titulo in df['Titulo']],
            multi=True,
            value=[df['Titulo'][0]],
            placeholder="Seleccione uno o más juegos"
        ),
        
        # Gráfico de barras para el precio
        dcc.Graph(id='price-bar-chart'),
        
        # Gráfico de barras para el puntaje
        dcc.Graph(id='score-bar-chart'),
        
        # Gráfico de barras para los comentarios positivos y negativos
        dcc.Graph(id='commentPositive-bar-chart'),
    ])

    return app

# Definir la función de callback para actualizar los gráficos basados en la selección del usuario
def callback(dashboard):
    # Callback para actualizar el gráfico de recomendación
    @dashboard.callback(
        [Output('recomendation-bar-chart', 'figure'),
        Output('price-range-output', 'children')],
        [Input('game-dropdown', 'value'),
        Input('price-slider', 'value')]
    )
    def update_recomendation_bar_chart(selected_games,price_range):
        filtered_df = df[df['Titulo'].isin(selected_games) & (df['Precio'] >= price_range[0]) & (df['Precio'] <= price_range[1])]
        fig = px.bar(filtered_df, x='Titulo', y='Recomendacion', title='Recomendación de Videojuegos')
        fig.update_xaxes(categoryorder='total descending')
        price_range_text = f'Rango de precios: ${price_range[0]} - ${price_range[1]}'
        return fig, price_range_text
    
    # Callback para actualizar el gráfico de precio
    @dashboard.callback(
        Output('price-bar-chart', 'figure'),
        Input('dinamic-dropdown', 'value'),
        )
    def update_price_bar_chart(selected_games):
        filtered_df = df[df['Titulo'].isin(selected_games)]
        fig = px.bar(filtered_df, x='Titulo', y='Precio', title='Precio de Videojuegos')
        fig.update_xaxes(categoryorder='total descending')
        return fig
    
    # Callback para actualizar el gráfico de puntaje
    @dashboard.callback(
        Output('score-bar-chart', 'figure'),
        [Input('dinamic-dropdown', 'value')]
    )
    def update_rating_bar_chart(selected_games):
        filtered_df = df[df['Titulo'].isin(selected_games)]
        fig = px.bar(filtered_df, x='Titulo', y='Puntaje', title='Puntaje de Videojuegos')
        fig.update_xaxes(categoryorder='total descending')
        return fig
    
  
    
    # Callback para actualizar el gráfico de comentarios positivos y negativos
    @dashboard.callback(
        Output('commentPositive-bar-chart', 'figure'),
        [Input('dinamic-dropdown', 'value')]
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

# Punto de entrada del programa
if __name__ == "__main__":
    # Cargar los datos desde el archivo CSV
    df = pd.read_csv("../datos/resultados.csv", sep="\t", encoding="utf-8-sig")

    # Inicializar la aplicación Dash
    app = dash.Dash(__name__)
    dashboard = dashboardDiseño(app)
    fig = callback(dashboard)
    
    # Ejecutar la aplicación en modo debug
    app.run_server(debug=True)