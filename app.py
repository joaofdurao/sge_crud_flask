from flask import Flask
from flask_jwt_extended import JWTManager
from app.models import db
from config import Config
from app.controllers.produto_controller import produto_bp
from app.controllers.usuario_controller import usuario_bp
from app.controllers.cliente_controller import cliente_bp
from app.controllers.pedido_controller import pedido_bp
from app.controllers.detalhe_pedido_controller import detalhe_pedido_bp

def criar_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    JWTManager(app)
    db.init_app(app)
    
    with app.app_context():
        db.create_all()
    
    app.register_blueprint(usuario_bp)
    app.register_blueprint(produto_bp)
    app.register_blueprint(cliente_bp)
    app.register_blueprint(pedido_bp)
    app.register_blueprint(detalhe_pedido_bp)

    app.run(debug=True)

if __name__ == '__main__':
    app = criar_app()