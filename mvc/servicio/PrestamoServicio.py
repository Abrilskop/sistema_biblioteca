from datetime import date, timedelta
from mvc.data.Conexion import obtener_conexion
from mvc.modelo.CPrestamo import CPrestamo
from mvc.modelo.CSolicitante import CSolicitante
from mvc.modelo.CEjemplar import CEjemplar
from mvc.modelo.CLibro import CLibro

class PrestamoServicio:
    def registrar_prestamo(self, id_ejemplar, id_solicitante, dias_prestamo=15):
        conexion = obtener_conexion()
        cursor = conexion.cursor(buffered=True)
        fecha_hoy = date.today()
        fecha_devolucion = fecha_hoy + timedelta(days=dias_prestamo)
        args = (id_ejemplar, id_solicitante, fecha_hoy, fecha_devolucion, 0)
        result_args = cursor.callproc("sp_registrar_prestamo", args)
        conexion.commit()
        cursor.close()
        conexion.close()
        return result_args[4]

    def registrar_devolucion(self, id_prestamo):
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        fecha_hoy = date.today()
        cursor.callproc("sp_devolver_prestamo", (id_prestamo, fecha_hoy))
        conexion.commit()
        cursor.close()
        conexion.close()

    def listar_prestamos(self, solo_pendientes=True):
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        param = 1 if solo_pendientes else 0
        cursor.callproc("sp_listar_prestamos", (param,))
        prestamos = []
        for resultado in cursor.stored_results():
            for fila in resultado.fetchall():
                (id_p, id_e, estado_e, id_s, nom_s, pat_s, mat_s, f_pres, f_prev, f_real) = fila
                solicitante = CSolicitante(id_s, nom_s, pat_s, mat_s)
                libro_info = CLibro("", "N/A")
                ejemplar = CEjemplar(id_e, libro_info, estado_e)
                prestamo = CPrestamo(id_p, ejemplar, solicitante, f_pres, f_prev, f_real)
                prestamos.append(prestamo)
        cursor.close()
        conexion.close()
        return prestamos