import streamlit as st
import pandas as pd
from api_client import obtener_usuarios_api
from database import crear_tabla, guardar_usuarios, consultar_usuarios, eliminar_datos

st.set_page_config(page_title="API-SQLITE", page_icon=":guardsman:", layout="wide")

crear_tabla()

st.title("API-SQLITE-STREAMLIT")
st.write("Esta aplicación permite obtener datos de una API y almacenarlos en una base de datos")

menu = st.sidebar.selectbox(
    "Seleccione una opción",
    [
        "Inicio",
        "Consumir API",
        "Ver base de datos",
        "Buscar usuario",
        "Eliminar datos"
    ]
)

# -------------------- INICIO --------------------
if menu == "Inicio":
    st.header("Bienvenido a la APP")
    st.info("Seleccione una opción en el menú lateral")

# -------------------- CONSUMIR API --------------------
elif menu == "Consumir API":
    st.header("Consumir API Pública")
    st.code("https://jsonplaceholder.typicode.com/users")

    if st.button("Obtener usuarios de la API"):
        usuarios = obtener_usuarios_api()

        if usuarios:
            guardar_usuarios(usuarios)
            st.success("Usuarios guardados correctamente")
            st.json(usuarios[0])
        else:
            st.error("No se pudieron obtener datos")

# -------------------- VER BASE DE DATOS --------------------
elif menu == "Ver base de datos":
    st.header("Usuarios almacenados")

    df = consultar_usuarios()

    if not df.empty:
        st.dataframe(df, use_container_width=True)

        col1, col2, col3 = st.columns(3)
        col1.metric("Total usuarios", len(df))
        col2.metric("Total ciudades", df["ciudad"].nunique())
        col3.metric("Total correos", df["email"].nunique())
    else:
        st.warning("No hay datos en la base de datos")

# -------------------- BUSCAR USUARIO --------------------
elif menu == "Buscar usuario":
    st.header("Buscar usuario")

    df = consultar_usuarios()

    if df.empty:
        st.warning("No hay datos guardados")
    else:
        nombre = st.text_input("Ingrese nombre o usuario")

        if nombre:
            resultado = df[
                df["nombre"].str.contains(nombre, case=False, na=False) |
                df["usuario"].str.contains(nombre, case=False, na=False)
            ]

            if resultado.empty:
                st.error("No se encontraron coincidencias")
            else:
                st.success("Resultado encontrado")
                st.dataframe(resultado, use_container_width=True)

# -------------------- ELIMINAR DATOS --------------------
elif menu == "Eliminar datos":
    st.header("Eliminar datos")
    st.warning("Esta acción eliminará todos los registros")

    if st.button("Eliminar todos los datos"):
        eliminar_datos()
        st.success("Datos eliminados correctamente")
