# -*- coding: utf-8 -*-
"""PROYECTO III. IMM MORELOS DEFINITIVO PARA PUB.

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Vfs9_vOYjdrfIsX3jnw0NRNqCLz6hyH-
"""

import pandas as pd
df = pd.read_excel('DATA IMM MORELOS.xlsx', sheet_name=None)

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
df_servicios = pd.read_excel('DATA IMM MORELOS.xlsx', sheet_name='NÚMERO DE SERVICIOS')
df_servicios = df_servicios.drop(columns=['Unnamed: 0'])
df_georef = pd.read_excel('DATA IMM MORELOS.xlsx', sheet_name='SERVICIOS DE GEORREFERENCIA I')

# Cargar los datos desde la hoja 'TIPO Y MOD. VIOL.' del archivo Excel
df_violencia = pd.read_excel('DATA IMM MORELOS.xlsx', sheet_name='TIPO Y MOD. VIOL.')

# Renombrar las columnas para facilitar la manipulación
df_violencia.columns = ['TIPO', 'PSICOLOGÍCA', 'FÍSICA', 'ECONÓMICA', 'SEXUAL', 'PATRIMONIAL', 'FAMILIAR',
                        'LABORAL Y DOCENTE', 'COMUNITARIA', 'INSTITUCIONAL', 'POLÍTICA', 'DIGITAL Y MEDIÁTICA', 'FEMINICIDA']

# Eliminar la primera fila que contiene los encabezados de los tipos de violencia
df_violencia = df_violencia.drop(index=0)

# Eliminar cualquier fila que contenga la fuente o cualquier texto adicional
df_violencia = df_violencia[df_violencia['TIPO'] != 'Fuente: https://drive.google.com/file/d/1W3VPYsFHPUVnhIYtdlXUjicWunj7Mvuc/view?usp=drive_link']

# Convertir los datos a tipo numérico (para asegurarnos que se pueda trabajar con los valores)
df_violencia.iloc[:, 1:] = df_violencia.iloc[:, 1:].apply(pd.to_numeric)

# Aplanar el DataFrame a formato largo (long format)
df_long_violencia = df_violencia.melt(id_vars=['TIPO'],
                                      var_name='MODALIDAD',
                                      value_name='NUMERO_DE_VIOLENCIA')

# Diccionario de reemplazo para los nombres de los CAE
nombres_cae = {
    'LÍNEA SEGURA': 'LÍNEA SEGURA',
    'ÚNIDAD MÓVIL': 'UNIDAD MÓVIL',
    'CAE JONACATEPEC': 'JONACATEPEC',
    'CAE HUEYAPAN': 'HUEYAPAN',
    'CAE XOCHITEPEC': 'XOCHITEPEC',
    'CAE EMILIANO ZAPATA': 'EMILIANO ZAPATA',
    'CAE TEMIXCO': 'TEMIXCO',
    'CAE TETECALA': 'TETECALA',
    'CJM CUERNAVACA': 'CUERNAVACA',
    'CJM': 'YAUTEPEC',
    'CAE CUERNAVACA': 'CUERNAVACA',
    'CAE YECAPIXTLA': 'YECAPIXTLA',
    'CAE AYALA': 'AYALA',
    'CAE JIUTEPEC': 'JIUTEPEC'
}

# Reemplazar los nombres de los CAE
df_long_violencia['MODALIDAD'] = df_long_violencia['MODALIDAD'].replace(nombres_cae)


# Convertir las columnas numéricas a tipo numérico y manejar errores
df_monitoreo['EJECUTADO'] = pd.to_numeric(df_monitoreo['EJECUTADO'], errors='coerce').fillna(0)
df_monitoreo['POR EJECUTAR'] = pd.to_numeric(df_monitoreo['POR EJECUTAR'], errors='coerce').fillna(0)
df_monitoreo['TOTAL'] = pd.to_numeric(df_monitoreo['TOTAL'], errors='coerce').fillna(0)

