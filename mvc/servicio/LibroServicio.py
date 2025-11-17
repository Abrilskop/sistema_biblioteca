from mvc.data.Conexion import obtener_conexion
from mvc.modelo.CLibro import CLibro

class LibroServicio:
    def listar_libros(self):
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.callproc("sp_listar_libros")
        libros = []
        for resultado in cursor.stored_results():
            for (isbn, titulo) in resultado.fetchall():
                libros.append(CLibro(isbn, titulo))
        cursor.close()
        conexion.close()
        return libros