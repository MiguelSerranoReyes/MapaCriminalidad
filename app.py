import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px

# Cargar los datos
df = pd.read_csv('carpetasFGJ_2023_reducido.csv')  # Asegúrate de que el nombre del archivo sea correcto

# Filtrar para asegurar que todas las filas tengan coordenadas
df = df.dropna(subset=['latitud', 'longitud'])

# Asumiendo que existe una columna 'categoria' en el DataFrame
categorias = df['categoria'].unique()

# Iniciar la aplicación Dash
app = dash.Dash(__name__)

# Definir el layout de la aplicación
app.layout = html.Div([
    html.H1("Mapa de Calor de Criminalidad en la Ciudad de México", className='h1'),
    dcc.Dropdown(
        id='categoria-selector',
        options=[{'label': i, 'value': i} for i in categorias],
        value='DELITO DE BAJO IMPACTO',  # Valor por defecto
        className='dropdown-estilizado'
    ),
    dcc.Graph(id='mapa-calor', className='graph')
], className='body')

# Callback para actualizar el mapa de calor
@app.callback(
    Output('mapa-calor', 'figure'),
    [Input('categoria-selector', 'value')]
)
def update_map(categoria_seleccionada):
    filtered_df = df[df['categoria'] == categoria_seleccionada]
    fig = px.density_mapbox(filtered_df, lat='latitud', lon='longitud', 
                            radius=10, 
                            center={"lat": 19.36, "lon": -99.133209}, 
                            zoom=10, 
                            mapbox_style="mapbox://styles/mapbox/light-v10")
    fig.update_layout(mapbox_accesstoken='pk.eyJ1IjoibWlnc2VycmFub3JleWVzIiwiYSI6ImNscGN1a2ttZzBvMWsyaXFvMnJ0N2ZlMzIifQ.SG8hRdvWh0Ob11TpfIknCg')
    return fig

# Ejecutar la aplicación
if __name__ == '__main__':
    app.run_server(debug=True)
    #app.run_server(debug=False, host='0.0.0.0', port=80)