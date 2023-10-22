import 'package:flutter/material.dart';

void main() => runApp(MaterialApp(home: Home()));

class Home extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        leading: const Icon(Icons.water),
        title: const Text('TrilhasApp'),
      ),
      body: Center(
        child: Container(
          constraints: BoxConstraints.expand(),
          child: Image.network(
            'https://media.giphy.com/media/pt0EKLDJmVvlS/giphy.gif',
            fit: BoxFit.cover,
          ),
        ),
      ),
      backgroundColor: Colors.blue[900],
      floatingActionButton: const FloatingActionButton(
        onPressed: null,
        tooltip: 'Adicionar nova trilha',
        child: Icon(Icons.add),
      ),
    );
  }
}
