  
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash.dependencies import Input, Output

# Cargar los datos desde las hojas correspondientes
df_recursos = pd.read_excel('DATA IMM MORELOS.xlsx', sheet_name='RECURSOS TOTAL')
df_monitoreo = pd.read_excel('DATA IMM MORELOS.xlsx', sheet_name='MONITOREO DEL PRESUPUESTO')
df_prevention = pd.read_excel('DATA IMM MORELOS.xlsx', sheet_name='PREVENCIÓN')
df_servicios = pd.read_excel('DATA IMM MORELOS.xlsx', sheet_name='NÚMERO DE SERVICIOS')  # Nueva hoja
df_violencia = pd.read_excel('DATA IMM MORELOS.xlsx', sheet_name='TIPO Y MOD. VIOL.')

# Eliminar la primera columna innecesaria en df_servicios
df_servicios = df_servicios.drop(columns=['Unnamed: 0'])

# Convertir las columnas numéricas a tipo numérico y manejar errores
df_monitoreo['EJECUTADO'] = pd.to_numeric(df_monitoreo['EJECUTADO'], errors='coerce').fillna(0)
df_monitoreo['POR EJECUTAR'] = pd.to_numeric(df_monitoreo['POR EJECUTAR'], errors='coerce').fillna(0)
df_monitoreo['TOTAL'] = pd.to_numeric(df_monitoreo['TOTAL'], errors='coerce').fillna(0)

# Calcular el porcentaje de avance (EJECUTADO / TOTAL)
df_monitoreo['PORCENTAJE AVANCE'] = df_monitoreo['EJECUTADO'] / df_monitoreo['TOTAL'] * 100
df_monitoreo['POR EJECUTAR'] = df_monitoreo['TOTAL'] - df_monitoreo['EJECUTADO']

# Crear el gráfico de barras de violencia por grupo con los colores solicitados
fig_violen_bar = px.bar(df_long,
                        x='VIOLENCIA',
                        y='NUMERO_DE_PERSONAS',
                        color='GRUPO',
                        color_discrete_map=color_map,
                        orientation='v',
                        title="PERSONAS ALCANZADAS POR PROCESOS DE PREVENCIÓN",
                        labels={'NUMERO_DE_PERSONAS': 'Número de Personas', 'VIOLENCIA': 'Tipo de Violencia'},
                        hover_data={'NUMERO_DE_PERSONAS': True, 'GRUPO': True})

fig_violen_bar.update_traces(
    hovertemplate='<b>%{x}</b><br>%{y} personas',  # Aquí se muestra "personas"
    customdata=df_long[['GRUPO']].values  # Personalizamos el hover para mostrar el grupo asociado
)

# Inicializar la aplicación Dash
app = dash.Dash(__name__)

