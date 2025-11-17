# Contenido completo y corregido para el archivo: mvc/modelo/cprestamo.py

from datetime import datetime, timedelta

from mvc.modelo.CEjemplar import CEjemplar
from mvc.modelo.CSolicitante import CSolicitante


class CPrestamo:
    def __init__(self, id_prestamo, ejemplar:CEjemplar, solicitante:CSolicitante, 
                 fecha_prestamo=None, fecha_devolucion_prevista=None, fecha_devolucion_real=None, dias_prestamo=15):
        """
        Inicializa el registro del préstamo.
        - Si no se proporcionan fechas, se crea un préstamo nuevo con la fecha actual.
        - Si se proporcionan fechas, se carga un préstamo existente (ej. desde la base de datos).
        """
        self.id_prestamo = id_prestamo
        self.ejemplar = ejemplar  # Referencia al objeto Ejemplar prestado
        self.solicitante = solicitante  # Referencia al objeto Solicitante

        # --- Lógica de fechas corregida ---
        if fecha_prestamo:
            # Si se proporciona una fecha_prestamo (cargando desde la BD), usamos los datos proporcionados.
            self.fecha_prestamo = fecha_prestamo
            self.fecha_devolucion_prevista = fecha_devolucion_prevista
            self.fecha_devolucion_real = fecha_devolucion_real
        else:
            # Si NO se proporciona fecha_prestamo, es un préstamo NUEVO y calculamos las fechas.
            self.fecha_prestamo = datetime.now()
            self.fecha_devolucion_prevista = self.fecha_prestamo + timedelta(days=dias_prestamo)
            self.fecha_devolucion_real = None

    def devolver(self):
        """Registra la devolución del ejemplar."""
        self.fecha_devolucion_real = datetime.now()
        # Es una buena práctica asegurarse de que el ejemplar exista antes de cambiar su estado
        if self.ejemplar:
            self.ejemplar.estado = "Disponible"
        print(f"Préstamo #{self.id_prestamo} devuelto exitosamente.")

    def __str__(self):
        """Representación en texto del préstamo."""
        estado_dev = "Activo" if not self.fecha_devolucion_real else "Devuelto"
        
        # Formatear fechas solo si no son nulas
        fecha_prevista_str = self.fecha_devolucion_prevista.strftime('%Y-%m-%d') if self.fecha_devolucion_prevista else "N/A"
        
        return (f"Préstamo #{self.id_prestamo} ({estado_dev}) | Ejemplar: {self.ejemplar.id_ejemplar} "
                f"| Solicitante: {self.solicitante.nombre} | Devolución Prevista: {fecha_prevista_str}")