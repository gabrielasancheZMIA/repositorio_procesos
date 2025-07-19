import streamlit as st
import os
from pathlib import Path

# Configuración de interfaz
st.set_page_config(page_title="Repositorio por Área", layout="wide")
st.markdown("""
    <style>
    .st-emotion-cache-1v0mbdj {
        padding: 2rem 3rem;
    }
    </style>
""", unsafe_allow_html=True)

# Carpeta base del repositorio
BASE_DIR = Path("repositorio_procesos")
AREAS = ["Incentivos", "Productividad", "Seguimiento", "Sistemática"]

# Crear carpetas si no existen
for area in AREAS:
    os.makedirs(BASE_DIR / area, exist_ok=True)

st.title("📁 Repositorio por Área")

# Selección de área
area = st.selectbox("Selecciona un área", AREAS)
area_path = BASE_DIR / area

st.subheader("📂 Archivos en el área seleccionada")

# Listar archivos existentes
todos_archivos = sorted(os.listdir(area_path))

if not todos_archivos:
    st.info("No hay archivos en esta área.")
else:
    for archivo in todos_archivos:
        col1, col2, col3, col4 = st.columns([4, 1, 2, 2])

        with col1:
            st.markdown(f"- {archivo}")

        # Botón Eliminar
        with col2:
            if st.button("🗑️ Eliminar", key=f"eliminar_{archivo}"):
                os.remove(area_path / archivo)
                st.success(f"'{archivo}' eliminado correctamente.")
                st.experimental_rerun()

        # Descargar archivo
        with col3:
            with open(area_path / archivo, "rb") as f:
                st.download_button("⬇️ Descargar", f, file_name=archivo, key=f"descargar_{archivo}")

        # Renombrar archivo
        with col4:
            nuevo_nombre = st.text_input("Renombrar", value=archivo.split(".")[0], key=f"renombrar_input_{archivo}")
            if st.button("✅ Renombrar", key=f"renombrar_btn_{archivo}"):
                extension = Path(archivo).suffix
                nuevo_archivo = f"{nuevo_nombre}{extension}"
                nuevo_path = area_path / nuevo_archivo
                if not nuevo_path.exists():
                    os.rename(area_path / archivo, nuevo_path)
                    st.success(f"'{archivo}' renombrado a '{nuevo_archivo}'")
                    st.experimental_rerun()
                else:
                    st.error("Ya existe un archivo con ese nombre.")

# Subir nuevo archivo
st.markdown("---")
st.subheader("📤 Subir nuevo archivo")
archivo_subido = st.file_uploader("Selecciona un archivo", type=None)

if archivo_subido:
    ruta_guardar = area_path / archivo_subido.name
    with open(ruta_guardar, "wb") as f:
        f.write(archivo_subido.read())
    st.success(f"'{archivo_subido.name}' subido correctamente a '{area}'.")
    st.experimental_rerun()