# Estructura de la aplicación con el mapa integrado
app.layout = html.Div([
    html.Div([
        html.H1("PLATAFORMA DE MONITOREO DE RECURSOS FEDERALES DEL INSTITUTO DE LA MUJER PARA EL ESTADO DE MORELOS", style={
            'textAlign': 'center', 'font-family': 'Arial, sans-serif', 'color': '#333333', 'font-weight': 'bold'}),
        html.P("Indicadores de gasto y de resultados de los recursos federales transferidos por la Comisión Nacional para Prevenir y Erradicar la Violencia contra las Mujeres y el Instituto Nacional de las Mujeres.",
               style={'textAlign': 'center', 'font-family': 'Arial, sans-serif', 'color': '#333333', 'font-style': 'italic', 'font-size': '16px', 'marginTop': '10px'})
    ], style={'marginBottom': '40px'}),  # Título centrado y margen inferior para separación

    # Gráfico de pastel con la distribución de recursos
    html.Div([
        html.H3("DISTRIBUCIÓN DE RECURSOS POR PROGRAMA", style={'textAlign': 'center', 'font-family': 'Arial, sans-serif', 'color': '#333333'}),
        dcc.Graph(id='grafico-pie', figure=fig_pie),
    ], style={'textAlign': 'center', 'marginBottom': '40px'}),  # Gráfico centrado y márgenes

    # Menú desplegable para seleccionar el rubro de recursos para el gráfico de barras
    html.Div([
        html.Label('Selecciona el rubro de recursos para el gráfico de barras:', style={
            'textAlign': 'center', 'font-family': 'Arial, sans-serif', 'color': '#333333'}),
        dcc.Dropdown(
            id='recurso-dropdown',
            options=[
                {'label': 'Recursos Humanos', 'value': 'RECURSOS HUMANO'},
                {'label': 'Recursos Materiales', 'value': 'RECURSOS MATERIALES'},
                {'label': 'Metas del Proyecto', 'value': 'METAS DEL PROYECTO'}
            ],
            value='RECURSOS HUMANO'  # Valor inicial
        ),
    ], style={'textAlign': 'center', 'marginBottom': '40px'}),  # Centrado y separación

    # Gráfico de barras de recursos
    html.Div([
        html.H3("RECURSOS FEDERALES POR PARTIDA PRESUPUESTAL", style={'textAlign': 'center', 'font-family': 'Arial, sans-serif', 'color': '#333333'}),
        dcc.Graph(id='grafico-barras', figure=fig_bar),
    ], style={'textAlign': 'center', 'marginBottom': '40px'}),

    # Gráfico de barras de mujeres atendidas
    html.Div([
        html.H3("MUJERES ALCANZADAS POR LOS SERVICIOS DEL CDM Y CAE DEL INSTITUTO DE LA MUJER PARA EL ESTADO DE MORELOS", style={'textAlign': 'center', 'font-family': 'Arial, sans-serif', 'color': '#333333'}),
        dcc.Graph(id='grafico-mujeres', figure=fig_mujeres),
    ], style={'textAlign': 'center', 'marginBottom': '40px'}),

    # Gráfico de barras de violencia por grupo
    html.Div([
        html.H3("PERSONAS ALCANZADAS POR PROCESOS DE PREVENCIÓN", style={'textAlign': 'center', 'font-family': 'Arial, sans-serif', 'color': '#333333'}),
        dcc.Graph(id='grafico-violencia', figure=fig_violen_bar),
    ], style={'textAlign': 'center', 'marginBottom': '40px'}),

    # Gráfico de barras de violencia
    html.Div([
        html.H3("MODALIDAD Y TIPOS DE VIOLENCIA EN MUNICIPIOS", style={'textAlign': 'center', 'font-family': 'Arial, sans-serif', 'color': '#333333'}),
        dcc.Graph(id='grafico-violencia-barras', figure=fig_violencia_barras),
    ], style={'textAlign': 'center', 'marginBottom': '40px'}),

    # Gráfico de barras apiladas de servicios brindados
    html.Div([
        html.H3("NÚMERO DE SERVICIOS BRINDADOS 2023 POR CENTRO DE ATENCIÓN EXTERNA", style={'textAlign': 'center', 'font-family': 'Arial, sans-serif', 'color': '#333333'}),
        dcc.Graph(id='grafico-servicios', figure=fig_servicios),
    ], style={'textAlign': 'center', 'marginBottom': '40px'}),

    # Agregar el mapa de georreferenciación
    html.Div([
        html.H3("GEORREFERENCIACIÓN DE SERVICIOS EN MORELOS", style={'textAlign': 'center', 'font-family': 'Arial, sans-serif', 'color': '#333333'}),
        dcc.Graph(id='mapa-georeferenciacion', figure=fig_map),
    ], style={'textAlign': 'center', 'marginBottom': '40px'}),

    # Texto al final de la página
    html.Div([
        html.P("ELABORADO POR LIC.C.POL. EDUARDO CABRERA GUTIÉRREZ.", style={'textAlign': 'center', 'font-family': 'Arial, sans-serif', 'color': '#333333', 'marginTop': '40px'}),
        html.P("CORREO: CABARDO.GUTZ@GMAIL.COM", style={'textAlign': 'center', 'font-family': 'Arial, sans-serif', 'color': '#333333'})
    ], style={'marginTop': '20px'})
], style={
    'backgroundColor': '#f4f4f9',  # Fondo neutro y profesional
    'font-family': 'Arial, sans-serif',  # Fuente moderna
    'color': '#333333',  # Color oscuro para un contraste adecuado
    'padding': '20px'
})

# Callback para actualizar el gráfico de barras según el dropdown
@app.callback(
    Output('grafico-barras', 'figure'),
    [Input('recurso-dropdown', 'value')]
)
def actualizar_grafico_barras(valor_seleccionado):
    if valor_seleccionado == 'RECURSOS HUMANO':
        columnas = ['RECURSOS HUMANO']
    elif valor_seleccionado == 'RECURSOS MATERIALES':
        columnas = ['RECURSOS MATERIALES']
    elif valor_seleccionado == 'METAS DEL PROYECTO':
        columnas = ['METAS DEL PROYECTO']

    # Crear el gráfico de barras actualizado
    fig_barras_actualizado = px.bar(
        df_monitoreo,
        x=columnas,  # Usar la columna seleccionada
        y='PROGRAMA',  # Cada barra será para un programa
        orientation='h',  # Barras horizontales
        barmode='stack',  # Barras apiladas
        title="MONITOREO DE PRESUPUESTO DE RECURSOS",
        labels={'value': 'Monto', 'PROGRAMA': 'Programa'},
        hover_data={'PROGRAMA': True},
        color='PROGRAMA',  # Usar 'PROGRAMA' como base para color
        color_discrete_map={  # Colores personalizados
            'PAIMEF': '#c72c18',
            'PROABIM': '#643ee6',
            'FOBAM': '#489f3b'
        }
    )

    return fig_barras_actualizado

if __name__ == '__main__':
    app.run_server(debug=True)
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash.dependencies import Input, Output

# Cargar los datos
df_recursos = pd.read_excel('DATA IMM MORELOS.xlsx', sheet_name='RECURSOS TOTAL')

# Inicializar la aplicación Dash
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Ejemplo de Aplicación Dash"),
    dcc.Graph(figure=px.bar(df_recursos, x='Columna1', y='Columna2'))
])

server = app.server

if __name__ == "__main__":
    app.run_server(debug=True)
