from flask import Blueprint, render_template, request, redirect, url_for, flash
from mvc.servicio.EjemplarServicio import EjemplarServicio
from mvc.servicio.LibroServicio import LibroServicio

ejemplar_bp = Blueprint('ejemplar', __name__)
ejemplar_servicio = EjemplarServicio()
libro_servicio = LibroServicio()

@ejemplar_bp.route("/ejemplares")
def gestionar_ejemplares():
    # La lógica POST para registrar se moverá a una ruta separada
    libros = libro_servicio.listar_libros()
    ejemplares = ejemplar_servicio.listar_ejemplares()
    return render_template("ejemplar.html", libros=libros, ejemplares=ejemplares)

# --- NUEVAS RUTAS PARA EL CRUD ---

@ejemplar_bp.route("/ejemplares/registrar", methods=["POST"])
def registrar_ejemplar():
    try:
        id_ejemplar = request.form["id_ejemplar"]
        isbn = request.form["isbn"]
        if id_ejemplar and isbn:
            ejemplar_servicio.registrar_ejemplar(id_ejemplar, isbn)
            flash(f"Ejemplar '{id_ejemplar}' registrado exitosamente.", "success")
        else:
            flash("El ID del ejemplar y el ISBN son obligatorios.", "danger")
    except Exception as e:
        flash(f"Error al registrar el ejemplar: {e}", "danger")
    return redirect(url_for('ejemplar.gestionar_ejemplares'))

@ejemplar_bp.route("/ejemplares/editar/<string:id_ejemplar>", methods=["GET", "POST"])
def editar_ejemplar(id_ejemplar):
    ejemplar = ejemplar_servicio.obtener_ejemplar_por_id(id_ejemplar)
    if not ejemplar:
        flash("Ejemplar no encontrado.", "danger")
        return redirect(url_for('ejemplar.gestionar_ejemplares'))

    if request.method == "POST":
        try:
            # El ID del ejemplar (clave primaria) no se cambia
            isbn_nuevo = request.form["isbn"]
            estado_nuevo = request.form["estado"]
            ejemplar_servicio.actualizar_ejemplar(id_ejemplar, isbn_nuevo, estado_nuevo)
            flash(f"Ejemplar '{id_ejemplar}' actualizado correctamente.", "success")
            return redirect(url_for('ejemplar.gestionar_ejemplares'))
        except Exception as e:
            flash(f"Error al actualizar el ejemplar: {e}", "danger")
    
    # Para el método GET, muestra el formulario de edición
    libros = libro_servicio.listar_libros()
    estados_posibles = ['Disponible', 'Prestado', 'En Reparacion', 'Extraviado']
    return render_template("editar_ejemplar.html", ejemplar=ejemplar, libros=libros, estados=estados_posibles)


@ejemplar_bp.route("/ejemplares/eliminar", methods=["POST"])
def eliminar_ejemplar():
    try:
        id_ejemplar = request.form["id_ejemplar"]
        exito = ejemplar_servicio.eliminar_ejemplar(id_ejemplar)
        if exito:
            flash(f"Ejemplar '{id_ejemplar}' eliminado correctamente.", "success")
        else:
            flash(f"No se pudo eliminar el ejemplar '{id_ejemplar}'. Es posible que esté actualmente prestado.", "danger")
    except Exception as e:
        flash(f"Error al eliminar el ejemplar: {e}", "danger")
    return redirect(url_for('ejemplar.gestionar_ejemplares'))