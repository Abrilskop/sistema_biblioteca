class Configuracion:
    """
    Clase que almacena los parámetros de la base de datos.
    Actúa como una fuente de datos de configuración.
    """

    def __init__(self, host, port, user, password, database):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database

    def obtener_parametros(self):
        """Devuelve los parámetros como un diccionario."""
        return {
            "host": self.host,
            "port": self.port,
            "user": self.user,
            "password": self.password,
            "database": self.database
        }