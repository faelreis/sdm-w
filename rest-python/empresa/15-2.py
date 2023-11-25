from flask import Flask
from flask_restx import Api, Resource, reqparse, fields

app = Flask(__name__)
api = Api(app, version='1.0', title='Folha de Pagamento API', description='API para gerenciar a folha de pagamento da empresa', doc='/doc', prefix='/doc')

# Dados iniciais da folha de pagamento
folha_pagamento = [
    {'cpf': 1, 'nome': 'Ana', 'horas_trabalhadas': 8, 'valor_hora': 45.78},
    {'cpf': 2, 'nome': 'Bruna', 'horas_trabalhadas': 2, 'valor_hora': 60.00},
    {'cpf': 3, 'nome': 'Carlos', 'horas_trabalhadas': 10, 'valor_hora': 38.99},
    {'cpf': 4, 'nome': 'Diogo', 'horas_trabalhadas': 4, 'valor_hora': 45.78},
    {'cpf': 5, 'nome': 'Ester', 'horas_trabalhadas': 5, 'valor_hora': 45.78}
]

# Definindo o modelo para os dados da folha de pagamento
folha_pagamento_model = api.model('Folha de Pagamento', {
    'cpf': fields.Integer(readonly=True, description='CPF do colaborador'),
    'nome': fields.String(required=True, description='Nome do colaborador'),
    'horas_trabalhadas': fields.Integer(required=True, description='Horas trabalhadas'),
    'valor_hora': fields.Float(required=True, description='Valor da hora (R$)')
})

# Parser para analisar os dados da requisição
parser = reqparse.RequestParser()
parser.add_argument('nome', type=str, help='Nome do colaborador')
parser.add_argument('horas_trabalhadas', type=int, help='Horas trabalhadas')
parser.add_argument('valor_hora', type=float, help='Valor da hora (R$)')

# Recurso para consultar, inserir e atualizar registros da folha de pagamento
@api.route('/folha-pagamento')
class FolhaPagamentoResource(Resource):

    @api.marshal_with(folha_pagamento_model, as_list=True)
    def get(self):
        """Consulta todos os registros da folha de pagamento."""
        return folha_pagamento

    @api.expect(parser)
    @api.marshal_with(folha_pagamento_model)
    def post(self):
        """Insere um novo registro na folha de pagamento."""
        args = parser.parse_args()
        novo_registro = {
            'cpf': len(folha_pagamento) + 1,
            'nome': args['nome'],
            'horas_trabalhadas': args['horas_trabalhadas'],
            'valor_hora': args['valor_hora']
        }
        folha_pagamento.append(novo_registro)
        return novo_registro, 201

@api.route('/folha-pagamento/<int:cpf>')
class ColaboradorResource(Resource):

    @api.marshal_with(folha_pagamento_model)
    def get(self, cpf):
        """Consulta um registro específico da folha de pagamento pelo CPF."""
        for colaborador in folha_pagamento:
            if colaborador['cpf'] == cpf:
                return colaborador
        api.abort(404, message=f"Colaborador com CPF {cpf} não encontrado")

    @api.expect(parser)
    @api.marshal_with(folha_pagamento_model)
    def put(self, cpf):
        """Atualiza totalmente um registro da folha de pagamento."""
        for colaborador in folha_pagamento:
            if colaborador['cpf'] == cpf:
                args = parser.parse_args()
                colaborador.update({
                    'nome': args['nome'],
                    'horas_trabalhadas': args['horas_trabalhadas'],
                    'valor_hora': args['valor_hora']
                })
                return colaborador
        api.abort(404, message=f"Colaborador com CPF {cpf} não encontrado")

    @api.expect(parser)
    @api.marshal_with(folha_pagamento_model)
    def patch(self, cpf):
        """Atualiza parcialmente um registro da folha de pagamento."""
        for colaborador in folha_pagamento:
            if colaborador['cpf'] == cpf:
                args = parser.parse_args()
                if args['nome']:
                    colaborador['nome'] = args['nome']
                if args['horas_trabalhadas']:
                    colaborador['horas_trabalhadas'] = args['horas_trabalhadas']
                if args['valor_hora']:
                    colaborador['valor_hora'] = args['valor_hora']
                return colaborador
        api.abort(404, message=f"Colaborador com CPF {cpf} não encontrado")

    @api.response(204, 'Colaborador removido com sucesso')
    def delete(self, cpf):
        """Remove um registro da folha de pagamento."""
        for colaborador in folha_pagamento:
            if colaborador['cpf'] == cpf:
                folha_pagamento.remove(colaborador)
                return '', 204
        api.abort(404, message=f"Colaborador com CPF {cpf} não encontrado")

@api.route('/pagamento-total')
class PagamentoTotalResource(Resource):

    def get(self):
        """Consulta o valor total a ser pago."""
        total = sum(colaborador['horas_trabalhadas'] * colaborador['valor_hora'] for colaborador in folha_pagamento)
        return {'pagamento_total': total}

@api.route('/pagamento-menor')
class PagamentoMenorResource(Resource):

    def get(self):
        """Consulta o menor pagamento a ser realizado."""
        menor_pagamento = min(colaborador['horas_trabalhadas'] * colaborador['valor_hora'] for colaborador in folha_pagamento)
        return {'menor_pagamento': menor_pagamento}

@api.route('/pagamento-maior')
class PagamentoMaiorResource(Resource):

    def get(self):
        """Consulta o maior pagamento a ser realizado."""
        maior_pagamento = max(colaborador['horas_trabalhadas'] * colaborador['valor_hora'] for colaborador in folha_pagamento)
        return {'maior_pagamento': maior_pagamento}

if __name__ == '__main__':
    app.run(debug=True)