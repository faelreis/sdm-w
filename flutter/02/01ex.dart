import 'package:flutter/material.dart';

void main() {
  String nomeDaPessoa = "Rafael";
  String diaDaSemana = "Sexta-feira";

  runApp(
    MaterialApp(
      home: Scaffold(
        appBar: AppBar(
          title: Text('Saudação'),
        ),
        backgroundColor: Colors.black,
        body: Center(
          child: RichText(
            textDirection: TextDirection.ltr,
            textAlign: TextAlign.center,
            text: TextSpan(
              children: <TextSpan>[
                TextSpan(
                  text: 'Olá, ',
                  style: TextStyle(
                    color: Colors.white,
                    fontSize: 18,
                  ),
                ),
                TextSpan(
                  text: nomeDaPessoa,
                  style: TextStyle(
                    color: Colors.red,
                    fontSize: 24,
                    fontWeight: FontWeight.bold,
                  ),
                ),
                TextSpan(
                  text: '!',
                  style: TextStyle(
                    color: Colors.white,
                    fontSize: 18,
                  ),
                ),
                TextSpan(
                  text: '\nHoje é $diaDaSemana.',
                  style: TextStyle(
                    color: Colors.white,
                    fontSize: 18,
                  ),
                ),
                TextSpan(
                  text: '\n\nExercício de estilos de textos',
                  style: TextStyle(
                    color: Colors.yellow,
                    fontSize: 18,
                  ),
                ),
                TextSpan(
                  text: '\n\n\nAplicação desenvolvida com Flutter!',
                  style: TextStyle(
                    color: Colors.purple,
                    fontSize: 18,
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
    ),
  );
}
