from flask import Flask
from flask_restx import Api, Resource

app = Flask(__name__)
api = Api(app)

# Dados da folha de pagamento
folha_pagamento = [
    {'CPF': 1, 'Nome': 'Ana', 'HorasTrabalhadas': 8, 'ValorHora': 45.78},
    {'CPF': 2, 'Nome': 'Bruna', 'HorasTrabalhadas': 2, 'ValorHora': 60.00},
    {'CPF': 3, 'Nome': 'Carlos', 'HorasTrabalhadas': 10, 'ValorHora': 38.99},
    {'CPF': 4, 'Nome': 'Diogo', 'HorasTrabalhadas': 4, 'ValorHora': 45.78},
    {'CPF': 5, 'Nome': 'Ester', 'HorasTrabalhadas': 5, 'ValorHora': 45.78},
]

class FolhaPagamentoResource(Resource):
    def get(self):
        return folha_pagamento

class PagamentoColaboradoresResource(Resource):
    def get(self):
        pagamentos = [{'Nome': registro['Nome'], 'Pagamento': registro['HorasTrabalhadas'] * registro['ValorHora']} for registro in folha_pagamento]
        return pagamentos

class MenorPagamentoResource(Resource):
    def get(self):
        menor_pagamento = min(folha_pagamento, key=lambda x: x['HorasTrabalhadas'] * x['ValorHora'])
        return menor_pagamento

class MaiorPagamentoResource(Resource):
    def get(self):
        maior_pagamento = max(folha_pagamento, key=lambda x: x['HorasTrabalhadas'] * x['ValorHora'])
        return maior_pagamento

class ValorTotalResource(Resource):
    def get(self):
        valor_total = sum(registro['HorasTrabalhadas'] * registro['ValorHora'] for registro in folha_pagamento)
        return {'ValorTotal': valor_total}

# Adicionando os recursos à API
api.add_resource(FolhaPagamentoResource, '/folha-pagamento')
api.add_resource(PagamentoColaboradoresResource, '/pagamento-colaboradores')
api.add_resource(MenorPagamentoResource, '/menor-pagamento')
api.add_resource(MaiorPagamentoResource, '/maior-pagamento')
api.add_resource(ValorTotalResource, '/valor-total')

if __name__ == '__main__':
    app.run(debug=True)