# Calcular el porcentaje de avance (EJECUTADO / TOTAL)
df_monitoreo['PORCENTAJE AVANCE'] = df_monitoreo['EJECUTADO'] / df_monitoreo['TOTAL'] * 100
df_monitoreo['POR EJECUTAR'] = df_monitoreo['TOTAL'] - df_monitoreo['EJECUTADO']

# Convertir los datos de PREVENCIÓN a formato largo para crear el gráfico de barras
df_long = df_prevention.melt(id_vars=['VIOLENCIA'],
                             value_vars=['NIÑAS ALCANZADOS', 'NIÑOS ALCANZADOS', 'MUJERES', 'HOMBRES'],
                             var_name='GRUPO',
                             value_name='NUMERO_DE_PERSONAS')

# Mapear los valores de grupo a las categorías correctas
group_map = {
    'NIÑAS ALCANZADOS': 'NIÑAS',  # Cambié 'NIÑAS ALCANZADAS' a 'NIÑAS'
    'NIÑOS ALCANZADOS': 'NIÑOS',
    'MUJERES': 'MUJERES',
    'HOMBRES': 'HOMBRES'
}

# Reemplazar las etiquetas de los grupos
df_long['GRUPO'] = df_long['GRUPO'].map(group_map)

# Colores personalizados para los grupos en el gráfico de prevención
color_map = {
    'NIÑAS': '#ea3f24',
    'NIÑOS': '#ef6141',
    'MUJERES': '#f87f5c',
    'HOMBRES': '#ffc598'
}

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

# Modificar el hover para mostrar "personas" en lugar de "NIÑAS", "NIÑOS", "HOMBRES", "MUJERES"
fig_violen_bar.update_traces(
    hovertemplate='<b>%{x}</b><br>%{y} personas',  # Aquí se muestra "personas"
    customdata=df_long[['GRUPO']].values  # Personalizamos el hover para mostrar el grupo asociado
)

# Crear el gráfico de pastel con colores personalizados
fig_pie = px.pie(df_recursos,
                 names='PROGRAMA',
                 values='RECURSOS',
                 title='Distribución de Recursos por Programa',
                 color='PROGRAMA',
                 color_discrete_map={
                     'PAIMEF (Programa de Apoyo a las Instancias de las Mujeres en las Entidades Federativas)': '#c72c18',  # Naranja para PAIMEF
                     'PROABIM (Programa para el Adelanto, Bienestar e Igualdad de las Mujeres)': '#643ee6', # Morado para PROABIM
                     'FOBAM (Fondo para el Bienestar y el Avance de las Mujeres)': '#489f3b'    # Verde para FOBAM
                 })

# Crear el gráfico de barras con la leyenda compartida para todos los recursos
fig_bar = px.bar(df_monitoreo,
                 x=['EJECUTADO', 'POR EJECUTAR'],  # 'EJECUTADO' es el avance y 'POR EJECUTAR' es el resto
                 y='PROGRAMA',  # Cada barra será para un programa
                 orientation='h',  # Barras horizontales
                 barmode='stack',  # Barras apiladas
                 title="MONITOREO DE PRESUPUESTO DE RECURSOS",
                 labels={'value': 'Monto', 'PROGRAMA': 'Programa'},
                 hover_data={'PROGRAMA': True},  # Solo mostrar el programa en el hover
                 color='PROGRAMA',  # Usar 'PROGRAMA' como base para color
                 color_discrete_map={  # Colores personalizados
                     'PAIMEF': '#c72c18',     # Naranja para PAIMEF
                     'PROABIM': '#643ee6',    # Morado para PROABIM
                     'FOBAM': '#489f3b'        # Verde para FOBAM
                 })

# Ajuste en el hover: queremos que en el hover se muestre el nombre del programa y la descripción correspondiente
fig_bar.update_traces(
    hovertemplate='%{y}<br>%{x}',
    customdata=df_monitoreo[['DESCRIPCIÓN RECURSOS HUMANOS', 'DESCRIPCIÓN RECURSOS MATERIALES', 'DESCRIPCIÓN METAS DEL PROYECTO']].values
)

