import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

st.set_page_config(
    page_title="Dashboard PIB",
    page_icon="📈",
    layout="wide"
)
Logo = st.sidebar.image("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQpjWwKg2T0Y8Uek5thVlKtlQQyjijaqRWlpSw7qLSFeA&s=10")

st.title("📈 Dashboard del Crecimiento del PIB")

df = pd.read_csv("pib.csv")

# Eliminar columnas innecesarias si existen
df = df.drop(columns=["Unnamed: 0"], errors="ignore")

# Lista de países
paises = sorted(df["Country Name"].dropna().unique())

# Sidebar
pais = st.sidebar.selectbox(
    "Seleccione un país",
    paises
)

st.sidebar.write("Nicolás Conejeros")

anios = list(map(int, df.columns[2:]))

inicio, fin = st.slider(
    "Seleccione el rango de años",
    min_value=min(anios),
    max_value=max(anios),
    value=(2000, 2024)
)

#Lista de La OCDE (Organización para la Cooperación y el Desarrollo Económicos)
ocde = [
    'Alemania','Australia','Austria','Bélgica','Canadá',
    'Chile','Colombia','Corea, República de','Costa Rica',
    'Dinamarca','República Eslovaca','Eslovenia','España',
    'Estados Unidos','Estonia','Finlandia','Francia',
    'Grecia','Hungría','Irlanda','Islandia','Israel',
    'Italia','Japón','Letonia','Lituania','Luxemburgo',
    'México','Noruega','Nueva Zelandia','Países Bajos',
    'Polonia','Portugal','Reino Unido','República Checa',
    'Suecia','Suiza','Turquía'
]

datos_pais = df[df["Country Name"] == pais]

anios_seleccionados = [str(a) for a in range(inicio, fin+1)]

serie_pais = datos_pais[anios_seleccionados].iloc[0]

promedio_pais = serie_pais.mean()


#Promedio OCDE
datos_ocde = df[df["Country Name"].isin(ocde)]

promedio_ocde = (
    datos_ocde[anios_seleccionados]
    .mean(axis=1)
    .mean()
)

#Diferencia
diferencia = promedio_pais - promedio_ocde

#Las KPIs (Tarjetas Estadísticas)
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Promedio del país",
        f"{promedio_pais:.2f}%"
    )

with col2:
    st.metric(
        "Promedio OCDE",
        f"{promedio_ocde:.2f}%"
    )

with col3:
    st.metric(
        "Diferencia",
        f"{diferencia:.2f}%"
    )


#Gráfico del crecimiento del PIB (%)
fig, ax = plt.subplots(figsize=(10,5))

ax.plot(
    anios_seleccionados,
    serie_pais.values,
    label=pais
)

promedio_anual_ocde = datos_ocde[anios_seleccionados].mean()

ax.plot(
    anios_seleccionados,
    promedio_anual_ocde.values,
    label="Promedio OCDE"
)

ax.set_title("Crecimiento del PIB (%)")
ax.set_ylabel("%")
ax.legend()

st.pyplot(fig)
