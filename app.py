import streamlit as st
import pandas as pd
import pyodbc
from sklearn.ensemble import RandomForestClassifier

# Configuración de la página web
st.set_page_config(page_title="Mantenimiento Predictivo Industrial", page_icon="⚙️", layout="wide")

st.title("⚙️ Sistema de Mantenimiento Predictivo - IoT & IA")
st.markdown("Monitoreo en tiempo real y predicción de fallos para maquinaria industrial conectado a **SQL Server**.")

@st.cache_data(ttl=60)
def cargar_datos():
    # Streamlit leerá estos datos de forma segura desde su panel en la nube (o de un archivo local de configuración)
    try:
        server = st.secrets["sql_server"]["server"]
        database = st.secrets["sql_server"]["database"]
        usuario = st.secrets["sql_server"]["usuario"]
        contrasena = st.secrets["sql_server"]["contrasena"]
        
        conexion_str = (
            f"DRIVER={{ODBC Driver 17 for SQL Server}};"
            f"SERVER={server};"
            f"DATABASE={database};"
            f"UID={usuario};"
            f"PWD={contrasena};"
        )
        
        conexion = pyodbc.connect(conexion_str)
        query = "SELECT temperatura_c, vibracion_mm_s, horas_operacion, mantenimiento_reciente, fallo_inminente FROM sensores_maquinas;"
        df = pd.read_sql(query, conexion)
        conexion.close()
        return df
    except Exception as e:
        # Si estás probando en local sin el archivo secrets, puedes dejar tus credenciales de respaldo aquí temporalmente o configurar los secretos locales.
        st.error(f"Error al conectar con la Base de Datos: {e}")
        return pd.DataFrame()
# Cargar los datos en la app
df = cargar_datos()

if not df.empty:
    # Mostrar métricas generales en la parte superior
    col1, col2, col3 = st.columns(3)
    col1.metric("Total de Registros en BD", len(df))
    col2.metric("Temperatura Promedio", f"{df['temperatura_c'].mean():.1f} °C")
    col3.metric("Vibración Promedio", f"{df['vibracion_mm_s'].mean():.2f} mm/s")

    st.divider()

    # Dividir la pantalla en dos columnas: Izquierda (Simulador / Predicción), Derecha (Datos de la BD)
    col_izq, col_der = st.columns([1, 1])

    with col_izq:
        st.subheader("🤖 Simulador de Predicción en Vivo")
        st.markdown("Ingresa los parámetros actuales de una máquina para evaluar su riesgo de fallo:")
        
        # Controles deslizantes (Sliders) para que el usuario mueva los valores
        temp_input = st.slider("Temperatura (°C)", float(df['temperatura_c'].min() - 10), float(df['temperatura_c'].max() + 10), float(df['temperatura_c'].mean()))
        vib_input = st.slider("Vibración (mm/s)", float(df['vibracion_mm_s'].min() - 1), float(df['vibracion_mm_s'].max() + 1), float(df['vibracion_mm_s'].mean()))
        horas_input = st.number_input("Horas de Operación", min_value=0, max_value=20000, value=1500)
        mantenimiento_input = st.selectbox("¿Mantenimiento reciente?", [0, 1], format_func=lambda x: "Sí (1)" if x == 1 else "No (0)")

        # Entrenar el modelo con los datos actuales de SQL Server
        X = df[['temperatura_c', 'vibracion_mm_s', 'horas_operacion', 'mantenimiento_reciente']]
        y = df['fallo_inminente']
        
        modelo = RandomForestClassifier(random_state=42)
        modelo.fit(X, y)

        # Botón para predecir
        if st.button("Evaluar Estado de la Máquina", type="primary"):
            datos_nuevo = [[temp_input, vib_input, horas_input, mantenimiento_input]]
            prediccion = modelo.predict(datos_nuevo)
            
            if prediccion[0] == 1:
                st.error("⚠️ **¡ALERTA! Riesgo Inminente de Fallo Detectado.** Se recomienda programar mantenimiento de inmediato.")
            else:
                st.success("✅ **Máquina Operando Normal.** No se detectan riesgos críticos en los parámetros.")

    with col_der:
        st.subheader("📊 Historial de Sensores (SQL Server)")
        st.markdown("Datos extraídos directamente de tu base de datos local:")
        st.dataframe(df, use_container_width=True)

else:
    st.warning("No se pudieron cargar los datos. Verifica tu conexión a SQL Server y la contraseña en el código.")