# Crear el gráfico de barras apiladas 3D para el número de servicios
fig_servicios = go.Figure()

# Servicios
servicios_columns = ['TRABAJO SOCIAL', 'PSICOLOGÍA', 'JURÍDICO', 'PSICOLOGÍA INFANTIL', 'OTRO', 'TANATOLOGÍA']
centros = df_servicios['CENTRO DE ATENCIÓN EXTERNA'].unique()

colores_servicios = {
    'TANATOLOGÍA': '#d92714',
    'OTRO': '#fdb184',
    'PSICOLOGÍA INFANTIL': '#fe2a18',
    'JURÍDICO': '#770b05',
    'PSICOLOGÍA': '#ea7757',
    'TRABAJO SOCIAL': '#fd1005'
}

# Apilar las barras para cada centro de atención
for servicio in servicios_columns:
    fig_servicios.add_trace(go.Bar(
        x=df_servicios['CENTRO DE ATENCIÓN EXTERNA'],
        y=df_servicios[servicio],
        name=servicio,
        marker=dict(color=colores_servicios[servicio]),
    ))

fig_servicios.update_layout(
    barmode='stack',
    title="Número de Servicios Brindados 2023",
    scene=dict(
        xaxis=dict(title='Centros de Atención'),
        yaxis=dict(title='Número de Servicios'),
        zaxis=dict(title='Servicios'),
    ),
    height=600
)

# Cargar los datos de MUJERES
df_mujeres = pd.read_excel('DATA IMM MORELOS.xlsx', sheet_name='MUJERES')

# Limpiar los nombres de las columnas
df_mujeres.columns = ['Centro', 'Mujeres']

# Extraer los números de "MUJERES ATENDIDAS" o "MUJERES ALCANZADAS"
df_mujeres['Mujeres'] = df_mujeres['Mujeres'].str.extract('(\d+)').astype(float)

# Filtrar las filas relevantes (Centros de Atención, Línea Segura y Unidad Móvil)
centros_atencion_externa = df_mujeres[df_mujeres['Centro'].str.contains('Centro de Atención Externa')]
linea_segura = df_mujeres[df_mujeres['Centro'] == 'Línea Segura']
unidad_movil = df_mujeres[df_mujeres['Centro'] == 'Unidad Móvil']
centros_para_desarrollo_mujeres = df_mujeres[df_mujeres['Centro'].str.contains('Centro para el Desarrollo de las Mujeres')]

# Concatenar los DataFrames
df_final = pd.concat([centros_atencion_externa, linea_segura, unidad_movil, centros_para_desarrollo_mujeres])

# Asignar tipo de centro para diferenciarlos
df_final['Tipo'] = df_final['Centro'].apply(
    lambda x: 'Centro de Atención Externa' if 'Centro de Atención Externa' in x else
              'Línea Segura' if x == 'Línea Segura' else
              'Unidad Móvil' if x == 'Unidad Móvil' else
              'Centro para el Desarrollo de las Mujeres'
)

# Colores personalizados para los tipos de centro
color_map_mujeres = {
    'Centro de Atención Externa': '#f9200d',
    'Línea Segura': '#f9200d',
    'Unidad Móvil': '#f9200d',
    'Centro para el Desarrollo de las Mujeres': '#3d1fde'
}

# Crear el gráfico de barras de mujeres atendidas
fig_mujeres = px.bar(df_final,
                     x='Centro',
                     y='Mujeres',
                     color='Tipo',
                     color_discrete_map=color_map_mujeres,
                     title="Mujeres Atendidas y Alcanzadas por Centro de Atención",
                     labels={'Centro': 'Centro de Atención', 'Mujeres': 'Número de Mujeres'},
                     hover_data={'Tipo': True, 'Mujeres': True})

# Coordenadas para el límite de Morelos en formato decimal (ya convertidas)
morelos_boundary = [
    [19.13167, -99.49444], [19.13167, -98.63306], [18.3325, -98.63306], [18.3325, -99.49444],
    [19.13167, -99.49444]  # Coordenadas que cierran el polígono
]

