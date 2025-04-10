import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import rasterio
import numpy as np
import geopandas as gpd
from shapely.geometry import Point
import os

st.set_page_config(
    layout='wide',
    page_title='Datas Centers'
)

st.markdown("""
    <style>
        .hover-box {
            background-color: white;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 10px;
            transition: all 0.3s ease;
            cursor: pointer;
        }

        .hover-box h4,
        .hover-box p {
            color: #1a1a1a; /* Cor escura padrão */
            transition: color 0.3s ease;
        }

        .hover-box:hover {
            background-color: #082C4F;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
            transform: translateY(-3px);
        }

        .hover-box:hover h4,
        .hover-box:hover p {
            color: white; /* Muda para branco no hover */
        }

        .stApp {
            background-color: #D3D9E2;
        }

        section[data-testid="stSidebar"] {
            background-color: #082C4F;
            color: white;
        }

        section[data-testid="stSidebar"] hr {
            border: none;
            height: 2px;
            background-color: #FFFFFF;
            margin-top: 20px;
            margin-bottom: 20px;
        }

        section[data-testid="stSidebar"] h1,
        section[data-testid="stSidebar"] h2,
        section[data-testid="stSidebar"] h3,
        section[data-testid="stSidebar"] h4,
        section[data-testid="stSidebar"] h5,
        section[data-testid="stSidebar"] h6 {
            color: white;
            font-family: 'Segoe UI', sans-serif;
            margin-top: 20px;
        }

        section[data-testid="stSidebar"] p,
        section[data-testid="stSidebar"] label,
        section[data-testid="stSidebar"] span {
            color: #F0F0F0;
            font-size: 16px;
        }

        section[data-testid="stSidebar"] .stRadio,
        section[data-testid="stSidebar"] .stCheckbox {
            padding-top: 8px;
            padding-bottom: 8px;
        }

        div[role="radiogroup"] > label[data-baseweb="radio"] {
            color: white;
        }

        div[role="radiogroup"] > label[data-baseweb="radio"] span {
            color: white !important;
        }

        div[role="checkbox"] label {
            color: white !important;
        }
        
        section[data-testid="stSidebar"] > div {
            margin-bottom: 20px;
        }
                .small-box {
            padding: 10px;
            font-size: 16px;
        }
        .small-box h4 {
            font-size: 18px;
        }
        .small-box p {
            font-size: 16px;
        }
        /* Latitude */
        [data-testid="stTextInput"][data-baseweb="input"] > div:has(input[id*="lat_input"]) input {
            width: 120px !important;
            height: 30px !important;
            font-size: 14px !important;
            background: red !important;
        }

        /* Longitude */
        [data-testid="stTextInput"][data-baseweb="input"] > div:has(input[id*="lon_input"]) input {
            width: 120px !important;
            height: 30px !important;
            font-size: 14px !important;
        }
        img {
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
            border-radius: 12px;
        }
    </style>
    """, unsafe_allow_html=True)


st.title('DashBoard Datas Centers')

st.markdown("""
<style>
.big-font {
    font-size:25px !important;
    color: white;
}
</style>
""", unsafe_allow_html=True)
st.markdown('<p class =="big-font"> Texto Raniere ! </p>',unsafe_allow_html=True)
st.divider()

if "show_inputs" not in st.session_state:
    st.session_state.show_inputs = True

# Leitura dos dados
df = pd.read_csv("Planilha_Plataforma.csv")
dfr = pd.read_csv("Planilha_regioes.csv")
municipios= gpd.read_file(".\BR_Municipios_2023\BR_Municipios_2023.shp")

# Sidebar - Opções de visualização
st.sidebar.subheader('Escolha qual mapa deseja visualizar:')
opcao = st.sidebar.radio("Qual mapa você deseja visualizar?", ["Brasil", "Região", "Estado"])

if opcao == "Estado": 
    st.sidebar.subheader('Escolha qual estado deseja visualizar:')
    df_estados = df[df['SIGLA'] != 'BR']
    estados = df_estados['LOCALIZAÇÃO'].value_counts().index
    estado = st.sidebar.selectbox('Estado', estados)
    df_filtered = df[df['LOCALIZAÇÃO'] == estado]

elif opcao == "Região":
    st.sidebar.subheader('Escolha qual Região deseja visualizar:')
    regioes = dfr['REGIÃO'].value_counts().index
    regiao = st.sidebar.selectbox('Região', regioes)
    dfr_filtered2 = dfr[dfr['REGIÃO'] == regiao]

st.sidebar.divider()

st.sidebar.subheader('Escolha os cenários:')
mostrar = st.sidebar.radio("Qual cenário você deseja visualizar?", ["Cenário 1", "Cenário 2", "Cenário 3"])

st.sidebar.divider()

col1, col2, col3 = st.columns([5, 5, 5])

# Informações principais
if opcao == "Brasil":
    area_disp = df.loc[df['SIGLA'] == 'BR', 'AREA_DISP'].values[0]
    area_disp_20 = df.loc[df['SIGLA'] == 'BR', 'AREA_M5'].values[0]
    restricoes = df.loc[df['SIGLA'] == 'BR', 'AREA_REST'].values[0]
elif opcao == "Estado" and estado:
    df_estado = df[df['LOCALIZAÇÃO'] == estado]
    area_disp = df_estado['AREA_DISP'].values[0]
    area_disp_20 = df_estado['AREA_M5'].values[0]
    restricoes = df_estado['AREA_REST'].values[0]
elif opcao == "Região" and regiao:
    dfr_regiao = dfr[dfr['REGIÃO'] == regiao]
    area_disp = dfr_regiao['AREA_DISP_1'].values[0]
    area_disp_20 = dfr_regiao['AREA_M5_1'].values[0]
    restricoes = dfr_regiao['AREA_REST_1'].values[0]

