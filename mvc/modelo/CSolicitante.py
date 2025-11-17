# mvc/modelo/CSolicitante.py

class CSolicitante:
    def __init__(self, id_solicitante, nombre, paterno, materno):
        """Inicializa la información del solicitante."""
        self.id_solicitante = id_solicitante
        self.nombre = nombre
        self.paterno = paterno
        self.materno = materno

    def nombre_completo(self):
        """
        Devuelve el nombre completo del solicitante concatenado.
        Este es el método que la plantilla necesita.
        """
        return f"{self.nombre} {self.paterno} {self.materno}"

    def __str__(self):
        return f"Solicitante: {self.nombre_completo()} (ID: {self.id_solicitante})"