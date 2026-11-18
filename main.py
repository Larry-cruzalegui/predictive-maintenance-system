import pandas as pd
import pyodbc
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

print("--- INICIANDO CONEXIÓN CON SQL SERVER Y MACHINE LEARNING ---\n")

# 1. Configuración usando el servidor y las credenciales de SQL Server (usuario 'sa')
server = 'localhost' 
database = 'MantenimientoIndustrialDB'
usuario = 'sa'
contrasena = 'La200715'  # Pon la contraseña que usaste en la pantalla

# Cadena de conexión para Autenticación de SQL Server
conexion_str = (
    f"DRIVER={{ODBC Driver 17 for SQL Server}};"
    f"SERVER={server};"
    f"DATABASE={database};"
    f"UID={usuario};"
    f"PWD={contrasena};"
)
try:
    # 2. Conectarse a la base de datos y extraer los datos en vivo
    print("Conectando a SQL Server...")
    conexion = pyodbc.connect(conexion_str)
    
    query = """
        SELECT temperatura_c, vibracion_mm_s, horas_operacion, mantenimiento_reciente, fallo_inminente 
        FROM sensores_maquinas;
    """
    
    # Pandas lee directamente el resultado de la consulta SQL y lo convierte en un DataFrame
    df = pd.read_sql(query, conexion)
    conexion.close()
    
    print("¡Datos extraídos con éxito desde SQL Server! Primeras filas:")
    print(df.head(), "\n")

    # 3. Separar características (X) y la variable objetivo (y)
    X = df[['temperatura_c', 'vibracion_mm_s', 'horas_operacion', 'mantenimiento_reciente']]
    y = df['fallo_inminente']

    # 4. Dividir los datos en entrenamiento y prueba
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # 5. Entrenar el modelo de Machine Learning
    print("Entrenando el modelo predictivo con datos de la BD...")
    modelo = RandomForestClassifier(random_state=42)
    modelo.fit(X_train, y_train)

    # 6. Evaluar el modelo
    y_pred = modelo.predict(X_test)
    precision = accuracy_score(y_test, y_pred)

    print(f"\n¡Modelo entrenado y evaluado con éxito!")
    print(f"Precisión del modelo: {precision * 100:.2f}%\n")
    print("Reporte de clasificación detallado:")
    print(classification_report(y_test, y_pred, zero_division=0))

except Exception as e:
    print("\n[Error de conexión]: Ocurrió un error al conectar con SQL Server.")
    print("Detalle técnico:", e)
    