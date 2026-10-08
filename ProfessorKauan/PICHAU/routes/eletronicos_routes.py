from flask import Blueprint, request

from controllers.eletronicos_controllers import create_eletronico, get_all_eletronicos_com_id, get_all_eletronicos

eletronicos_routes = Blueprint('eletronicos_routes',__name__)

@eletronicos_routes.route('/Eletronico', methods=['GET'])
def eletronico_get():
    return get_all_eletronicos()


@eletronicos_routes.route('/Eletronico/<int:id>', methods=['GET'])
def eletronico_get_por_id(id):
    return get_all_eletronicos_com_id(id)


@eletronicos_routes.route('/Eletronico', methods=['POST'])
def eletronicos_post():
    return create_eletronico(request.json)
