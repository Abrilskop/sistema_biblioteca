from mvc.data.Conexion import obtener_conexion
from mvc.modelo.CEjemplar import CEjemplar
from mvc.modelo.CLibro import CLibro

class EjemplarServicio:
    def registrar_ejemplar(self, id_ejemplar, isbn):
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.callproc("sp_registrar_ejemplar", (id_ejemplar, isbn))
        conexion.commit()
        cursor.close()
        # No cerramos la conexión global aquí

    # Método actualizado para coincidir con la lógica del controlador
    def cambiar_estado(self, id_ejemplar, nuevo_estado):
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.callproc("sp_cambiar_estado_ejemplar", (id_ejemplar, nuevo_estado))
        conexion.commit()
        cursor.close()

    def listar_ejemplares(self):
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.callproc("sp_listar_ejemplares")
        ejemplares = []
        for resultado in cursor.stored_results():
            for (id_ejemplar, isbn, titulo, estado) in resultado.fetchall():
                libro = CLibro(isbn, titulo)
                ejemplar = CEjemplar(id_ejemplar, libro, estado)
                ejemplares.append(ejemplar)
        cursor.close()
        return ejemplares

    # --- NUEVOS MÉTODOS PARA EL CRUD ---

    def obtener_ejemplar_por_id(self, id_ejemplar):
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.callproc("sp_obtener_ejemplar", (id_ejemplar,))
        ejemplar_obj = None
        for resultado in cursor.stored_results():
            fila = resultado.fetchone()
            if fila:
                (id_ejemplar_db, isbn, titulo, estado) = fila
                libro = CLibro(isbn, titulo)
                ejemplar_obj = CEjemplar(id_ejemplar_db, libro, estado)
                break
        cursor.close()
        return ejemplar_obj

    def actualizar_ejemplar(self, id_ejemplar, isbn, estado):
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.callproc("sp_actualizar_ejemplar", (id_ejemplar, isbn, estado))
        conexion.commit()
        cursor.close()

    def eliminar_ejemplar(self, id_ejemplar):
        conexion = obtener_conexion()
        cursor = conexion.cursor(buffered=True)
        # El procedimiento devuelve 1 para éxito, 0 para falla
        args = (id_ejemplar, 0)
        result_args = cursor.callproc("sp_eliminar_ejemplar", args)
        conexion.commit()
        cursor.close()
        return result_args[1] == 1 # Devuelve True si tuvo éxito, False si no