with col1:
    st.markdown(f"""
        <div class="hover-box">
            <h4>Área Disponível</h4>
            <p style="font-size:22px;">{area_disp} km²</p>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
        <div class="hover-box">
            <h4>Área Disponível com a nota maior 5</h4>
            <p style="font-size:22px;">{area_disp_20} km²</p>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
        <div class="hover-box">
            <h4>Restrições</h4>
            <p style="font-size:22px;">{restricoes} km²</p>
        </div>
    """, unsafe_allow_html=True)
# Bloco para gráficos e imagem com 2 colunas
st.divider()
g1, g2 = st.columns([2, 1.3])
l1, l2, l3 = st.columns([2, 10, 2])
with g1:
    if opcao == "Brasil":
        IMAGEM_3 = df.loc[df['SIGLA'] == 'BR', 'IMG_JPEG'].values[0]
        st.image(f".\\mapas\\{IMAGEM_3}.jpeg", caption='Mapa do Brasil')
with l2:        
    if opcao == "Estado" and estado:
        IMAGEM = df_filtered['IMG_JPEG'].values[0]
        st.image(f".\\mapas\\{IMAGEM}.jpeg", caption=f'Mapa do {estado}')
with g1:
    if opcao == "Região" and regiao:
        IMAGEM_2 = dfr_filtered2['IMG_JPEG_1'].values[0]
        st.image(f".\\REGIOES\\{IMAGEM_2}.jpeg", caption=f'Região {regiao}')

with g2:
    if opcao == "Brasil":
        df['NOTA_MEDIA'] = df['NOTA_MEDIA'].str.replace(',', '.').astype(float)
        df_estados = df[df['SIGLA'] != 'BR']
        df_grouped = df_estados.sort_values(by='NOTA_MEDIA', ascending=False)

        plt.figure(figsize=(8, 3))
        plt.bar(df_grouped['SIGLA'], df_grouped['NOTA_MEDIA'], color='#082C4F')
        plt.xlabel('Estado')
        plt.ylabel('Nota Média')
        plt.title('Nota Média por Estado')
        st.pyplot(plt)

        with rasterio.open(".\\nota_5\\nota_5.tif") as dataset:
            band = dataset.read(1)
            nodata_value = dataset.nodata
            if nodata_value is not None:
                band = band[band != nodata_value]
            
            plt.figure(figsize=(8, 4.5))
            plt.hist(band.flatten(), bins=30, color="#1A4466", edgecolor="white", alpha=1)
            plt.xlabel("Nota por Km²")
            plt.ylabel("Frequência")
            plt.title("Histograma dos Pixels do Raster")
            plt.grid(True, alpha= 0.4)
            st.pyplot(plt)
        with g1:
            lat_col, lon_col = st.columns(2)  # Latitude e Longitude lado a lado
            with lat_col:
                latitude_str = st.text_input("Latitude", placeholder="Ex: -23.5505", key="teste")
            with lon_col:
                longitude_str = st.text_input("Longitude", placeholder="Ex: -46.6333")

                def get_pixel_value(lat, lon, raster_path=".\\nota_5\\NotaFinal.tif"):
                    with rasterio.open(raster_path) as dataset:
                        try:
                            row, col = dataset.index(float(lon), float(lat))
                            value = dataset.read(1)[row, col]
                            return value
                        except:
                            return "Coordenadas fora da área do raster"

        # Se os campos estiverem preenchidos, mostra as caixas abaixo
        with g1:
            if latitude_str and longitude_str:
                try:
                    nota_pixel = get_pixel_value(latitude_str, longitude_str)
                    latitude = float(latitude_str)
                    longitude = float(longitude_str)

                    ponto = gpd.GeoDataFrame(geometry=[Point(longitude, latitude)], crs="EPSG:4326")
                    municipio_info = gpd.sjoin(ponto, municipios, how="left", predicate="within")

                    if municipio_info.empty:
                        st.warning("Coordenada fora de qualquer município!")
                    else:
                        nome_municipio = municipio_info.iloc[0].get("NM_MUN", "Desconhecido")
                        uf = municipio_info.iloc[0].get("NM_UF", "Desconhecido")

                    # Caixas aparecem abaixo dos campos
                    l1, l2, l3 = st.columns([1, 1, 1])
                    with l1:
                        st.markdown(f"""
                            <div class="hover-box small-box">
                                <h4>Nota</h4>
                                <p>{nota_pixel:.2f}</p>
                            </div>
                        """, unsafe_allow_html=True)
                    with l2:
                        st.markdown(f"""
                            <div class="hover-box small-box">
                                <h4>Estado</h4>
                                <p>{uf}</p>
                            </div>
                        """, unsafe_allow_html=True)
                    with l3:
                        st.markdown(f"""
                            <div class="hover-box small-box">
                                <h4>Município</h4>
                                <p>{nome_municipio}</p>
                            </div>
                        """, unsafe_allow_html=True)

                except ValueError:
                    st.error("Latitude e longitude devem ser números válidos.")

    elif opcao == "Região" and regiao:
        df['NOTA_MEDIA'] = df['NOTA_MEDIA'].str.replace(',', '.').astype(float)
        estados_na_regiao = df[df['REGIÕES'] == regiao]
        estados_ordenados = estados_na_regiao.sort_values(by='NOTA_MEDIA', ascending=False)
        plt.figure(figsize=(8, 3))
        plt.bar(estados_ordenados['SIGLA'], estados_ordenados['NOTA_MEDIA'], color='#082C4F')
        plt.xlabel('Estado')
        plt.ylabel('Nota Média')
        plt.title(f'Nota Média por Estado - Região {regiao}')
        st.pyplot(plt)

st.divider()
st.subheader('Calculadora de Viabiliade')