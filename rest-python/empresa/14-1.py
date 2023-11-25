from flask import Flask
from flask_restx import reqparse, abort, Api, Resource

app = Flask(__name__)
api = Api(app)

PRODUTOS = [
    {'id': 0, 'nome': 'sapato', 'preco': 128.55},
    {'id': 1, 'nome': 'camisa', 'preco': 49.89},
    {'id': 2, 'nome': 'calça', 'preco': 89.99},
    {'id': 3, 'nome': 'bermuda', 'preco': 78.63}
]

def aborta_se_o_produto_nao_existe(id):
    encontrei = False
    for produto in PRODUTOS:
        if produto['id'] == int(id):
            encontrei = True
    if not encontrei:
        abort(404, mensagem="O produto com id = {} não existe".format(id))  # 404: Not Found

# Parse dos dados enviados na requisição no formato JSON:
parser = reqparse.RequestParser()
parser.add_argument('id', type=int, help='identificador do produto')
parser.add_argument('nome', type=str, help='nome do produto')
parser.add_argument('preco', type=float, help='preço do produto')

# Produto:
# 1) Apresenta um único produto.
# 2) Remove um único produto.
# 3) Atualiza (substitui) um produto.
class Produto(Resource):
    def get(self, id):
        aborta_se_o_produto_nao_existe(id)
        return PRODUTOS[int(id)]

    def delete(self, id):
        aborta_se_o_produto_nao_existe(id)
        del PRODUTOS[int(id)]
        return '', 204  # 204: No Content

    def put(self, id):
        aborta_se_o_produto_nao_existe(id)
        args = parser.parse_args()
        for produto in PRODUTOS:
            if produto['id'] == int(id):
                produto['id'] = args['id']
                produto['nome'] = args['nome']
                produto['preco'] = args['preco']
                break
        return produto, 200  # 200: OK

# ListaProduto:
# 1) Apresenta a lista de produtos.
# 2) Insere um novo produto.
class ListaProduto(Resource):
    def get(self):
        return PRODUTOS

    def post(self):
        args = parser.parse_args()
        id = -1
        for produto in PRODUTOS:
            if int(produto['id']) > id:
                id = int(produto['id'])
        id = id + 1
        produto = {'id': id, 'nome': args['nome'], 'preco': args['preco']}
        PRODUTOS.append(produto)
        return produto, 201  # 201: Created

# Roteamento de recursos:
api.add_resource(Produto, '/produtos/<id>')
api.add_resource(ListaProduto, '/produtos')

if __name__ == '__main__':
    app.run(debug=True)
