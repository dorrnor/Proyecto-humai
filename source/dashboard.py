import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px



def dashboardDiseño(app):
    # Diseño de la aplicación
    app.layout = html.Div([
        html.H1("Dashboards de analisis de Vandal"),
        dcc.Dropdown(
            id='game-dropdown',
            options=[{'label': titulo, 'value': titulo} for titulo in df['Titulo']],
            multi=True,
            value=list(df['Titulo']),  # Todos los juegos seleccionados por defecto
        ),
        dcc.Graph(id='recomendation-bar-chart'),
        dcc.Dropdown(
            id='dinamic-dropdown',
            options=[{'label': titulo, 'value': titulo} for titulo in df['Titulo']],
            multi=True,
            value=[df['Titulo'][0]],
            placeholder="Seleccione uno o más juegos"
        ),
        dcc.Graph(id='price-bar-chart'),
        dcc.Graph(id='score-bar-chart'),
        dcc.Graph(id='genre-bar-chart'),
        dcc.Graph(id='commentPositive-bar-chart'),
    ])

    return app


def callback(dashboard):
     # Callback para actualizar el gráfico en función de la selección del usuario
    @dashboard.callback(
        Output('recomendation-bar-chart', 'figure'),
        [Input('game-dropdown', 'value')]
    )
    def update_recomendation_bar_chart(selected_games):
        filtered_df = df[df['Titulo'].isin(selected_games)]
        fig = px.bar(filtered_df, x='Titulo', y='Recomendacion', title='Recomendacion de Videojuegos')
        fig.update_xaxes(categoryorder='total descending')
        return fig
    
    @dashboard.callback(
        Output('price-bar-chart', 'figure'),
        [Input('dinamic-dropdown', 'value')]
    )
    def update_price_bar_chart(selected_games):
        filtered_df = df[df['Titulo'].isin(selected_games)]
        fig = px.bar(filtered_df, x='Titulo', y='Precio', title='Precio de Videojuegos')
        fig.update_xaxes(categoryorder='total descending')
        return fig
    
    @dashboard.callback(
        Output('score-bar-chart', 'figure'),
        [Input('dinamic-dropdown', 'value')]
    )
    def update_rating_bar_chart(selected_games):
        filtered_df = df[df['Titulo'].isin(selected_games)]
        fig = px.bar(filtered_df, x='Titulo', y='Puntaje', title='Puntaje de Videojuegos')
        fig.update_xaxes(categoryorder='total descending')
        return fig
    
    @dashboard.callback(
        Output('genre-bar-chart', 'figure'),
        [Input('dinamic-dropdown', 'value')]
    )
    def update_genre_bar_chart(selected_games):
        filtered_df = df[df['Titulo'].isin(selected_games)]
        fig = px.bar(filtered_df, x='Titulo', y='Genero', title='Genero de Videojuegos')
        fig.update_xaxes(categoryorder='total descending')
        return fig
    
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

if __name__ == "__main__":
    # Cargar los datos desde el archivo CSV
    df = pd.read_csv("../datos/resultados.csv", sep="\t", encoding="utf-8-sig")

    # Inicializar la aplicación Dash
    app = dash.Dash(__name__)
    dashboard = dashboardDiseño(app)
    fig = callback(dashboard)
    
    # Ejecutar la aplicación
    app.run_server(debug=True)