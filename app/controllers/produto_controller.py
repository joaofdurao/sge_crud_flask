from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.models import db, Produto

produto_bp = Blueprint("produtos", __name__)


@produto_bp.route('/produtos', methods=['POST'])
@jwt_required()
def create_produto():

    produto = request.json
    novo_produto = Produto(produto_nome=produto['produto_nome'], produto_preco=produto['produto_preco'])
    db.session.add(novo_produto)
    db.session.commit()

    return jsonify(
        {
            'id': novo_produto.produto_id,
            'nome': novo_produto.produto_nome            
        }), 201


@produto_bp.route('/produtos', methods=['GET'])
@jwt_required()
def list_produtos():
    produtos = Produto.query.all()

    return jsonify([
        {
            'id': p.produto_id, 
            'nome': p.produto_nome, 
            'preco': p.produto_preco
        } for p in produtos]), 200 

@produto_bp.route('/produtos/<int:id>', methods=['GET'])
@jwt_required()
def find_produto_by_id(id):
    produto = Produto.query.get(id)
    
    if not produto:
        return jsonify({'Mensagem': 'Produto não encontrado'}), 404
    
    return jsonify({'Produto encontrado':[
            {
                'id': produto.produto_id,
                'nome': produto.produto_nome
            }
        ]}), 200

@produto_bp.route('/produtos/<int:id>', methods=['PUT'])
@jwt_required()
def update_produto(id):
    dados = request.json
    produto = Produto.query.get(id)

    if not produto:
        return jsonify({'Mensagem': 'Produto não encontrado'}), 404

    if dados['produto_nome']:
        produto.produto_nome = dados['produto_nome']
    if dados['produto_preco']:
        produto.produto_preco = dados['produto_preco'] 
    
    db.session.commit()

    return jsonify(
        {
            'Produto alterado':[
            {
                'id': produto.produto_id,
                'nome': produto.produto_nome
            }]
        }), 200

@produto_bp.route('/produtos/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_produto(id):
    
    produto = Produto.query.get(id)

    if not produto:
        return jsonify({'Mensagem': 'Produto não encontrado'}), 404
    
    db.session.delete(produto)
    db.session.commit()

    return jsonify(
        {
            'Mensagem':'Produto excluido'
        }), 200