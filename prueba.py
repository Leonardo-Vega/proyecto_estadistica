import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
import streamlit as st


# TITULO WEB
st.title("ANÁLISIS ESTADÍSTICO DE ESTUDIANTES")


df_est = pd.read_csv("datos_estudiantes.csv")

# MOSTRAR DATAFRAME
st.subheader("Base de Datos")
st.dataframe(df_est.head())

# #AZUL:FASE 2
#-------------------------------------------------------------------------
#-------------------------------------------------------------------------

#variable cualitativa nominal nombre de las carreras
frec_cualita = df_est["carrera"].value_counts().reset_index()

#renombrar columnas
frec_cualita.columns = ["carrera", "fi"]

#frecuencia relativa
frec_cualita["hi"] = frec_cualita["fi"] / len(df_est)

#frecuencia relativa porcentual
frec_cualita["hip"] = frec_cualita["hi"] * 100

#frecuencia acumulada
frec_cualita["Fi"] = frec_cualita["fi"].cumsum()

#frecuencia relativa acumulada
frec_cualita["Hi"] = frec_cualita["hi"].cumsum()

st.subheader("TABLA DE FRECUENCIAS: CARRERAS")
st.dataframe(frec_cualita)

# #AZUL:FASE 3
#-------------------------------------------------------------------------
#-------------------------------------------------------------------------

# 1. Conteo de frecuencias para la variable discreta 'materias_aprobadas'
tabla_discreta = df_est["materias_aprobadas"].value_counts().sort_index().reset_index()

# 2. Renombramos las columnas
tabla_discreta.columns = ["Materias_X", "fi"]

# cálculo de Frecuencia relativa
tabla_discreta["hi"] = tabla_discreta["fi"] / len(df_est)

# Frecuencias Acumuladas
tabla_discreta["Fi"] = tabla_discreta["fi"].cumsum()

tabla_discreta["Hi"] = tabla_discreta["hi"].cumsum()

tabla_discreta["hip"] = tabla_discreta["hi"] * 100

st.subheader("TABLA DE FRECUENCIAS: MATERIAS APROBADAS")
st.dataframe(tabla_discreta)

# #AZUL:FASE 4
#-------------------------------------------------------------------------
#-------------------------------------------------------------------------

#PASO A

#TABLA DE FRECUENCIAS PARA LA VARIABLE CUANTITATIVA DISCRETA EDAD
n = len(df_est)
rango = df_est['edad'].max() - df_est['edad'].min()

# Regla de Sturges
k = int(np.ceil(1 + 3.322 * np.log10(n)))
amplitud = rango / k

st.write(f"n: {n}, Rango: {rango}, Intervalos (k): {k}, Amplitud: {amplitud}")

#divide el rango en k partes
cortes = np.arange(df_est["edad"].min(), df_est["edad"].max()+amplitud, amplitud)

#PASO B

#Definición de intervalos
df_est["intervalos"] = pd.cut(df_est["edad"], bins=cortes, include_lowest=True, right=False)

#a partir de los intervalos se cuentan las frecuencias
tabla_agrupada = df_est["intervalos"].value_counts().sort_index().reset_index()

tabla_agrupada.columns = ["intervalos", "fi"]

#marca de clase
tabla_agrupada["marca_clase"] = tabla_agrupada["intervalos"].apply(lambda x: x.mid)

#frecuencia relativa
tabla_agrupada["hi"] = tabla_agrupada["fi"] / len(df_est)

#frecuencia relativa porcentual
tabla_agrupada["hip"] = tabla_agrupada["hi"] * 100

#frecuencia acumulada
tabla_agrupada["Fi"] = tabla_agrupada["fi"].cumsum()

#frecuencia relativa acumulada
tabla_agrupada["Hi"] = tabla_agrupada["hi"].cumsum()

st.subheader("TABLA AGRUPADA DE EDADES")
st.dataframe(tabla_agrupada)

