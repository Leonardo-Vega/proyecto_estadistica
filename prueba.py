import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
import streamlit as st

# TITULO WEB
st.title("ANÁLISIS ESTADÍSTICO DE POKÉMON")

df_est = pd.read_csv("datos_pokemon.csv")

# MOSTRAR DATAFRAME
st.subheader("Base de Datos")
st.dataframe(df_est.head())

#-------------------------------------------------------------------------
# FASE 2
#-------------------------------------------------------------------------

# Variable cualitativa nominal: Tipo Principal
frec_cualita = df_est["tipo_principal"].value_counts().reset_index()

# Renombrar columnas
frec_cualita.columns = ["tipo_principal", "fi"]

# Frecuencia relativa
frec_cualita["hi"] = frec_cualita["fi"] / len(df_est)

# Frecuencia relativa porcentual
frec_cualita["hip"] = frec_cualita["hi"] * 100

# Frecuencia acumulada
frec_cualita["Fi"] = frec_cualita["fi"].cumsum()

# Frecuencia relativa acumulada
frec_cualita["Hi"] = frec_cualita["hi"].cumsum()

st.subheader("TABLA DE FRECUENCIAS: TIPOS DE POKÉMON")
st.dataframe(frec_cualita)

#-------------------------------------------------------------------------
# FASE 3
#-------------------------------------------------------------------------

# Variable cuantitativa discreta: Nivel
tabla_discreta = df_est["nivel"].value_counts().sort_index().reset_index()

# Renombrar columnas
tabla_discreta.columns = ["Nivel_X", "fi"]

# Frecuencia relativa
tabla_discreta["hi"] = tabla_discreta["fi"] / len(df_est)

# Frecuencia acumulada
tabla_discreta["Fi"] = tabla_discreta["fi"].cumsum()

# Frecuencia relativa acumulada
tabla_discreta["Hi"] = tabla_discreta["hi"].cumsum()

# Frecuencia relativa porcentual
tabla_discreta["hip"] = tabla_discreta["hi"] * 100

st.subheader("TABLA DE FRECUENCIAS: NIVELES")
st.dataframe(tabla_discreta)

#-------------------------------------------------------------------------
# FASE 4
#-------------------------------------------------------------------------

# Variable cuantitativa agrupada: Velocidad

n = len(df_est)
rango = df_est['velocidad'].max() - df_est['velocidad'].min()

# Regla de Sturges
k = int(np.ceil(1 + 3.322 * np.log10(n)))
amplitud = rango / k

st.write(f"n: {n}, Rango: {rango}, Intervalos (k): {k}, Amplitud: {amplitud}")

# Divide el rango en k partes
cortes = np.arange(
    df_est["velocidad"].min(),
    df_est["velocidad"].max() + amplitud,
    amplitud
)

# Definición de intervalos
df_est["intervalos"] = pd.cut(
    df_est["velocidad"],
    bins=cortes,
    include_lowest=True,
    right=False
)

# Frecuencias
tabla_agrupada = df_est["intervalos"].value_counts().sort_index().reset_index()

tabla_agrupada.columns = ["intervalos", "fi"]

# Marca de clase
tabla_agrupada["marca_clase"] = tabla_agrupada["intervalos"].apply(lambda x: x.mid)

# Frecuencia relativa
tabla_agrupada["hi"] = tabla_agrupada["fi"] / len(df_est)

# Frecuencia relativa porcentual
tabla_agrupada["hip"] = tabla_agrupada["hi"] * 100

# Frecuencia acumulada
tabla_agrupada["Fi"] = tabla_agrupada["fi"].cumsum()

# Frecuencia relativa acumulada
tabla_agrupada["Hi"] = tabla_agrupada["hi"].cumsum()

st.subheader("TABLA AGRUPADA DE VELOCIDAD")
st.dataframe(tabla_agrupada)

#-------------------------------------------------------------------------
# FASE 5
#-------------------------------------------------------------------------

plt.style.use('seaborn-v0_8-whitegrid')

plt.rcParams['axes.titlesize'] = 16
plt.rcParams['axes.labelsize'] = 12

#-------------------------------------------------------------------------
# GRAFICO DE BARRAS
#-------------------------------------------------------------------------

fig, ax = plt.subplots(figsize=(12,6))

ax.bar(
    frec_cualita['tipo_principal'],
    frec_cualita['fi'],
    color='skyblue'
)

ax.set_title('DISTRIBUCIÓN POR TIPO DE POKÉMON', fontweight='bold')
ax.set_xlabel('Tipo Principal')
ax.set_ylabel('Cantidad de Pokémon (fi)')

st.pyplot(fig)

#-------------------------------------------------------------------------
# GRAFICO DE BASTON
#-------------------------------------------------------------------------

fig, ax = plt.subplots(figsize=(12,6))

ax.vlines(
    tabla_discreta['Nivel_X'],
    ymin=0,
    ymax=tabla_discreta['fi'],
    color='navy',
    linewidth=2
)

ax.plot(
    tabla_discreta['Nivel_X'],
    tabla_discreta['fi'],
    "o",
    color='red'
)

ax.set_xticks(tabla_discreta['Nivel_X'])

ax.set_title('DISTRIBUCIÓN DE NIVELES', fontweight='bold')
ax.set_xlabel('Nivel')
ax.set_ylabel('Frecuencia Absoluta (fi)')

st.pyplot(fig)

#-------------------------------------------------------------------------
# HISTOGRAMA + POLIGONO
#-------------------------------------------------------------------------

fig, ax = plt.subplots(figsize=(12, 6))

ax.hist(
    df_est['velocidad'],
    bins=cortes,
    color='#1fcaa0',
    edgecolor='white',
    alpha=0.6,
    label='Histograma'
)

ax.plot(
    tabla_agrupada['marca_clase'],
    tabla_agrupada['fi'],
    color='red',
    marker='D',
    linewidth=2,
    label='Polígono'
)

ax.set_title(
    'ANÁLISIS DE VELOCIDAD DE LOS POKÉMON',
    fontweight='bold'
)

ax.set_xticks(cortes)

ax.set_xlabel('Intervalos de Velocidad')
ax.set_ylabel('Frecuencia Absoluta (fi)')

ax.legend()

st.pyplot(fig)

#-------------------------------------------------------------------------
# OJIVA
#-------------------------------------------------------------------------

fig, ax = plt.subplots(figsize=(10,5))

ax.plot(
    tabla_agrupada['marca_clase'],
    tabla_agrupada['Fi'],
    color='red',
    marker='s',
    linewidth=2,
    label='Ojiva'
)

ax.fill_between(
    tabla_agrupada['marca_clase'],
    tabla_agrupada['Fi'],
    color='purple',
    alpha=0.3
)

ax.set_title(
    'OJIVA DE VELOCIDAD DE LOS POKÉMON',
    fontweight='bold'
)

ax.set_xticks(cortes)

ax.set_xlabel('Intervalos de Velocidad')
ax.set_ylabel('Frecuencia Absoluta Acumulada (Fi)')

ax.legend()

st.pyplot(fig)

#-------------------------------------------------------------------------
# GRAFICO DE TORTA
#-------------------------------------------------------------------------

fig, ax = plt.subplots(figsize=(10,5))

ax.pie(
    frec_cualita['hi'],
    labels=frec_cualita['tipo_principal'],
    autopct='%1.1f%%',
    startangle=90,
    colors=sns.color_palette('pastel')
)

ax.set_title(
    "PORCENTAJE DE POKÉMON POR TIPO",
    fontweight='bold'
)

st.pyplot(fig)