from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .produto import Produto
from .usuario import Usuario
from .cliente import Cliente
from .pedido import Pedido
from .detalhe_pedido import DetalhePedido