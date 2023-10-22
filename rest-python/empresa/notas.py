from flask import Flask, request, render_template_string

app = Flask(__name__)

@app.route('/avaliacoes')
def avaliacoes():
    nota1 = request.args.get('nota1')
    nota2 = request.args.get('nota2')
    nota3 = request.args.get('nota3')

    if nota1 is not None and nota2 is not None and nota3 is not None:
        try:
            nota1 = float(nota1)
            nota2 = float(nota2)
            nota3 = float(nota3)

            media = (nota1 + nota2 + nota3) / 3

            if 0 <= media < 3:
                mensagem = "REPROVADO"
            elif 3 <= media < 7:
                mensagem = "EXAME"
            else:
                mensagem = "APROVADO"
            return f'Média: {media:.2f}<br>{mensagem}'

        except ValueError:
            return 'Precisa inserir valores numéricos válidos para as notas!'
    
    return render_template_string('''
        <!DOCTYPE html>
        <html lang="pt-br">
            <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Comunicação Cliente-Servidor: Notas das Avaliações</title>
            <style>
                body{
                    background-color: #FFF;
                    color: #000;
                    font-family: sans-serif;
                }           
                                  
                input{
                    background-color: transparent;
                    border: 1px solid #000;
                    color: #000;
                    padding: 10px 20px;
                }

                #btnResult{
                    background-color: #000;
                    color: #FFF;
                    transition: all .4s ease;
                    cursor: pointer; 
                    padding: 10px 20px;
                }

                #btnResult:hover{
                    opacity: 50%;
                }               
            </style>                      
        </head>
        <body>
            <form action="/avaliacoes">
                <input type="text" name="nota1" placeholder="Nota 1 (0-10)">
                <input type="text" name="nota2" placeholder="Nota 2 (0-10)">
                <input type="text" name="nota3" placeholder="Nota 3 (0-10)">
                <input id="btnResult" type="submit" value="Calcular Média">
            </form>
        </body>
        </html>
    ''')

if __name__ == '__main__':
    app.run(debug=True)
