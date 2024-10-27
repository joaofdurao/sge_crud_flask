from statistics import quantiles
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.models import db, Pedido, DetalhePedido, DetalhePedido

detalhe_pedido_bp = Blueprint("detalhepedidos", __name__)


@detalhe_pedido_bp.route("/detalhe_pedidos", methods=["POST"])
@jwt_required()
def create_detalhe_pedido():

    detalhe_pedido = request.json
    novo_detalhe_pedido = DetalhePedido(
        dp_quantidade=detalhe_pedido["dp_quantidade"],
        dp_preco=detalhe_pedido["dp_preco"],
        dp_desconto=detalhe_pedido["dp_desconto"],
        dp_pedido_id=detalhe_pedido["dp_pedido_id"],
        dp_produto_id=detalhe_pedido["dp_produto_id"]
    )
    db.session.add(novo_detalhe_pedido)
    db.session.commit()

    return (
        jsonify(
            {
                "id": novo_detalhe_pedido.dp_id,
                "quantidade": novo_detalhe_pedido.dp_quantidade,
                "preco": novo_detalhe_pedido.dp_preco,
                "desconto": novo_detalhe_pedido.dp_desconto,
                "pedido_id": novo_detalhe_pedido.dp_pedido_id,
                "produto_id": novo_detalhe_pedido.dp_produto_id,
            }
        ),
        201,
    )


@detalhe_pedido_bp.route("/detalhe_pedidos", methods=["GET"])
@jwt_required()
def list_detalhe_pedidos():
    detalhe_pedidos = DetalhePedido.query.all()

    return (
        jsonify(
            [
                {
                    "id": dp.dp_id,
                    "quantidade": dp.dp_quantidade,
                    "preco": dp.dp_preco,
                    "desconto": dp.dp_desconto,
                    "pedido_id": dp.dp_pedido_id,
                    "produto_id": dp.dp_produto_id,
                }
                for dp in detalhe_pedidos
            ]
        ),
        200,
    )


@detalhe_pedido_bp.route("/detalhe_pedidos/<int:id>", methods=["GET"])
@jwt_required()
def find_detalhe_pedido_by_id(id):
    detalhe_pedido = DetalhePedido.query.get(id)

    if not detalhe_pedido:
        return jsonify({"Mensagem": "DetalhePedido não encontrado"}), 404

    return (
        jsonify(
            {
                "DetalhePedido encontrado": [
                    {
                        "id": detalhe_pedido.dp_id,
                        "quantidade": detalhe_pedido.dp_quantidade,
                        "preco": detalhe_pedido.dp_preco,
                        "desconto": detalhe_pedido.dp_desconto,
                        "pedido_id": detalhe_pedido.dp_pedido_id,
                        "produto_id": detalhe_pedido.dp_produto_id,
                    }
                ]
            }
        ),
        200,
    )


@detalhe_pedido_bp.route("/detalhe_pedidos/<int:id>", methods=["PUT"])
@jwt_required()
def update_detalhe_pedido(id):
    dados = request.json
    detalhe_pedido = DetalhePedido.query.get(id)

    if not detalhe_pedido:
        return jsonify({"Mensagem": "DetalhePedido não encontrado"}), 404

    if dados["dp_quantidade"]:
        detalhe_pedido.dp_quantidade = dados["dp_quantidade"]
    if dados["dp_preco"]:
        detalhe_pedido.dp_preco = dados["dp_preco"]
    if dados["dp_desconto"]:
        detalhe_pedido.dp_desconto = dados["dp_desconto"]
    if dados["dp_pedido_id"]:
        detalhe_pedido.dp_pedido_id = dados["dp_pedido_id"]
    if dados["dp_produto_id"]:
        detalhe_pedido.dp_produto_id = dados["dp_produto_id"]

    db.session.commit()

    return (
        jsonify(
            {
                "DetalhePedido alterado": [
                    {
                        "id": detalhe_pedido.dp_id,
                        "quantidade": detalhe_pedido.dp_quantidade,
                        "preco": detalhe_pedido.dp_preco,
                        "desconto": detalhe_pedido.dp_desconto,
                        "pedido_id": detalhe_pedido.dp_pedido_id,
                        "produto_id": detalhe_pedido.dp_produto_id,
                    }
                ]
            }
        ),
        200,
    )


@detalhe_pedido_bp.route("/detalhe_pedidos/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_detalhe_pedido(id):

    detalhe_pedido = DetalhePedido.query.get(id)

    if not detalhe_pedido:
        return jsonify({"Mensagem": "DetalhePedido não encontrado"}), 404

    db.session.delete(detalhe_pedido)
    db.session.commit()

    return jsonify({"Mensagem": "DetalhePedido excluido"}), 200
