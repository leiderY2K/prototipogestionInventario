import mysql.connector
from mysql.connector import Error
from codigo_producto import CodigoProducto

class GuardarMySQL:
    def __init__(self, db_config):
        """
        Inicializa la clase con la configuración de la base de datos.
        
        :param db_config: Diccionario con la configuración de la base de datos
        """
        self.codigo_producto = CodigoProducto()
        self.host = db_config['host']
        self.user = db_config['user']
        self.password = db_config['password']
        self.database = db_config['database']
        self.connection = None

    def conectar(self):
        """
        Establece la conexión con la base de datos MySQL.
        """
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            if self.connection.is_connected():
                print("Conexión a la base de datos MySQL establecida con éxito.")
        except Error as e:
            print(f"Error al conectar a MySQL: {e}")
            raise

    def separar_nombre(self, nombre_completo):
        partes = nombre_completo.split()
        if len(partes) > 1:
            return partes[0], ' '.join(partes[1:])
        return nombre_completo, ''

    def guardar_datos(self, resultados):
        """
        Guarda los resultados en las tablas correspondientes de MySQL.
        """
        if self.connection is None or not self.connection.is_connected():
            return

        cursor = None
        try:
            cursor = self.connection.cursor(buffered=True)  # Usar cursor buffered


            for resultado in resultados:
                try:
                    # Verificar que el resultado tenga todos los elementos necesarios
                    if len(resultado) < 6:
                        continue

                    investigador = resultado[0]
                    titulo_producto = resultado[1]
                    tipo_producto = resultado[2]
                    año = resultado[3]
                    nombre_archivo = resultado[4]
                    link_archivo = resultado[5]

                    # Procesar tipo de producto
                    tipo_producto_final = tipo_producto.split(", ")[0] if tipo_producto else "XCNE"
                    
                    # Procesar año
                    año_final = año.split(", ")[0] if año else "XANE"
                    try:
                        año_final = int(año_final)
                    except ValueError:
                        año_final = 0  # Año por defecto si no se puede convertir

                    # Separar nombres y apellidos
                    nombres, apellidos = self.separar_nombre(investigador)

                    # Insertar tipo de producto
                    cursor.execute(
                        "INSERT IGNORE INTO TipoDeProducto (nombreTipoDeProducto) VALUES (%s)",
                        (tipo_producto_final,)
                    )

                    # Obtener el ID del tipo de producto
                    cursor.execute(
                        "SELECT idTipoDeProducto FROM TipoDeProducto WHERE nombreTipoDeProducto = %s",
                        (tipo_producto_final,)
                    )
                    tipo_producto_id = cursor.fetchone()[0]

                    # Generar código único para el producto
                    codigo_producto = self.codigo_producto.generar_codigo_producto(
                        investigador, str(año_final), tipo_producto_final
                    )

                    # Insertar el producto (con link_archivo vacío)
                    cursor.execute(
                        "INSERT INTO Producto (TituloProducto, linkVisualizacion, codigoUnico, ano, idTipoDeProducto) "
                        "VALUES (%s, %s, %s, %s, %s)",
                        (titulo_producto, '', codigo_producto, año_final, tipo_producto_id)
                    )

                    # Obtener el ID del producto insertado
                    cursor.execute(
                        "SELECT idProducto FROM Producto WHERE codigoUnico = %s",
                        (codigo_producto,)
                    )
                    producto_id = cursor.fetchone()[0]

                    # Insertar el investigador
                    cursor.execute(
                        "INSERT IGNORE INTO Investigador (nombres, apellidos) VALUES (%s, %s)",
                        (nombres, apellidos)
                    )

                    # Obtener el ID del investigador
                    cursor.execute(
                        "SELECT idInvestigador FROM Investigador WHERE nombres = %s AND apellidos = %s",
                        (nombres, apellidos)
                    )
                    investigador_id = cursor.fetchone()[0]

                    # Relacionar investigador con producto
                    cursor.execute(
                        "INSERT IGNORE INTO InvestigadorProducto (idInvestigador, idProducto) "
                        "VALUES (%s, %s)",
                        (investigador_id, producto_id)
                    )


                except Error as e:
                    # Continúa con el siguiente resultado en caso de error
                    continue

            # Confirmar los cambios
            self.connection.commit()

        except Error as e:
            self.connection.rollback()
        finally:
            if cursor:
                cursor.close()
            
    def cerrar_conexion(self):

        if hasattr(self, 'connection') and self.connection.is_connected():
            self.connection.close()
            print("Conexión cerrada.")