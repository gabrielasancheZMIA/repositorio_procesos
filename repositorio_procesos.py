import streamlit as st
import os
from pathlib import Path

st.set_page_config(page_title="Repositorio de Procesos", layout="wide")
st.title("📁 Repositorio General por Área")

# Áreas disponibles
areas = ["Incentivos", "Productividad", "Seguimiento", "Sistemática"]

# Crear carpetas si no existen
base_path = Path("repositorio_procesos")
for area in areas:
    (base_path / area).mkdir(parents=True, exist_ok=True)

# ------------------ SUBIR ARCHIVO ------------------
st.markdown("### 📤 Subir nuevo archivo al repositorio")
with st.form("formulario_subida"):
    col1, col2 = st.columns([2, 3])
    with col1:
        area_destino = st.selectbox("Área de destino", areas)
    with col2:
        archivo_subido = st.file_uploader("Selecciona un archivo", type=None, label_visibility="collapsed")
    subir = st.form_submit_button("✅ Subir archivo")

    if subir and archivo_subido:
        ruta_destino = base_path / area_destino / archivo_subido.name
        with open(ruta_destino, "wb") as f:
            f.write(archivo_subido.getbuffer())
        st.success(f"Archivo '{archivo_subido.name}' subido exitosamente a {area_destino}.")
        st.rerun()

st.markdown("---")
st.markdown("### 📚 Archivos almacenados por área")

# ------------------ MOSTRAR TODOS LOS ARCHIVOS POR ÁREA ------------------
for area in areas:
    ruta_area = base_path / area
    archivos = list(ruta_area.glob("*"))

    if archivos:
        st.markdown(f"#### 📂 Área: {area}")
        for archivo in archivos:
            col1, col2, col3 = st.columns([4, 1, 3])
            with col1:
                st.markdown(f"- {archivo.name}")
            with col2:
                if st.button("🗑️ Eliminar", key=f"delete_{area}_{archivo.name}"):
                    archivo.unlink()
                    st.success(f"Archivo '{archivo.name}' eliminado de {area}.")
                    st.rerun()
            with col3:
                nuevo_nombre = st.text_input("Renombrar", value=archivo.stem, key=f"rename_{area}_{archivo.name}")
                if st.button("✅ Renombrar", key=f"rename_btn_{area}_{archivo.name}"):
                    nueva_ruta = archivo.with_name(nuevo_nombre + archivo.suffix)
                    archivo.rename(nueva_ruta)
                    st.success(f"Archivo renombrado a '{nuevo_nombre}'.")
                    st.rerun()
    else:
        st.markdown(f"🗂️ *(Sin archivos en el área {area})*")
