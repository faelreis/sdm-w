import 'package:flutter/material.dart';

void main() {
  runApp(
    MaterialApp(
      home: Scaffold(
        appBar: AppBar(
          title: Text('Imagens'),
        ),
        backgroundColor: Colors.black,
        body: Center(
          child: Row(
            mainAxisAlignment: MainAxisAlignment.center,
            children: <Widget>[
              Image.network('https://picsum.photos/250?image=10'),
              Image.network('https://picsum.photos/250?image=25'),
              Image.network('https://picsum.photos/250?image=15'),
            ],
          ),
        ),
      ),
    ),
  );
}
