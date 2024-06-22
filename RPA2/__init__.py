from flask import Flask

def create_app():
    app = Flask(__name__)

    # Configuración de la aplicación
    app.config.from_mapping(
        SECRET_KEY='your_secret_key',
        # Otras configuraciones
    )

    # Importar y registrar Blueprints, si los tienes
    from . import app as app_blueprint
    app.register_blueprint(app_blueprint)

    return app