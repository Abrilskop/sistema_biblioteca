from mvc.data.Conexion import obtener_conexion
from mvc.modelo.CSolicitante import CSolicitante

class SolicitanteServicio:
    def listar_solicitantes_activos(self):
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.callproc("sp_listar_solicitantes_activos")
        solicitantes = []
        for resultado in cursor.stored_results():
            for (id_sol, nombre, pat, mat) in resultado.fetchall():
                solicitantes.append(CSolicitante(id_sol, nombre, pat, mat))
        cursor.close()
        conexion.close()
        return solicitantes