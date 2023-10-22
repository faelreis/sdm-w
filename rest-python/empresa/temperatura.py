from flask import Flask, request, render_template_string

app = Flask(__name__)

@app.route('/temperatura')
def temperatura():
    celsius = request.args.get('celsius')
    if celsius is not None:
        try:
            celsius = float(celsius)
            fahrenheit = (celsius * 1.8) + 32
            return f'A temperatura em Fahrenheit é: {fahrenheit:.2f}°F'
        except ValueError:
            return 'Por favor, insira um valor numérico válido para Celsius.'
    return render_template_string('''
        <!DOCTYPE html>
        <html lang="pt-br">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Comunicação Cliente-Servidor: Temperatura Celsius para Fahrenheit</title>
            <style>
                body{
                    background-color: #FFF;
                    color: #000;
                    font-family: sans-serif;
                }           
                                  
                #inputTemperature{
                    background-color: transparent;
                    border: 1px solid #000;
                    color: #000;
                    padding: 10px 20px;
                    width: 200px;
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
            <form action="/temperatura">
                <input id="inputTemperature" type="text" name="celsius" placeholder="Insira a temperatura em Celsius">
                <input id="btnResult" type="submit" value="Converter">
            </form>
        </body>
        </html>
    ''')

if __name__ == '__main__':
    app.run(debug=True)
