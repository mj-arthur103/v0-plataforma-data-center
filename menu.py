import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import rasterio
import numpy as np

#o page_config é para configurar a página o layout se vai ser grande ou n, nome da página,etc
st.set_page_config(
    layout='wide',
    page_title='Datas Centers'
)
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

#leitura do csv
df = pd.read_csv("Planilha_plataforma.csv")
dfr = pd.read_csv("Planilha_regioes.csv")

#df.set_index('SIGLA_1', inplace=True)#esse aqui seria para eu adicionar o eixo x ao gráfico

#Alternar entre o mapa de Região, Estado, Brasil
st.sidebar.subheader('Escolha qual mapa deseja visualizar:')
opcao = st.sidebar.radio("Qual mapa você deseja visualizar?", ["Brasil", "Região", "Estado"])

#Escolha de Estado
if opcao == "Estado": 
    st.sidebar.subheader('Escolha qual estado deseja visualizar:')
    df_estados= df[df['SIGLA'] != 'BR']
    estados=df_estados['LOCALIZAÇÃO'].value_counts().index
    estado=st.sidebar.selectbox('Estado',estados)
    df_filtered=df[df['LOCALIZAÇÃO']==estado]

#Escolha de Região
elif opcao == "Região":
    st.sidebar.subheader('Escolha qual Região deseja visualizar:')
    regioes=dfr['REGIÃO'].value_counts().index
    regiao=st.sidebar.selectbox('Região',regioes)
    dfr_filtered2=dfr[dfr['REGIÃO']==regiao]

st.sidebar.divider()

#Cenarios
st.sidebar.subheader('Escolha os cenarios:')
mostrar= st.sidebar.checkbox('Cenário 1')
mostrar_2= st.sidebar.checkbox('Cenário 2')
mostrar_3= st.sidebar.checkbox('Cenário 3')

st.sidebar.divider()

#Coordenadas
st.sidebar.subheader('Digite as coordenadas:')
latitude = st.sidebar.text_input("Latitude", placeholder="Ex: -23.5505")
longitude = st.sidebar.text_input("Longitude", placeholder="Ex: -46.6333")

# Layout principal
col1, col2= st.columns([3.2,3.1])

# Informações e gráficos
with col2:
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
        dfr_regiao= dfr[dfr['REGIÃO'] == regiao]
        area_disp = dfr_regiao['AREA_DISP_1'].values[0]
        area_disp_20 = dfr_regiao['AREA_M5_1'].values[0]
        restricoes = dfr_regiao['AREA_REST_1'].values[0]
    st.markdown(f"""
        <div style="background-color:#262730; padding:20px; border-radius:10px; margin-bottom:10px;">
            <h4 style="color:white;">Área Disponível</h4>
            <p style="color:white; font-size:22px;">{area_disp} km²</p>
        </div>
        <div style="background-color:#262730; padding:20px; border-radius:10px; margin-bottom:10px;">
            <h4 style="color:white;">Área Disponivel com a nota maior que 5</h4>
            <p style="color:white; font-size:22px;">{area_disp_20}km²</p>
        </div>
        <div style="background-color:#262730; padding:20px; border-radius:10px;">
            <h4 style="color:white;">Restrições</h4>
            <p style="color:white; font-size:22px;">{restricoes} km²</p>
        </div>
    """, unsafe_allow_html=True)

# Exibição automática do mapa com alternância
with col1:
    if opcao == "Brasil":
        IMAGEM_3 = df.loc[df['SIGLA'] == 'BR', 'IMG_JPEG'].values[0]
        st.image(f".\\mapas\\{IMAGEM_3}.jpeg")
        with col1:
            
            df['NOTA_MEDIA'] = df['NOTA_MEDIA'].str.replace(',', '.').astype(float)
            # Filtrando para remover a linha do Brasil
            df_estados = df[df['SIGLA'] != 'BR']
            df_grouped = df_estados.sort_values(by=['NOTA_MEDIA'], ascending=False)
            # Plotando o gráfico de barras
            plt.figure(figsize=(10,3))
            plt.bar(df_grouped['SIGLA'], (df_grouped['NOTA_MEDIA']), color='skyblue')
            plt.xlabel('Estado')
            plt.ylabel('Nota Média')
            plt.title('Nota Média por Estado')

            # Exibindo o gráfico no Streamlit
            st.pyplot(plt)
        with col2:
        # Caminho para o seu raster
            raster_path = (f".\\nota_5\\nota_5.tif")
        # Abrindo o raster
            with rasterio.open(raster_path) as dataset:
        # Lendo os dados do raster
                band = dataset.read(1)  # Lendo a primeira banda
        # Máscara para remover valores NoData
            nodata_value = dataset.nodata
            if nodata_value is not None:
                band = band[band != nodata_value]

            # Criando histograma
            plt.figure(figsize=(7, 3))
            plt.hist(band.flatten(), bins=30, color="blue", edgecolor="black", alpha=0.7)
            plt.xlabel("Nota por Km²")
            plt.ylabel("Frequência")
            plt.title("Histograma dos Pixels do Raster")
            plt.grid(True)

            # Exibir histograma
            st.pyplot(plt)
    elif opcao == "Estado" and estado:
        IMAGEM=df_filtered['IMG_JPEG'].values[0]
        st.image(f".\\mapas\\{IMAGEM}.jpeg", caption= f'Mapa do {estado}') 
    elif opcao == "Região" and regiao:
        IMAGEM_2=dfr_filtered2['IMG_JPEG_1'].values[0]
        st.image(f".\\REGIOES\\{IMAGEM_2}.jpeg", caption= f'Região {regiao}')
        with col1:
            df['NOTA_MEDIA'] = df['NOTA_MEDIA'].str.replace(',', '.').astype(float)

            # Filtrar os estados que pertencem à região selecionada
            estados_na_regiao = df[df['REGIÕES'] == regiao]

            # Ordenar do maior para o menor
            estados_ordenados = estados_na_regiao.sort_values(by='NOTA_MEDIA', ascending=False)

            # Criar gráfico de barras
            plt.figure(figsize=(10, 3))
            plt.bar(estados_ordenados['SIGLA'], estados_ordenados['NOTA_MEDIA'], color='skyblue')
            plt.xlabel('Estado')
            plt.ylabel('Nota Média')
            plt.title(f'Nota Média por Estado - Região {regiao}')

            # Exibir no Streamlit
            st.pyplot(plt)
st.divider()
st.subheader('Calculadora de Viabiliade')