# Crear un mapa de dispersión con las coordenadas de latitud y longitud
fig_map = go.Figure(go.Scattermapbox(
    lat=df_georef['LATITUD'],
    lon=df_georef['LONGITUD'],
    mode='markers',
    marker=dict(
        size=10,
        color=['#c72c18' if 'Centro de Atención Externa' in x or 'Centro de Justicia para las Mujeres' in x else '#3d1fde' for x in df_georef['CENTRO']],  # Colores personalizados
        opacity=0.7
    ),
    text=df_georef.apply(lambda row: f"<b>Centro:</b> {row['CENTRO']}<br><b>Municipio:</b> {row['MUNICIPIO']}<br><b>Descripción de Servicios:</b> {row['DESCRIPCIÓN DE SERVICIOS']}<br><b>Dirección:</b> {row['DIRECCIÓN']}<br><b>Servicios Profesionales:</b> {row['SERVICIOS PROFESIONALES']}<br><b>Subsidio Federal:</b> {row['SUBSIDIO FEDERAL']}", axis=1),  # Crear el hover
    hovertemplate='%{text}<extra></extra>'  # El hover se verá más vertical
))

# Agregar el límite de Morelos como un polígono morado
fig_map.add_trace(go.Scattermapbox(
    fill='toself',  # Rellenar el área del polígono
    fillcolor='rgba(61, 31, 222, 0.2)',  # Color de relleno con opacidad
    line=dict(color='#3d1fde', width=3),  # Color del borde morado
    lat=[point[0] for point in morelos_boundary],
    lon=[point[1] for point in morelos_boundary],
    name='Límite de Morelos'
))

# Actualizar layout del mapa para hacer zoom inicial en Morelos
fig_map.update_layout(
    mapbox_style="carto-positron",
    mapbox_zoom=8,  # Ajustar el zoom para que se vea todo Morelos
    mapbox_center={"lat": 18.7032, "lon": -99.2762},  # Centro de Morelos
    title="Mapa de Georreferenciación de Servicios",
    showlegend=False,
    height=700
)

# Colores personalizados para los tipos de violencia, usando tonos naranjas y rojizos
color_map_tipo = {
    'LÍNEA SEGURA': '#D32F2F',  # Rojo intenso
    'ÚNIDAD MÓVIL': '#F57C00',       # Naranja brillante
    'CAE JONACATEPEC': '#FF9800',    # Naranja cálido
    'CAE HUEYAPAN ': '#FF5722',       # Naranja rojizo
    'CAE XOCHITEPEC': '#E64A19',   # Rojo anaranjado
    'CAE EMILIANO ZAPATA': '#D84315',      # Rojo cálido
    'CAE TEMIXCO': '#F4511E',  # Naranja fuerte
    'CAE TETECALA': '#FF7043',   # Naranja claro
    'CJM CUERNAVACA': '#E53935', # Rojo suave
    'CJM YAUTEPEC': '#C62828',      # Rojo oscuro
    'CAE CUERNAVACA ': '#D32F2F', # Rojo intenso
    'CAE YECAPIXTLA': '#B71C1C',
    'CAE AYALA':'#9c1d10',
    'CAE JIUTEPEC': '#f8230f'
}

# Crear gráfico bidireccional con barras horizontales
fig_violencia_barras = px.bar(df_long_violencia,
                              y='MODALIDAD',
                              x='NUMERO_DE_VIOLENCIA',
                              color='TIPO',
                              orientation='h',  # Establecer el gráfico como horizontal
                              title="MODALIDAD Y TIPO DE VIOLENCIAS EN MUNICIPIOS",
                              labels={'NUMERO_DE_VIOLENCIA': 'Número de Casos', 'MODALIDAD': 'Modalidad de Violencia'},
                              color_discrete_map=color_map_tipo,
                              hover_data={'NUMERO_DE_VIOLENCIA': True, 'TIPO': True})

