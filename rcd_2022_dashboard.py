import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
# configuración página
st.set_page_config(
    page_title="RCD 2022",
    page_icon="🏂",
    layout="wide",
    initial_sidebar_state="expanded")

alt.themes.enable("dark")
ruta = './data/indicadores_por_AA.xlsx'
df = pd.read_excel(ruta, usecols=lambda column: column != 'Unnamed: 0')
### 
# Seleccionando columnas
columnas = ['autoridad_ambiental', 
            'indicador_cantidad_rcd_generado',
            'indicador_cantidad_de_rcd_aprovechado', 
            'indicador_cantidad_de_rcd_disposicion_final',
            'total_material_punto_limpio_con_1_1',
            'total_planta_de_aprovechamiento_con_1_1', 
            'total_receptor_con_1_1', 
            'total_generado_reportado',  
            ]
df = df[columnas]
df.rename(columns = {
    'autoridad_ambiental': 'Autoridad Ambiental',
    'indicador_cantidad_rcd_generado': 'RCD Generado',
    'indicador_cantidad_de_rcd_aprovechado': 'RCD Aprovechado',
    'indicador_cantidad_de_rcd_disposicion_final': 'RCD a Disposición Final',
    'total_material_punto_limpio_con_1_1': 'RCD a Punto Limpio',
    'total_planta_de_aprovechamiento_con_1_1': 'RCD a Planta de Aprovechamiento',
    'total_receptor_con_1_1': 'RCD a Receptor',
    'total_generado_reportado': 'RCD Generado Reportado',
    }, inplace = True
)
### título
titulo = '<p style="font-family:sans-serif; color:Green; font-size: 24px;'
titulo += 'text-align: center">'
titulo += 'Residuos de Construcción y Demolición (RCD) reportados por las '
titulo += 'Autoridades Ambientales - 2022</p>'
st.markdown(titulo, unsafe_allow_html=True)
# Crear sidebar para seleccionar una autoridad ambiental
with st.sidebar:
    st.title('RCD en Colombia para el año 2022')
    autoridad_ambiental_lista = list(df['Autoridad Ambiental'].unique())
    selected_autoridades = st.multiselect('Selecciona una Autoridad Ambiental',
                   autoridad_ambiental_lista,
                   )
# st.write(selected_autoridades)
if len(selected_autoridades) > 0:
    df = df[df['Autoridad Ambiental'].isin(selected_autoridades)]
    # st.dataframe(df)
### 
# Melt the DataFrame to a long format
df_melted = df.melt(id_vars='Autoridad Ambiental', 
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
