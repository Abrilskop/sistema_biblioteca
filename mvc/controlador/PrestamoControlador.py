from flask import Blueprint, render_template, request, redirect, url_for, flash
from mvc.servicio.PrestamoServicio import PrestamoServicio
from mvc.servicio.SolicitanteServicio import SolicitanteServicio
from mvc.servicio.EjemplarServicio import EjemplarServicio

prestamo_bp = Blueprint('prestamo', __name__)
prestamo_servicio = PrestamoServicio()
solicitante_servicio = SolicitanteServicio()
ejemplar_servicio = EjemplarServicio()

@prestamo_bp.route("/prestamos", methods=["GET", "POST"])
def gestionar_prestamos():
    if request.method == "POST":
        try:
            if 'registrar' in request.form:
                id_ejemplar = request.form["id_ejemplar"]
                id_solicitante = request.form["id_solicitante"]
                prestamo_servicio.registrar_prestamo(id_ejemplar, id_solicitante)
                flash("Préstamo registrado exitosamente.", "success")
            elif 'devolver' in request.form:
                id_prestamo = request.form["id_prestamo"]
                prestamo_servicio.registrar_devolucion(int(id_prestamo))
                flash(f"Devolución del préstamo #{id_prestamo} registrada.", "success")
        except Exception as e:
            flash(f"Error al procesar la solicitud: {e}", "danger")
        return redirect(url_for('prestamo.gestionar_prestamos'))

    prestamos_activos = prestamo_servicio.listar_prestamos(solo_pendientes=True)
    todos_ejemplares = ejemplar_servicio.listar_ejemplares()
    ejemplares_disponibles = [e for e in todos_ejemplares if e.estado == 'Disponible']
    solicitantes_activos = solicitante_servicio.listar_solicitantes_activos()
    return render_template("prestamo.html", prestamos=prestamos_activos, ejemplares=ejemplares_disponibles, solicitantes=solicitantes_activos)

# --- NUEVA RUTA PARA EL HISTORIAL ---
@prestamo_bp.route("/prestamos/historial")
def historial_prestamos():
    # Llamamos al servicio para obtener TODOS los préstamos (pendientes y devueltos)
    todos_los_prestamos = prestamo_servicio.listar_prestamos(solo_pendientes=False)
    return render_template("historial_prestamos.html", prestamos=todos_los_prestamos)