# Inicializar la aplicación Dash
app = dash.Dash(__name__)

styles = {
    'backgroundColor': '#FFE5D9',  # Fondo rojizo claro
    'fontFamily': 'Montserrat Light, Arial, sans-serif',  # Fuente Montserrat Light
    'color': '#8B0000',  # Color de texto rojizo oscuro
    'padding': '20px'
}

title_style = {
    'textAlign': 'center',
    'fontFamily': 'Montserrat Light, Arial, sans-serif',
    'color': '#FF4500',  # Color naranja rojizo
    'fontWeight': 'bold',
    'fontSize': '36px',
    'textShadow': '2px 2px 4px rgba(0, 0, 0, 0.3)',  # Sombra para el texto
    'background': 'linear-gradient(90deg, #FF4500, #8B0000)',  # Fondo degradado
    'WebkitBackgroundClip': 'text',
    'WebkitTextFillColor': 'transparent'
}





app.layout = html.Div([
    html.Div([
        html.H1("PLATAFORMA DE MONITOREO DE RECURSOS FEDERALES DEL INSTITUTO DE LA MUJER PARA EL ESTADO DE MORELOS", style=title_style),
        html.P("Indicadores de gasto y de resultados de los recursos federales transferidos por la Comisión Nacional para Prevenir y Erradicar la Violencia contra las Mujeres y el Instituto Nacional de las Mujeres.",
               style={'textAlign': 'center', 'fontFamily': 'Montserrat Light, Arial, sans-serif', 'color': '#8B0000', 'fontStyle': 'italic', 'fontSize': '16px', 'marginTop': '10px'})
    ], style={'marginBottom': '40px'}), # Título centrado y margen inferior para separación


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
        html.P("Elaboración con datos del Informe de Cierre del PROABIM, el FOBAM y el PAIMEF del ejercicio fiscal 2023", style={'textAlign': 'center', 'font-family': 'Arial, sans-serif', 'color': '#333333', 'marginTop': '40px'}),
        html.P("ELABORADO POR LIC.C.POL. EDUARDO CABRERA GUTIÉRREZ.", style={'textAlign': 'center', 'font-family': 'Arial, sans-serif', 'color': '#333333', 'marginTop': '40px'}),
        html.P("CORREO: CABARDO.GUTZ@GMAIL.COM", style={'textAlign': 'center', 'font-family': 'Arial, sans-serif', 'color': '#333333'})
    ], style={'marginTop': '20px'})
    ], style=styles)

# Callback para actualizar el gráfico de barras según la selección del menú desplegable
@app.callback(
    Output('grafico-barras', 'figure'),
    [Input('recurso-dropdown', 'value')]
)
def actualizar_grafico_barras(rubro_seleccionado):
    # Filtrar el DataFrame según el rubro seleccionado
    df_filtrado = df_monitoreo[['PROGRAMA', rubro_seleccionado]]
    df_filtrado = df_filtrado.sort_values(rubro_seleccionado, ascending=False)

    # Crear el gráfico de barras actualizado
    fig_bar = px.bar(df_filtrado,
                     x=rubro_seleccionado,
                     y='PROGRAMA',
                     orientation='h',
                     title="Avance por Programa Federal",
                     labels={'value': 'Monto', 'PROGRAMA': 'Programa'},
                     hover_data={'PROGRAMA': True},
                     color='PROGRAMA',
                     color_discrete_map={
                         'PAIMEF': '#c72c18',
                         'PROABIM': '#643ee6',
                         'FOBAM': '#489f3b'
                     })

    fig_bar.update_traces(
        hovertemplate='%{y}<br>%{x}',
        customdata=df_monitoreo[['DESCRIPCIÓN RECURSOS HUMANOS', 'DESCRIPCIÓN RECURSOS MATERIALES', 'DESCRIPCIÓN METAS DEL PROYECTO']].values
    )

    return fig_bar
    
server = app.server

# Ejecutar la aplicación
if __name__ == '__main__':
    app.run_server(debug=True)

