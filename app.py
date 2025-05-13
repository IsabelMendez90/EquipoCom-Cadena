
import streamlit as st
import pandas as pd
from openai import OpenAI
import os

st.set_page_config(page_title="Ficha Técnica de Materiales", layout="wide")
st.title("📄 Ficha Técnica de Materiales de Construcción con apoyo de Mentor AI para AR2007B.545")
st.markdown(
    "Creadora: Dra. J. Isabel Méndez Garduño")

# Cargar base de datos
df = pd.read_excel("materiales_energyplus.xlsx")

# Inicializar estado para respuestas si no existe
if "respuestas_ai" not in st.session_state:
    st.session_state.respuestas_ai = {}

# Selección del material
materiales = df["Nombre"].tolist()
seleccionados = st.multiselect("Selecciona uno o más materiales para consultar:", materiales)

if seleccionados:
    for nombre in seleccionados:
        st.header(f"🧱 {nombre}")
        fila = df[df["Nombre"] == nombre].iloc[0]

        st.subheader("📐 Propiedades Físicas")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"- **Nombre en Inglés:** {fila['Name(EN)']}")
            st.markdown(f"- **Densidad:** {fila['Densidad (kg/m3)']} kg/m³")
            st.markdown(f"- **Conductividad térmica:** {fila['Conductividad (W/m-K)']} W/m·K")
        with col2:
            st.markdown(f"- **Calor específico:** {fila['Calor Específico (J/kg-K)']} J/kg·K")
            st.markdown(f"- **Rugosidad superficial:** {fila['Rugosidad superficial']}")
            st.markdown(f"- **Tipo:** {fila['Tipo']}")

        st.subheader("🧪 Propiedades Químicas, Ciclo de Vida y Recomendaciones (Mentor AI)")

        # Mostrar respuesta previa si existe
        if nombre in st.session_state.respuestas_ai:
            st.info(st.session_state.respuestas_ai[nombre])

        if st.button(f"🔎 Consultar Mentor AI sobre '{nombre}'"):
            try:
                client = OpenAI(
                    base_url="https://openrouter.ai/api/v1",
                    api_key=st.secrets["OPENROUTER_API_KEY"]
                )

                prompt = f"""
Ficha técnica extendida del material de construcción: {nombre}.
1. Composición química (si es inerte o emite algo), resistencia al fuego y a la corrosión.
2. Origen del material, si es renovable o reciclado, y el impacto de su producción.
3. Recomendaciones para su uso arquitectónico y mantenimiento, especificando si es adecuado para muros, techos, pisos, etc.
Incluye datos numéricos siempre que sea posible. Usa fuentes confiables como literatura técnica o fichas de fabricantes. No le hagas preguntas después al usuario, sólo limítate a brindar la información
"""


                messages = [
                    {
                        "role": "system",
                        "content": (
                            "Eres un arquitecto y urbanista experto en arquitectura participativa, diseño sistémico y con perspectiva de género aplicado al contexto mexicano. "
                            "Tienes experiencia en espacios educativos para infancia y adolescencia, incluyendo educación especial, educación inclusiva y accesibilidad universal. "
                            "Dominas criterios de sostenibilidad, selección de materiales responsables, instalaciones educativas y viabilidad constructiva en contextos urbanos de México."
                        )
                    },
                    {"role": "user", "content": prompt}
                ]

                completion = client.chat.completions.create(
                    extra_headers={
                        "HTTP-Referer": "https://tudespacho-academico.com",
                        "X-Title": "Ficha Tecnica AI"
                    },
                    extra_body={},
                    model="deepseek/deepseek-chat-v3-0324:free",
                    messages=messages
                )

                respuesta = completion.choices[0].message.content
                st.session_state.respuestas_ai[nombre] = respuesta
                st.success("Respuesta del mentor AI almacenada.")
                st.info(respuesta)

            except Exception as e:
                st.warning(f"No se pudo conectar con el Mentor AI. Error: {e}")