# #AZUL: FASE 5
#-------------------------------------------------------------------------
#-------------------------------------------------------------------------

# Configuración de estilo académico
plt.style.use('seaborn-v0_8-whitegrid')

plt.rcParams['axes.titlesize'] = 16
plt.rcParams['axes.labelsize'] = 12

#-------------------------------------------------------------------------
# GRAFICO DE BARRAS
#-------------------------------------------------------------------------

fig, ax = plt.subplots(figsize=(12,6))

ax.bar(frec_cualita['carrera'], frec_cualita['fi'], color='skyblue')

ax.set_title('DISTRIBUCIÓN POR CARRERA', fontweight='bold')
ax.set_xlabel('Carreras Universitarias')
ax.set_ylabel('Cantidad de Estudiantes (fi)')

st.pyplot(fig)

#-------------------------------------------------------------------------
# GRAFICO DE BASTON
#-------------------------------------------------------------------------

fig, ax = plt.subplots(figsize=(12,6))

ax.vlines(tabla_discreta['Materias_X'],
          ymin=0,
          ymax=tabla_discreta['fi'],
          color='navy',
          linewidth=2)

ax.plot(tabla_discreta['Materias_X'],
        tabla_discreta['fi'],
        "o",
        color='red')

ax.set_xticks(tabla_discreta['Materias_X'])

ax.set_title('AVANCE ACADEMICO(VARIABLES DISCRETAS)', fontweight='bold')
ax.set_xlabel('Número de Materias Aprobadas')
ax.set_ylabel('Frecuencia Absoluta (fi)')

st.pyplot(fig)

#-------------------------------------------------------------------------
# HISTOGRAMA + POLIGONO
#-------------------------------------------------------------------------

fig, ax = plt.subplots(figsize=(12, 6))

ax.hist(df_est['edad'],
        bins=cortes,
        color='#1fcaa0',
        edgecolor='white',
        alpha=0.6,
        label='Histograma')

ax.plot(tabla_agrupada['marca_clase'],
        tabla_agrupada['fi'],
        color='red',
        marker='D',
        linewidth=2,
        label='Polígono')

ax.set_title('ANÁLISIS DE DISTRIBUCIÓN DE EDADES (DATOS AGRUPADOS)',
             fontweight='bold')

ax.set_xticks(cortes)

ax.set_xlabel('Intervalos de Clase (años) / Marca de Clase (Xi)')
ax.set_ylabel('Frecuencia Absoluta (fi)')

ax.legend()

st.pyplot(fig)

#-------------------------------------------------------------------------
# OJIVA
#-------------------------------------------------------------------------

fig, ax = plt.subplots(figsize=(10,5))

ax.plot(tabla_agrupada['marca_clase'],
        tabla_agrupada['Fi'],
        color='red',
        marker='s',
        linewidth=2,
        label='Ojiva')

ax.fill_between(tabla_agrupada['marca_clase'],
                tabla_agrupada['Fi'],
                color='purple',
                alpha=0.3)

ax.set_title('ANÁLISIS DE DISTRIBUCIÓN DE EDADES (DATOS AGRUPADOS)',
             fontweight='bold')

ax.set_xticks(cortes)

ax.set_xlabel('Intervalos de Clase (años)')
ax.set_ylabel('Frecuencia Absoluta Acumulada (Fi)')

ax.legend()

st.pyplot(fig)

#-------------------------------------------------------------------------
# GRAFICO DE TORTA
#-------------------------------------------------------------------------

fig, ax = plt.subplots(figsize=(10, 5))

ax.pie(frec_cualita['hi'],
       labels=frec_cualita['carrera'],
       autopct='%1.1f%%',
       startangle=90,
       colors=sns.color_palette('pastel'))

ax.set_title("PORCENTAJE DE ESTUDIANTES POR CARRERA",
             fontweight="bold")

st.pyplot(fig)