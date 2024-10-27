from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.models import db, Cliente

cliente_bp = Blueprint("clientes", __name__)

@cliente_bp.route("/clientes", methods=["POST"])
@jwt_required()
def create_cliente():

    cliente = request.json
    novo_cliente = Cliente(
        cliente_nome=cliente["cliente_nome"], cliente_email=cliente["cliente_email"]
    )
    db.session.add(novo_cliente)
    db.session.commit()

    return jsonify(
            {
                "id": novo_cliente.cliente_id,
                "nome": novo_cliente.cliente_nome,
                "email": novo_cliente.cliente_email,
            }
        ), 201
    


@cliente_bp.route("/clientes", methods=["GET"])
@jwt_required()
def list_clientes():
    clientes = Cliente.query.all()

    return (
        jsonify(
            [
                {"id": c.cliente_id, "nome": c.cliente_nome, "email": c.cliente_email}
                for c in clientes
            ]
        ),
        200,
    )


@cliente_bp.route("/clientes/<int:id>", methods=["GET"])
@jwt_required()
def find_cliente_by_id(id):
    cliente = Cliente.query.get(id)

    if not cliente:
        return jsonify({"Mensagem": "Cliente não encontrado"}), 404

    return (
        jsonify(
            {
                "Cliente encontrado": [
                    {
                        "id": cliente.cliente_id,
                        "nome": cliente.cliente_nome,
                        "email": cliente.cliente_email,
                    }
                ]
            }
        ),
        200,
    )


@cliente_bp.route("/clientes/<int:id>", methods=["PUT"])
@jwt_required()
def update_cliente(id):
    dados = request.json
    cliente = Cliente.query.get(id)

    if not cliente:
        return jsonify({"Mensagem": "Cliente não encontrado"}), 404

    if dados["cliente_nome"]:
        cliente.cliente_nome = dados["cliente_nome"]
    if dados["cliente_email"]:
        cliente.cliente_email = dados["cliente_email"]

    db.session.commit()

    return (
        jsonify(
            {
                "Cliente alterado": [
                    {
                        "id": cliente.cliente_id,
                        "nome": cliente.cliente_nome,
                        "email": cliente.cliente_email,
                    }
                ]
            }
        ),
        200,
    )


@cliente_bp.route("/clientes/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_cliente(id):

    cliente = Cliente.query.get(id)

    if not cliente:
        return jsonify({"Mensagem": "Cliente não encontrado"}), 404

    db.session.delete(cliente)
    db.session.commit()

    return jsonify({"Mensagem": "Cliente excluido"}), 200
