import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="Ruta de Materiales - Despacho Académico", layout="centered")
st.title("📦 Generador de Ruta de Materiales para Anteproyecto con ayuda de Mentor AI para AR2007B.545")
st.markdown(
    "Creadora: Dra. J. Isabel Méndez Garduño")

st.markdown("Esta app te permite identificar potenciales materiales de construcción y su cadena de suministro.
En la descripción de materiales, aquí te muestro un ejemplo de qué poner: 

Estamos diseñando un espacio escolar comunitario en la colonia Nonoalco, CDMX, para niños de 3 a 12 años, incluyendo usuarios con discapacidad. El proyecto incluye un área de juegos, una pequeña aula multifuncional, baños accesibles y señalización amigable. Buscamos soluciones que prioricen seguridad, sostenibilidad, accesibilidad y participación vecinal.
            ")

# Estado inicial
if "mentor_respuesta" not in st.session_state:
    st.session_state.mentor_respuesta = ""
if "materiales_dict" not in st.session_state:
    st.session_state.materiales_dict = {}

st.header("Mentor AI de Materiales")
proyecto = st.text_area("🧠 Describe brevemente tu anteproyecto (tipo de espacio, usuarios, escala, necesidades):")

mentor_activado = st.button("🧠 Enviar a Mentor AI")

if proyecto and mentor_activado:
    try:
        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=st.secrets["OPENROUTER_API_KEY"]
        )

        user_prompt = (
            f"Estoy desarrollando un anteproyecto arquitectónico con estas características: {proyecto}.\n\n"
            "1. Sugiéreme materiales apropiados que sean sustentables, accesibles y pertinentes para niños y adolescentes en un entorno escolar urbano como CDMX.\n"
            "2. Posteriormente genera una tabla con tres columnas: Materiales, Propiedades, Uso en el proyecto.\n"
            "3. Después, selecciona todos los materiales propuestos y describe en cada material su cadena de suministro actual (origen, transformación, transporte, actores involucrados).\n"
            "4. Evalúa sus impactos (ambientales, sociales, certificaciones, da 3 alternativas locales o responsables).\n"
            "5. Genera y muestra una tabla donde se muestre en todos los materiales, las 3 alternativas con sus impactos ambientales, sociales, certificaciones.\n"
            "Da la información en formato claro para poder ser usado y no preguntes si desean más información."
        )

        messages = [
            {
                "role": "system",
                "content": (
                    "Eres un arquitecto y urbanista experto en arquitectura participativa, diseño sistémico y con perspectiva de género aplicado al contexto mexicano. "
                    "Tienes experiencia en espacios educativos para infancia y adolescencia, incluyendo educación especial, educación inclusiva y accesibilidad universal. "
                    "Dominas criterios de sostenibilidad, selección de materiales responsables, instalaciones educativas y viabilidad constructiva en contextos urbanos de México."
                )
            },
            {"role": "user", "content": user_prompt}
        ]

        completion = client.chat.completions.create(
            extra_headers={
                "HTTP-Referer": "https://tudespacho-academico.com",
                "X-Title": "Despacho Academico de Arquitectura"
            },
            extra_body={},
            model="deepseek/deepseek-chat-v3-0324:free",
            messages=messages
        )

        mentor_respuesta = completion.choices[0].message.content
        st.markdown("**Sugerencia del Mentor AI:**")
        st.info(mentor_respuesta)

    except Exception as e:
        st.warning(f"No se pudo conectar con el Mentor AI. Error: {e}")


