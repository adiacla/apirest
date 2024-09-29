from flask import Flask, jsonify, request
import mysql.connector

app = Flask(__name__)

# Configurar la conexión a la base de datos MySQL
def db_connection():
    connection = mysql.connector.connect(
        host="ec2-3-87-21-118.compute-1.amazonaws.com",  # Tu dirección de host
        user="root",                              # Tu usuario de MySQL
        password="dclaros1",                       # Tu contraseña de MySQL
        database="ventas"                     # El nombre de la base de datos
    )
    return connection

# Ruta para obtener datos de una tabla específica
@app.route('/api/datos', methods=['GET'])
def obtener_datos():
    try:
        # Conectarse a la base de datos
        conn = db_connection()
        cursor = conn.cursor(dictionary=True)

        # Ejecutar una consulta SQL
        cursor.execute("SELECT * FROM transacciones")
        rows = cursor.fetchall()

        # Devolver los resultados como JSON
        return jsonify(rows), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

@app.route('/api/datos/producto/<string:producto>', methods=['GET'])
def obtener_dato_por_producto(producto):
    try:
        conn = db_connection()
        cursor = conn.cursor(dictionary=True)

        # Ejecutar una consulta SQL con el nombre del producto
        cursor.execute("SELECT * FROM tu_tabla WHERE Producto = %s", (producto,))
        row = cursor.fetchone()

        # Si no existe el registro, retornar un 404
        if row is None:
            return jsonify({"error": "Registro no encontrado"}), 404

        return jsonify(row), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# Ruta para insertar un nuevo registro en la tabla
@app.route('/api/datos', methods=['POST'])
def insertar_dato():
    try:
        # Obtener datos enviados en la petición POST
        nuevo_dato = request.json

        # Conectar a la base de datos
        conn = db_connection()
        cursor = conn.cursor()

        # Crear la consulta de inserción con los valores correctos
        sql = """
            INSERT INTO transacciones (Producto, Cliente, Cantidad, PrecioU, TotalVenta, Fecha)
            VALUES (%s, %s, %s, %s, %s, %s)
        """

        # Obtener y validar los valores necesarios del JSON recibido
        producto = nuevo_dato.get('Producto')
        cliente = nuevo_dato.get('Cliente')
        cantidad = int(nuevo_dato.get('Cantidad'))  # Cantidad es un entero
        precioU = float(nuevo_dato.get('PrecioU'))  # PrecioU es flotante
        totalVenta = float(nuevo_dato.get('TotalVenta'))  # TotalVenta es flotante
        fecha = nuevo_dato.get('Fecha')  # Se espera una fecha en formato 'YYYY-MM-DD'

        # Asegurarse de que la fecha esté en formato de datetime.date
        fecha = datetime.datetime.strptime(fecha, '%Y-%m-%d').date()

        # Crear la tupla de valores
        valores = (producto, cliente, cantidad, precioU, totalVenta, fecha)

        # Ejecutar la consulta
        cursor.execute(sql, valores)
        conn.commit()

        return jsonify({"message": "Registro insertado correctamente"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)