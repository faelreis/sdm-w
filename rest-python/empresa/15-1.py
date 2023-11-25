from flask import Flask
from flask_restx import reqparse, abort, Api, Resource, fields

app = Flask(__name__)
api = Api(
    app,
    version='1.0',
    title='API dos Produtos de uma Empresa',
    description='Permite gerenciar os registros dos produtos de uma empresa',
    doc='/doc',
    prefix='/doc'
)

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

campos_obrigatorios_para_atualizacao = api.model('Atualizaçao de Produto', {
    'id': fields.Integer(required=True, description='identificador do produto'),
    'nome': fields.String(required=True, description='nome do produto'),
    'preco': fields.Float(required=True, description='preço do produto'),
})

campos_obrigatorios_para_insercao = api.model('Inserção de Produto', {
    'id': fields.Integer(required=False, readonly=True, description='identificador do produto'),
    'nome': fields.String(required=True, description='nome do produto'),
    'preco': fields.Float(required=True, description='preço do produto'),
})

# Produto:
# 1) Apresenta um único produto.
# 2) Remove um único produto.
# 3) Atualiza (substitui) um produto.
@api.route('/produtos/<id>')
@api.doc(params={'id': 'identificador do produto'})
class Produto(Resource):

    @api.doc(responses={200: 'produto retornado'})
    def get(self, id):
        aborta_se_o_produto_nao_existe(id)
        return PRODUTOS[int(id)]

    @api.doc(responses={204: 'produto removido'})  # 204: No Content
    def delete(self, id):
        aborta_se_o_produto_nao_existe(id)
        del PRODUTOS[int(id)]
        return '', 204

    @api.doc(responses={200: 'produto substituído'})  # 200: OK
    @api.expect(campos_obrigatorios_para_atualizacao)
    def put(self, id):
        aborta_se_o_produto_nao_existe(id)
        args = parser.parse_args()
        for produto in PRODUTOS:
            if produto['id'] == int(id):
                produto['id'] = args['id']
                produto['nome'] = args['nome']
                produto['preco'] = args['preco']
                break
        return produto

# ListaProduto:
# 1) Apresenta a lista de produtos.
# 2) Insere um novo produto.
@api.route('/produtos')
class ListaProduto(Resource):

    @api.doc(responses={200: 'produtos retornados'})
    def get(self):
        return PRODUTOS

    @api.doc(responses={201: 'produto inserido'})  # 201: Created
    @api.expect(campos_obrigatorios_para_insercao)
    def post(self):
        args = parser.parse_args()
        id = -1
        for produto in PRODUTOS:
            if int(produto['id']) > id:
                id = int(produto['id'])
        id = id + 1
        produto = {'id': id, 'nome': args['nome'], 'preco': args['preco']}
        PRODUTOS.append(produto)
        return produto, 201

if __name__ == '__main__':
    app.run(debug=True)