from flask import Flask, render_template
from mvc.controlador.EjemplarControlador import ejemplar_bp
from mvc.controlador.PrestamoControlador import prestamo_bp

app = Flask(__name__)
# Necesario para que funcionen los mensajes flash
app.secret_key = 'clave_secreta_para_flash_messages'

# Registrar blueprints
app.register_blueprint(ejemplar_bp)
app.register_blueprint(prestamo_bp)

@app.route("/")
def index():
    # Renderiza la plantilla base que contiene la navegación principal
    return render_template("base.html")

if __name__ == "__main__":
    app.run(debug=True, port=5000)