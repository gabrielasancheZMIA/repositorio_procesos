import streamlit as st
import os
import shutil
from pathlib import Path

# Áreas definidas
AREAS = ["Incentivos", "Productividad", "Seguimiento", "Sistemática"]
BASE_DIR = Path("repositorio_procesos")

# Crear estructura de carpetas si no existe
for area in AREAS:
    os.makedirs(BASE_DIR / area, exist_ok=True)

# Configuración general de la interfaz
st.set_page_config(page_title="Repositorio por Área", page_icon="📁", layout="centered")

st.markdown("## 📁 Repositorio por Área")
st.markdown("Sube, descarga, elimina o renombra archivos organizados por área.\n")

# Selección de área
area_seleccionada = st.selectbox("Selecciona un área", AREAS)

if area_seleccionada:
    area_path = BASE_DIR / area_seleccionada
    archivos = os.listdir(area_path)

    st.markdown(f"### 📂 Archivos en el área seleccionada")

    if archivos:
        archivo_seleccionado = st.selectbox("Selecciona un archivo", archivos)

        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("📥 Descargar"):
                with open(area_path / archivo_seleccionado, "rb") as f:
                    st.download_button(
                        label="Descargar archivo",
                        data=f,
                        file_name=archivo_seleccionado,
                        mime="application/octet-stream"
                    )

        with col2:
            if st.button("🗑️ Eliminar"):
                os.remove(area_path / archivo_seleccionado)
                st.success(f"Archivo eliminado: {archivo_seleccionado}")
                st.query_params.clear()  # 🔄 Refrescar página sin error
                st.stop()

        with col3:
            nuevo_nombre = st.text_input("Renombrar", value=archivo_seleccionado.split(".")[0])
            if st.button("✅ Renombrar"):
                nueva_ruta = area_path / f"{nuevo_nombre}{Path(archivo_seleccionado).suffix}"
                os.rename(area_path / archivo_seleccionado, nueva_ruta)
                st.success(f"Archivo renombrado como: {nueva_ruta.name}")
                st.query_params.clear()
                st.stop()
    else:
        st.info("No hay archivos en esta área.")

# Subida de nuevos archivos
st.markdown("---")
st.markdown("### 📤 Subir nuevo archivo")

archivo_subido = st.file_uploader("Selecciona un archivo", type=None)

if archivo_subido is not None:
    archivo_destino = BASE_DIR / area_seleccionada / archivo_subido.name
    with open(archivo_destino, "wb") as f:
        f.write(archivo_subido.read())
    st.success(f"Archivo cargado exitosamente: {archivo_subido.name}")
    st.query_params.clear()
    st.stop()
