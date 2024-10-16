import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import altair as alt
import plotly.express as px
import pydeck as pdk
# from millify import millify

# configuración página
st.set_page_config(
    page_title="RCD 2022",
    page_icon="🏂",
    layout="wide",
    initial_sidebar_state="expanded")

alt.themes.enable("dark")
ruta = './data/indicadores_por_AA.xlsx'
ruta_gestores = './data/gestores_coordenadas.csv'
df = pd.read_excel(ruta, usecols=lambda column: column != 'Unnamed: 0')
cantidad_autoridades_ambientales = df.shape[0]
df_gestores = pd.read_csv(ruta_gestores, 
                            usecols=lambda column: column!= 'Unnamed: 0',
                            sep = ',')
# st.dataframe(df_gestores)
# st.write(df_gestores.columns)
df_coord_gestores = df_gestores[['latitude', 'longitude']]
# st.dataframe(df_coord_gestores)
### título
titulo = '<p style="font-family:sans-serif; color:Green; font-size: 24px;'
titulo += 'text-align: center">'
titulo += 'Residuos de Construcción y Demolición (RCD) reportados por las '
titulo += 'Autoridades Ambientales - 2022</p>'

ruta_logo = './images/logo_minambiente.png'
st.logo(ruta_logo, size = 'medium')

col_titulo_1, col_titulo_2 = st.columns([0.2, 0.8])
with col_titulo_1:
    st.image(ruta_logo)
with col_titulo_2:
    st.markdown(titulo, unsafe_allow_html=True)
warning = 'Los datos presentados hasta el momento corresponden a una primera versión '
warning += 'de la información revisada hasta el 20 de junio del 2024. '
warning += 'Si hay alguna incongruencia puede deberse a la calidad de los datos o '
warning += 'a que la información no está actualizada. '
warning += 'Se generarán distintas versiones de la información con el fin de mitigar '
warning += 'dichas incogruencias o con el fin de proporcionar información más clara.'
st.warning(warning, icon="⚠️")
## Menú
menu = option_menu(None, ["RCD 2022", "Mapa de gestores"],
                   icons = ['house', 'geo-alt-fill'],
                   menu_icon = 'cast',
                   default_index=0,
                   orientation='horizontal')
menu
# Crear sidebar para seleccionar una autoridad ambiental
df.rename(columns = {
    'autoridad_ambiental': 'Autoridad Ambiental',
    'indicador_cantidad_rcd_generado': 'RCD Generado',
    'total_aprovechado_en_obra_con_1_1' : 'RCD Aprovechado en Obra',
    'total_planta_de_aprovechamiento_con_1_1': 'RCD enviado a Planta de Aprovechamiento',
    'indicador_cantidad_de_rcd_disposicion_final': 'RCD enviado a Disposición Final',
    'total_material_punto_limpio_con_1_1': 'RCD enviado a Punto Limpio',
    'total_receptor_con_1_1': 'RCD enviado a Receptor',
    # 'total_generado_reportado': 'RCD Generado Reportado',
    }, inplace = True
)

