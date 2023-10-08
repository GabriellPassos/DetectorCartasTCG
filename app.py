import streamlit as st
import numpy as np
from PIL import Image
from Identificador import Identificar

def btnToggle(btnName):
    st.session_state[btnName] = not st.session_state[btnName]
def process(image):
    st.spinner(text="In progress...")
    image = Image.open(image)
    return Identificar(image, minAltura=minAlt, maxAltura=maxAlt, minLargura=minLar, maxLargura=maxLar)

st.title("Detector de Cartas TCG")
st.subheader("Monte novos baralhos!")
st.text("Basta tirar uma foto das suas cartas e fazer o upload para o Detector de Cartas TCG. \nNosso algoritmo inteligente reconhece automaticamente cada carta e a adiciona \nà sua coleção virtual. Você pode categorizá-las, filtrá-las e gerenciá-las \ncom facilidade, poupando horas de trabalho manual.")
st.sidebar.header("Configurações")
st.sidebar.subheader("Medida Limite")
st.sidebar.text("Filtra os resultados da busca \npela altura e largura individual.")
minAlt = st.sidebar.number_input('MIN Altura', value= 0)
maxAlt = st.sidebar.number_input('MAX Altura', value= 1000)
minLar = st.sidebar.number_input('MIN Largura', value=0)
maxLar = st.sidebar.number_input('MAX Largura', value= 1000)
if 'btnCamera' not in st.session_state:
    st.session_state.btnCamera = False


if st.session_state.btnCamera:
    btnCameraText = 'Desligar Câmera'
    picture = st.camera_input("Posicione sua(s) cartas")
    if picture:
        img = process(picture)
        st.image(img)
else:
    btnCameraText = 'Ligar Câmera'
    uploaded_file = st.file_uploader("Selecione uma imagem")
    if uploaded_file is not None:
        img = process(uploaded_file)
        st.image(img)

btnCamera = st.button(btnCameraText)

if btnCamera:
    on_click = btnToggle("btnCamera")


