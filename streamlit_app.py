import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import altair as alt
import plotly.express as px
# from millify import millify

# configuración página
st.set_page_config(
    page_title="RCD 2022",
    page_icon="🏂",
    layout="wide",
    initial_sidebar_state="expanded")

alt.themes.enable("dark")
ruta = './data/indicadores_por_AA.xlsx'
ruta_gestores = './datos/Base de datos final_v2_maria_paula.xlsx'
df = pd.read_excel(ruta, usecols=lambda column: column != 'Unnamed: 0')
cantidad_autoridades_ambientales = df.shape[0]
# df_gestores = pd.read_excel(ruta_gestores, 
#                             usecols=lambda column: column!= 'Unnamed: 0',
#                             sheet_name='gestores')
# df_coord_gestores = df_gestores[['latitude', 'longitude']]

### título
titulo = '<p style="font-family:sans-serif; color:Green; font-size: 24px;'
titulo += 'text-align: center">'
titulo += 'Residuos de Construcción y Demolición (RCD) reportados por las '
titulo += 'Autoridades Ambientales - 2022</p>'
st.markdown(titulo, unsafe_allow_html=True)
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

with st.sidebar:
    st.title('RCD en Colombia para el año 2022')
    autoridad_ambiental_lista = list(df['Autoridad Ambiental'].unique())
    selected_autoridades = st.multiselect('Selecciona una Autoridad Ambiental',
                   autoridad_ambiental_lista,
                   )
# with st.sidebar:
#     selected = option_menu("RCD", ["RCD 2022", "mapa de gestores"],
#                            icons = ['house', 'globe-americas'], menu_icon = 'cast',
#                            default_index = 1)
#     selected
### Mapeo de gestores
# st.dataframe(df_coord_gestores)
# st.map(df_coord_gestores, 
#        latitude = 'latitude',
#        longitude = 'longitude')
### Datos Autoridades Ambientales RCD 2022
## gráfico meta de aprovechamiento
df_meta_aprov = df[['Autoridad Ambiental', 'meta_de_aprovechamiento']]
if len(selected_autoridades) > 0:
    df = df[df['Autoridad Ambiental'].isin(selected_autoridades)]

# st.dataframe(df)
### 
# Seleccionando columnas
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
media_meta_aprov = df['meta_de_aprovechamiento'].mean()
# rcd_generado = millify(df['RCD Generado'].sum())
rcd_generado = round(df['RCD Generado'].sum(), 1)
# rcd_dispo_final = millify(df['RCD enviado a Disposición Final'].sum())
rcd_dispo_final = round(df['RCD enviado a Disposición Final'].sum(), 1)
label_meta_aprov = "Promedio de las metas de aprovechamiento: "

# Create an indicator for each row in the DataFrame
col_1, col_2, col_3 = st.columns(3)
if df.shape[0] == cantidad_autoridades_ambientales:
    with col_1:
        label_meta_aprov = "Promedio de las metas de aprovechamiento"
        st.metric(label = label_meta_aprov,
                value = f"{media_meta_aprov * 100:.1f}%",
                delta='Excluyendo material de excavación',
                delta_color='inverse')
    with col_2:
        label_gen = 'Total de RCD generado'
        st.metric(label = label_gen,
                value = f"{rcd_generado:,.0f}",
                delta='Toneladas')
    with col_3:
        label_dispo_final = 'Total de RCD enviado a Disposición Final'
        st.metric(label = label_dispo_final, 
                  value = f'{rcd_dispo_final:,.0f}',
                  delta='Toneladas',
                  delta_color='normal')
else:
    for i, row in df.iterrows():
        with col_1:
            label_meta_aprov = "Meta de aprovechamiento: "
            st.metric(label= label_meta_aprov + f"{row['Autoridad Ambiental']}",
                    value=f"{row['meta_de_aprovechamiento'] * 100:.1f}%",
                    delta='Excluyendo material de excavación',
                    delta_color='inverse')
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