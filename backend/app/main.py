from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager

def create_app():
    app = Flask(__name__)

    app.config["JWT_SECRET_KEY"] = "dev-secret"
    CORS(app, supports_credentials=True)
    JWTManager(app)

    # ROUTES
    from routes.auth import auth_bp
    from routes.booking import booking_bp
    from routes.cabinet import cabinet_bp
    from routes.admin import admin_bp

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(booking_bp, url_prefix="/api/bookings")
    app.register_blueprint(cabinet_bp, url_prefix="/api/cabinet")
    app.register_blueprint(admin_bp, url_prefix="/api/admin")

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
