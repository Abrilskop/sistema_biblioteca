import mysql.connector
# Se ajusta la ruta de importación para que funcione dentro de la estructura MVC
from mvc.data.Configuracion import Configuracion

class Conexion:
    _instance = None
    _db_connection = None # Atributo para almacenar el objeto de conexión
    _config = None

    @classmethod
    def obtener_instancia(cls, configuracion: Configuracion = None):
        if cls._instance is None:
            if configuracion is None:
                raise ValueError("Se requiere una configuración para la primera instancia.")
            cls._instance = cls.__new__(cls)
            cls._instance._config = configuracion
            cls._instance._inicializar_conexion()
        return cls._instance

    def _inicializar_conexion(self):
        parametros = self._config.obtener_parametros()
        try:
            self._db_connection = mysql.connector.connect(**parametros)
            print("Conexión persistente a la DB establecida.")
        except mysql.connector.Error as e:
            # En lugar de un error genérico, lanzamos el error de MySQL
            raise e

    def obtener_conexion_activa(self):
        """
        Retorna el objeto de conexión de la base de datos,
        reconectando si es necesario.
        """
        if self._db_connection is None or not self._db_connection.is_connected():
            print("Conexión perdida. Intentando reconectar...")
            self._inicializar_conexion()
        
        return self._db_connection

# --- INICIALIZACIÓN DEL SINGLETON ---
# 1. Se crea el objeto de configuración una sola vez.
# "172.20.10.4"
config = Configuracion(
    host="localhost",
    port=3306,
    user="root",
    password="systemowner",  # <-- TU CONTRASEÑA
    database="bdserviciobiblioteca"
)

# 2. Se llama al classmethod para crear la instancia Singleton en cuanto se carga el módulo.
_db_singleton_instance = Conexion.obtener_instancia(config)

# 3. Se crea una función de ayuda global para que los servicios la usen fácilmente.
def obtener_conexion():
    """
    Esta función simple devuelve el objeto de conexión activo desde el Singleton.
    """
    return _db_singleton_instance.obtener_conexion_activa()