if menu == "RCD 2022":
    

    with st.sidebar:
        st.title('RCD en Colombia para el año 2022')
        autoridad_ambiental_lista = list(df['Autoridad Ambiental'].unique())
        selected_autoridades = st.multiselect('Selecciona una Autoridad Ambiental',
                    autoridad_ambiental_lista,
                    )
    df_meta_aprov = df[['Autoridad Ambiental', 'meta_de_aprovechamiento']]
    if len(selected_autoridades) > 0:
        df = df[df['Autoridad Ambiental'].isin(selected_autoridades)]

    columnas = ['Autoridad Ambiental', 
            'RCD Generado',
            # 'indicador_cantidad_de_rcd_aprovechado', 
            'RCD Aprovechado en Obra',
            'RCD enviado a Disposición Final',
            'RCD enviado a Planta de Aprovechamiento', 
            'RCD enviado a Punto Limpio', 
            'RCD enviado a Receptor'  
            ]
    df_barplot = df[columnas]

        # st.dataframe(df)
    ### 
    # Melt the DataFrame to a long format
    df_melted = df_barplot.melt(id_vars='Autoridad Ambiental', 
                        var_name='Tipo de RCD', 
                        value_name='RCD en toneladas')

    # plotly
    fig = px.bar(df_melted, x = 'Autoridad Ambiental', y = 'RCD en toneladas',
                color = 'Tipo de RCD', barmode = 'group',
                width=800, height = 500
                )
    fig.update_layout(barmode = 'group', bargroupgap = 0.1, xaxis_tickangle = -45)
    fig.update_traces(width = 0.2)
    st.plotly_chart(fig)

    ### Gráfico de los indicadores
    # meta de aprovechamiento
    media_meta_aprov = df['meta_de_aprovechamiento'].mean()
    # rcd_generado = millify(df['RCD Generado'].sum())
    rcd_generado = round(df['RCD Generado'].sum(), 1)
    # rcd aprovechado en obra
    rcd_aprovechado_en_obra = round(df['RCD Aprovechado en Obra'].sum(), 1)
    # rcd a receptor
    rcd_receptor = round(df['RCD enviado a Receptor'].sum(), 1)
    # rcd a punto limpio
    rcd_punto_limpio = round(df['RCD enviado a Punto Limpio'].sum(), 1)
    # rcd a planta de aprovechamiento
    rcd_planta_aprov = round(df['RCD enviado a Planta de Aprovechamiento'].sum(), 1)
    label_meta_aprov = "Promedio de las metas de aprovechamiento: "
    rcd_dispo_final = round(df['RCD enviado a Disposición Final'].sum(), 1)

    # Create an indicator for each row in the DataFrame
    col_1, col_2, col_3 = st.columns(3)
    # col_1_1, col_2_1, col_3_1 = st.columns(3)
    if df.shape[0] == cantidad_autoridades_ambientales:

        with col_1:
            label_meta_aprov = "Promedio de las metas de aprovechamiento"
            st.metric(label = label_meta_aprov,
                    value = f"{media_meta_aprov * 100:.1f}%",
                    delta='Excluyendo material de excavación',
                    delta_color='inverse')
            label_planta_aprov = 'Total de RCD enviado a Planta de Aprovechamiento'
            st.metric(label = label_planta_aprov,
                    value = f"{rcd_planta_aprov:,.0f}")
            label_aprov_en_obra = 'Total de RCD Aprovechado en Obra'
            st.metric(label = label_aprov_en_obra,
                      value = f"{rcd_aprovechado_en_obra:,.0f}")

        with col_2:
            label_gen = 'Total de RCD generado'
            st.metric(label = label_gen,
                    value = f"{rcd_generado:,.0f}",
                    delta='Toneladas')
            label_receptor = 'Total de RCD enviado a Receptor'
            st.metric(label = label_receptor,
                    value = f"{rcd_receptor:,.0f}",
                    delta='Toneladas')
        with col_3:
            label_dispo_final = 'Total de RCD enviado a Disposición Final'
            st.metric(label = label_dispo_final, 
                    value = f'{rcd_dispo_final:,.0f}',
                    delta='Toneladas',
                    delta_color='normal')
            label_punto_limpio = 'Total de RCD enviado a Punto Limpio'
            st.metric(label = label_punto_limpio,
                    value = f"{rcd_punto_limpio:,.0f}",
                    delta='Toneladas')
    else:
        for i, row in df.iterrows():
            with col_1:
                label_meta_aprov = "Meta de aprovechamiento: "
                label_aprov_en_obra = "RCD Aprovechado en Obra: "
                st.metric(label= label_meta_aprov + f"{row['Autoridad Ambiental']}",
                        value=f"{row['meta_de_aprovechamiento'] * 100:.1f}%",
                        delta='Excluyendo material de excavación',
                        delta_color='inverse')
                rcd_aprov_en_obra = round(row['RCD Aprovechado en Obra'], 1)
                st.metric(label = label_aprov_en_obra + f"{row['Autoridad Ambiental']}",
                          value = f"{rcd_aprov_en_obra:,.0f}",
                          delta = 'Toneladas')
                
            with col_2:
                label_gen = "RCD generado: "
                # rcd_gen = millify(row['RCD Generado'])
                rcd_gen = round(row['RCD Generado'], 1)
                st.metric(label= label_gen + f"{row['Autoridad Ambiental']}",
                        value=f"{rcd_gen:,.0f}",
                        delta='Toneladas')
            with col_3:
                label_dispo_final = "RCD enviado a Disposición Final: "
                # rcd_dispo_final = millify(row['RCD enviado a Disposición Final'])
                rcd_dispo_final = round(row['RCD enviado a Disposición Final'], 0)
                st.metric(label=label_dispo_final + f"{row['Autoridad Ambiental']}",
                        value=f'{rcd_dispo_final:,.0f}',
                        delta='Toneladas',
                        delta_color='normal')
elif menu == "Mapa de gestores":

# with st.sidebar:
#     selected = option_menu("RCD", ["RCD 2022", "mapa de gestores"],
#                            icons = ['house', 'globe-americas'], menu_icon = 'cast',
#                            default_index = 1)
#     selected
### Mapeo de gestores
# st.dataframe(df_coord_gestores)
    layer = pdk.Layer(
        "ScatterplotLayer",
        data = df_gestores,
        id = "nomb",
        get_position = ["longitude", "latitude"],
        get_color="[12, 153, 7]",
        pickable = True,
        auto_highlight = True,
        get_radius = 3000,
    )
    # Set the view of the map
    view_state = pdk.ViewState(
        latitude=df_gestores['latitude'].mean(),
        longitude=df_gestores['longitude'].mean(),
        controller = True,
        zoom=5,
        pitch=10
    )
    # Renderizando el mapa
    texto_tooltip = "Nombre del gestor: {nomb}\n" 
    texto_tooltip += "Actividad de recolección y transporte: {recolec}\n"
    texto_tooltip += "Actividad de almacenamineto en punto limpio: {almac}\n"
    texto_tooltip += "Actividad de aprovechamiento: {aprovec}\n"
    texto_tooltip += "Actividad de disposición final: {finaldis}\n"
    texto_tooltip += "Autoridad Ambiental: {aa}\n"

    grafico = pdk.Deck(layers=[layer],
                initial_view_state=view_state,
                tooltip={'text':texto_tooltip},
                )

    evento = st.pydeck_chart(grafico, on_select="rerun", selection_mode='multi-object')
    evento.selection

# st.map(df_gestores[['latitude', 'longitude']], 
#        latitude = 'latitude',
#        longitude = 'longitude',
#        color = '#0c9907',
#        size = 200,
#        zoom = 4)
### Datos Autoridades Ambientales RCD 2022
## gráfico meta de aprovechamiento

# st.dataframe(df)
### 
# Seleccionando columnas

# plot_meta_aprov = alt.Chart(df_meta_aprov).mark_arc(innerRadius=45, cornerRadius=25).encode(
#       theta="meta_de_aprovechamiento",
#     #   color= alt.Color("Topic:N",
#     #                   scale=alt.Scale(
#     #                       #domain=['A', 'B'],
#     #                       domain=[input_text, ''],
#     #                       # range=['#29b5e8', '#155F7A']),  # 31333F
#     #                       range=chart_color),
#     #                   legend=None),
#   ).properties(width=130, height=130)

# st.altair_chart(plot_meta_aprov)