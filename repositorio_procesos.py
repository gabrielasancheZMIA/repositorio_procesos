import streamlit as st
import os
from pathlib import Path
import shutil

st.set_page_config(page_title="Repositorio de Procesos", layout="wide")

st.title("📁 Repositorio por Área")

# Áreas disponibles
areas = ["Incentivos", "Productividad", "Seguimiento", "Sistemática"]

# Crear carpetas si no existen
base_path = Path("repositorio_procesos")
for area in areas:
    area_path = base_path / area
    area_path.mkdir(parents=True, exist_ok=True)

# Selección de área
area_seleccionada = st.selectbox("Selecciona un área", areas)
ruta_area = base_path / area_seleccionada

st.markdown("### 📂 Archivos en el área seleccionada")
archivos = list(ruta_area.glob("*"))

# Mostrar archivos disponibles
for archivo in archivos:
    col1, col2, col3 = st.columns([4, 1, 2])
    with col1:
        st.markdown(f"- {archivo.name}")
    with col2:
        if st.button("🗑️ Eliminar", key=f"delete_{archivo.name}"):
            archivo.unlink()
            st.success(f"Archivo '{archivo.name}' eliminado.")
            st.rerun()
    with col3:
        nuevo_nombre = st.text_input("Renombrar", value=archivo.stem, key=f"rename_{archivo.name}")
        if st.button("✅ Renombrar", key=f"rename_btn_{archivo.name}"):
            nueva_ruta = archivo.with_name(nuevo_nombre + archivo.suffix)
            archivo.rename(nueva_ruta)
            st.success(f"Archivo renombrado a '{nuevo_nombre}'.")
            st.rerun()

st.markdown("---")
st.markdown("### 📤 Subir nuevo archivo")

archivo_subido = st.file_uploader("Selecciona un archivo", type=None)

if archivo_subido is not None:
    destino = ruta_area / archivo_subido.name
    with open(destino, "wb") as f:
        f.write(archivo_subido.getbuffer())
    st.success(f"Archivo '{archivo_subido.name}' subido exitosamente a {area_seleccionada}.")
    st.rerun()

