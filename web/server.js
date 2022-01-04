// Instânciando express
const express = require('express');
const app = express();

// Rota que retorna como resposta a página index.html
app.get('/', (req, res) => {
  res.sendFile(__dirname + '/index.html');
});

// Definindo a porta onde o servidor escutará as requisições
const port = process.env.PORT || 8080;
app.listen(port, () => {
  console.log('Server ON | Port:', port);
});