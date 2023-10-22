import 'package:flutter/material.dart';

void main() {
  runApp(
    MaterialApp(
      home: Scaffold(
        appBar: AppBar(
          title: Text('Logo + Imagens'),
        ),
        backgroundColor: Colors.white,
        body: Center(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.center,
            children: <Widget>[
              FlutterLogo(size: 100),

              Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: <Widget>[
                  Image.network('https://picsum.photos/250?image=10'),
                  Image.network('https://picsum.photos/250?image=25'),
                  Image.network('https://picsum.photos/250?image=15'),
                ],
              ),
            ],
          ),
        ),
      ),
    ),
  );
}
