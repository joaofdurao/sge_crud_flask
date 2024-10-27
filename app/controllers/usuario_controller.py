from flask import Blueprint, request, jsonify
from app.models import db, Usuario
from flask_jwt_extended import create_access_token, jwt_required
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash


usuario_bp = Blueprint('usuarios', __name__)

@usuario_bp.route('/usuarios', methods=['POST'])
def create_usuario():

    usuario = request.json
    senha_hash = generate_password_hash(usuario['usuario_senha'])
    novo_usuario = Usuario(usuario_login=usuario['usuario_login'], usuario_senha=senha_hash)
    db.session.add(novo_usuario)
    db.session.commit()

    return jsonify(
        {
            'id': novo_usuario.usuario_id,
            'nome': novo_usuario.usuario_login            
        }), 201


@usuario_bp.route('/usuarios', methods=['GET'])
@jwt_required()
def list_usuarios():
    usuarios = Usuario.query.all()

    return jsonify([
        {
            'id': u.usuario_id, 
            'Nome': u.usuario_login, 
            'Senha': u.usuario_senha
        } for u in usuarios]), 200 

@usuario_bp.route('/usuarios/<int:id>', methods=['GET'])
@jwt_required()
def find_usuario_by_id(id):
    usuario = Usuario.query.get(id)
    
    if not usuario:
        return jsonify({'mensagem': 'Usuário não encontrado'}), 404
    
    return jsonify({'Usuario encontrado':[ 
            {
            'id': usuario.usuario_id,
            'nome': usuario.usuario_login            
        }
    ]}), 200

@usuario_bp.route('/usuarios/<int:id>', methods=['PUT'])
@jwt_required()
def update_usuario(id):
    dados = request.json
    usuario = Usuario.query.get(id)

    if not usuario:
        return jsonify({'mensagem': 'Usuário não encontrado'}), 404

    usuario.usuario_login = dados['usuario_login']
    db.session.commit()

    return jsonify({'Usuário alterado': usuario.usuario_login}), 200

@usuario_bp.route('/usuarios/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_usuario(id):
    
    usuario = Usuario.query.get(id)

    if not usuario:
        return jsonify({'mensagem': 'Usuário não encontrado'}), 404
    
    db.session.delete(usuario)
    db.session.commit()

    return jsonify({'mensagem':'Usuário excluido'}), 200

@usuario_bp.route('/login', methods=['POST'])
def login():
    dados = request.json
    usuario_login = dados.get('usuario_login')
    usuario_senha = dados.get('usuario_senha')

    usuario = Usuario.query.filter_by(usuario_login=usuario_login).first()

    if usuario and check_password_hash(usuario.usuario_senha, usuario_senha):
        access_token = create_access_token(identity=usuario.usuario_id)
        return jsonify(access_token=access_token), 200

    return jsonify({"mensagem": "Credenciais inválidas"}), 401