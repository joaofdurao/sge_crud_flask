from flask import Blueprint, request, jsonify
from datetime import datetime

from flask_jwt_extended import jwt_required
from app.models import db, Pedido

pedido_bp = Blueprint("pedidos", __name__)


@pedido_bp.route("/pedidos", methods=["POST"])
@jwt_required()
def create_pedido():

    pedido = request.json
    novo_pedido = Pedido(
        data_compra=datetime.strptime(pedido["data_compra"], '%Y-%m-%d'), cliente_id=pedido["cliente_id"]
    )
    db.session.add(novo_pedido)
    db.session.commit()

    return (
        jsonify(
            {
                "id": novo_pedido.pedido_id,
                "data_compra": datetime.strftime(novo_pedido.data_compra, '%Y-%m-%d'),
                "cliente_id": novo_pedido.cliente_id,
            }
        ),
        201,
    )


@pedido_bp.route("/pedidos", methods=["GET"])
@jwt_required()
def list_pedidos():
    pedidos = Pedido.query.all()

    return (
        jsonify(
            [
                {
                    "id": p.pedido_id,
                    "data_compra": datetime.strftime(p.data_compra, '%Y-%m-%d'),
                    "cliente_id": p.cliente_id,
                }
                for p in pedidos
            ]
        ),
        200,
    )


@pedido_bp.route("/pedidos/<int:id>", methods=["GET"])
@jwt_required()
def find_pedido_by_id(id):
    pedido = Pedido.query.get(id)

    if not pedido:
        return jsonify({"Mensagem": "Pedido não encontrado"}), 404

    return (
        jsonify(
            {
                "Pedido encontrado": [
                    {
                        "id": pedido.pedido_id,
                        "data_compra": datetime.strftime(pedido.data_compra, '%Y-%m-%d'),
                        "cliente_id": pedido.cliente_id,
                    }
                ]
            }
        ),
        200,
    )


@pedido_bp.route("/pedidos/<int:id>", methods=["PUT"])
@jwt_required()
def update_pedido(id):
    dados = request.json
    pedido = Pedido.query.get(id)

    if not pedido:
        return jsonify({"Mensagem": "Pedido não encontrado"}), 404

    if dados["data_compra"]:
        pedido.data_compra = datetime.strptime(dados["data_compra"], '%Y-%m-%d')
    if dados["cliente_id"]:
        pedido.cliente_id = dados["cliente_id"]

    db.session.commit()

    return (
        jsonify(
            {
                "Pedido alterado": [
                    {
                        "id": pedido.pedido_id,
                        "data_compra": datetime.strftime(pedido.data_compra, '%Y-%m-%d'),
                        "cliente_id": pedido.cliente_id,
                    }
                ]
            }
        ),
        200,
    )


@pedido_bp.route("/pedidos/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_pedido(id):

    pedido = Pedido.query.get(id)

    if not pedido:
        return jsonify({"Mensagem": "Pedido não encontrado"}), 404

    db.session.delete(pedido)
    db.session.commit()

    return jsonify({"Mensagem": "Pedido excluido"}), 200
