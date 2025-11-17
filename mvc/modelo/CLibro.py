# mvc/modelo/CLibro.py

class CLibro:
    """
    Representa la entidad Libro.
    Autor y año son opcionales para permitir crear objetos
    con información parcial (ej. para listados).
    """
    def __init__(self, isbn, titulo, autor=None, anio_publicacion=None):
        self.isbn = isbn
        self.titulo = titulo
        self.autor = autor
        self.anio_publicacion = anio_publicacion

    def __str__(self):
        return f"Libro: {self.titulo} (ISBN: {self.isbn})"