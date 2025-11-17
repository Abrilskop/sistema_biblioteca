class CEjemplar:
    def __init__(self, id_ejemplar, libro, estado="Disponible"):
        """Inicializa el ejemplar, asociado a un objeto Libro."""
        self.id_ejemplar = id_ejemplar # ID único del ejemplar físico (ej. código de barras)
        self.libro = libro # Referencia al objeto Libro
        self.estado = estado # Estado: 'Disponible', 'Prestado', 'En Reparación'

    def __str__(self):
        return f"Ejemplar #{self.id_ejemplar} de '{self.libro.titulo}'. Estado: {self.estado}"