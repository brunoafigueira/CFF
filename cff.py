import streamlit as st
import yaml
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth
import pandas as pd
import gdown
import re

# ======================================
# 1. CONFIGURAÇÃO DE AUTENTICAÇÃO
# ======================================
with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

# ======================================
# 2. PÁGINA DE LOGIN
# ======================================
name, authentication_status, username = authenticator.login(location='main')

if not authentication_status:
    st.stop()  # Impede o acesso ao resto do app se não autenticado

# ======================================
# 3. APLICATIVO PRINCIPAL (após login)
# ======================================
authenticator.logout('Logout', 'sidebar')
st.write(f'Bem-vindo *{name}*')

# --------------------------------------
# (Seu código original aqui)
# --------------------------------------
st.set_page_config(page_title="Visualizador por Posição", layout="wide")

# CSS e Layout (mantenha igual)
col1, col2 = st.columns([1, 4])
with col1:
    st.image("logocff.svg", width=200)    
with col2:
    st.title("📊 Visualizador por Posição de Coluna")

# Processamento do Excel (original)
GOOGLE_DRIVE_LINK = "https://docs.google.com/spreadsheets/d/1wFo7MDo0NAQA4VZ6t-aIeHDzEnIllRiN/edit?usp=drive_link"
file_id = re.search(r'/d/(.*?)/', GOOGLE_DRIVE_LINK).group(1)
url_download = f"https://drive.google.com/uc?id={file_id}"

try:
    gdown.download(url_download, "a_temp.xlsx", quiet=False)
    df = pd.read_excel("a_temp.xlsx", engine='openpyxl')
    
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
