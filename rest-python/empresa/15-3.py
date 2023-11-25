from flask import Flask
from flask_restx import Api, Resource, reqparse, fields

app = Flask(__name__)
api = Api(app, version='1.0', title='Estoque API', description='API para gerenciar o estoque da empresa', doc='/doc', prefix='/doc')

# Dados iniciais do estoque
estoque = [
    {'codigo': 1, 'nome': 'Calça', 'quantidade': 12, 'preco': 89.94},
    {'codigo': 2, 'nome': 'Camisa', 'quantidade': 54, 'preco': 49.99},
    {'codigo': 3, 'nome': 'Saia', 'quantidade': 33, 'preco': 72.14},
    {'codigo': 4, 'nome': 'Sapato', 'quantidade': 12, 'preco': 99.11},
    {'codigo': 5, 'nome': 'Vestido', 'quantidade': 47, 'preco': 78.32}
]

# Definindo o modelo para os dados do estoque
estoque_model = api.model('Estoque', {
    'codigo': fields.Integer(readonly=True, description='Código do produto'),
    'nome': fields.String(required=True, description='Nome do produto'),
    'quantidade': fields.Integer(required=True, description='Quantidade em estoque'),
    'preco': fields.Float(required=True, description='Preço do produto (R$)')
})

# Parser para analisar os dados da requisição
parser = reqparse.RequestParser()
parser.add_argument('nome', type=str, help='Nome do produto')
parser.add_argument('quantidade', type=int, help='Quantidade em estoque')
parser.add_argument('preco', type=float, help='Preço do produto (R$)')

# Recurso para consultar, inserir e atualizar registros do estoque
@api.route('/estoque')
class EstoqueResource(Resource):

    @api.marshal_with(estoque_model, as_list=True)
    def get(self):
        """Consulta todos os registros do estoque."""
        return estoque

    @api.expect(parser)
    @api.marshal_with(estoque_model)
    def post(self):
        """Insere um novo registro no estoque."""
        args = parser.parse_args()
        novo_registro = {
            'codigo': len(estoque) + 1,
            'nome': args['nome'],
            'quantidade': args['quantidade'],
            'preco': args['preco']
        }
        estoque.append(novo_registro)
        return novo_registro, 201

@api.route('/estoque/<int:codigo>')
class ProdutoResource(Resource):

    @api.marshal_with(estoque_model)
    def get(self, codigo):
        """Consulta um registro específico do estoque pelo código."""
        for produto in estoque:
            if produto['codigo'] == codigo:
                return produto
        api.abort(404, message=f"Produto com código {codigo} não encontrado")

    @api.expect(parser)
    @api.marshal_with(estoque_model)
    def put(self, codigo):
        """Atualiza totalmente um registro do estoque."""
        for produto in estoque:
            if produto['codigo'] == codigo:
                args = parser.parse_args()
                produto.update({
                    'nome': args['nome'],
                    'quantidade': args['quantidade'],
                    'preco': args['preco']
                })
                return produto
        api.abort(404, message=f"Produto com código {codigo} não encontrado")

    @api.expect(parser)
    @api.marshal_with(estoque_model)
    def patch(self, codigo):
        """Atualiza parcialmente um registro do estoque."""
        for produto in estoque:
            if produto['codigo'] == codigo:
                args = parser.parse_args()
                if args['nome']:
                    produto['nome'] = args['nome']
                if args['quantidade']:
                    produto['quantidade'] = args['quantidade']
                if args['preco']:
                    produto['preco'] = args['preco']
                return produto
        api.abort(404, message=f"Produto com código {codigo} não encontrado")

    @api.response(204, 'Produto removido com sucesso')
    def delete(self, codigo):
        """Remove um registro do estoque."""
        for produto in estoque:
            if produto['codigo'] == codigo:
                estoque.remove(produto)
                return '', 204
        api.abort(404, message=f"Produto com código {codigo} não encontrado")

@api.route('/estoque-total')
class EstoqueTotalResource(Resource):

    def get(self):
        """Consulta o total em estoque de todos os produtos."""
        total = sum(produto['quantidade'] for produto in estoque)
        return {'estoque_total': total}

@api.route('/estoque-individual/<int:codigo>')
class EstoqueIndividualResource(Resource):

    def get(self, codigo):
        """Consulta o total em estoque de um produto isoladamente."""
        for produto in estoque:
            if produto['codigo'] == codigo:
                return {'estoque_individual': produto['quantidade']}
        api.abort(404, message=f"Produto com código {codigo} não encontrado")

@api.route('/estoque-menor')
class EstoqueMenorResource(Resource):

    def get(self):
        """Consulta o produto com menor quantidade no estoque."""
        produto_menor = min(estoque, key=lambda x: x['quantidade'])
        return {'produto_menor': produto_menor}

@api.route('/estoque-maior')
class EstoqueMaiorResource(Resource):

    def get(self):
        """Consulta o produto com maior quantidade no estoque."""
        produto_maior = max(estoque, key=lambda x: x['quantidade'])
        return {'produto_maior': produto_maior}

@api.route('/valor-total-estoque')
class ValorTotalEstoqueResource(Resource):

    def get(self):
        """Consulta o valor total no estoque."""
        valor_total = sum(produto['quantidade'] * produto['preco'] for produto in estoque)
        return {'valor_total_estoque': valor_total}

@api.route('/baixa-estoque/<int:codigo>')
class BaixaEstoqueResource(Resource):

    def put(self, codigo):
        """Realiza uma baixa de produto no estoque (venda)."""
        for produto in estoque:
            if produto['codigo'] == codigo:
                args = parser.parse_args()
                if args['quantidade'] and args['quantidade'] <= produto['quantidade']:
                    produto['quantidade'] -= args['quantidade']
                    return produto
                else:
                    api.abort(400, message="Quantidade inválida para baixa de estoque")
        api.abort(404, message=f"Produto com código {codigo} não encontrado")

@api.route('/entrada-estoque/<int:codigo>')
class EntradaEstoqueResource(Resource):

    def put(self, codigo):
        """Contabiliza a entrada de produto no estoque (compra)."""
        for produto in estoque:
            if produto['codigo'] == codigo:
                args = parser.parse_args()
                if args['quantidade']:
                    produto['quantidade'] += args['quantidade']
                    return produto
                else:
                    api.abort(400, message="Quantidade inválida para entrada de estoque")
        api.abort(404, message=f"Produto com código {codigo} não encontrado")

if __name__ == '__main__':
    app.run(debug=True)
