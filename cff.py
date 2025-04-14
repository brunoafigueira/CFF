import streamlit as st
import pandas as pd
import gdown
import re

# Configuração da página
st.set_page_config(page_title="Visualizador por Posição", layout="wide")

# CSS personalizado
st.markdown("""
<style>
    .vertical-center {
        display: flex;
        align-items: center;
        height: 100%;
    }
</style>
""", unsafe_allow_html=True)

# Layout
col1, col2 = st.columns([1, 4])
with col1:
    st.markdown('<div class="vertical-center">', unsafe_allow_html=True)
    st.image("logocff.svg", width=200)
    st.markdown('</div>', unsafe_allow_html=True)
    
with col2:
    st.markdown('<div class="vertical-center">', unsafe_allow_html=True)
    st.title("📊 Visualizador por Posição de Coluna")
    st.markdown('</div>', unsafe_allow_html=True)

# LINK DO GOOGLE DRIVE (substitua abaixo pelo seu)
GOOGLE_DRIVE_LINK = "https://docs.google.com/spreadsheets/d/1wFo7MDo0NAQA4VZ6t-aIeHDzEnIllRiN/edit?usp=drive_link&ouid=113558481846573208134&rtpof=true&sd=true"

# Extrair ID do link
file_id = re.search(r'/d/(.*?)/', GOOGLE_DRIVE_LINK).group(1)
url_download = f"https://drive.google.com/uc?id={file_id}"
CAMINHO_ARQUIVO = "a_temp.xlsx"

try:
    gdown.download(url_download, CAMINHO_ARQUIVO, quiet=False)
    df = pd.read_excel(CAMINHO_ARQUIVO, engine='openpyxl')
    
    posicoes_colunas = [0, 2, 3]
    df_selecionado = df.iloc[:, posicoes_colunas]

    st.dataframe(
        df_selecionado,
        height=600,
        use_container_width=True,
        hide_index=True,
        column_config={
            str(col): st.column_config.Column(f"Coluna {idx+1}")
            for idx, col in enumerate(df_selecionado.columns)
        }
    )

except Exception as e:
    st.error(f"Erro ao carregar o arquivo: {str(e)}")
