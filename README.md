<h1 align="center">Caramelo Bot</h1>

<h3 align="center">
Um chatbot criado por discentes da Universidade Federal do Mato Grosso Do Sul para a ONG Amigo dos bichos.
</h3>

### Membros
- Anália Beatriz
- Daniel Yudi Carvalho
- Filipe Camuso Fernandez
- João Paulo Wakugawa
- Leonardo Oliveira

### Objetivo
- Desenvolver um projeto que auxilie a comunidade local com o conhecimento adquirido no estágio.

### Links
- <a href="https://trello.com/invite/b/hkxIKP57/0e6bf25c31d5218211d56ebc33c06306/sprint-5">Trello</a>
- <a href="https://docs.google.com/spreadsheets/d/1NYO1OVlJrjbIj-GFCXI5qa7sUbln-00VaZbEmgKcTWE/edit#gid=0">Daily Teams Avengers</a>

---

### Comandos do Rasa
```
$ rasa init            // Criando uma pasta com config iniciais
$ rasa train           // Treinando o modelo
    --fixed-model-name // Flag para gerar modelo com nome específico
$ rasa run actions     // Lembrar de reiniciar sempre que houver alterações
$ rasa shell           // Testando as funcionalidades do modelo
    -vv                // Flag para mostrar mais detalhes
$ rasa interactive     // Auxilia na definição de uma story 
$ rasa visualize       // Mostra um modelo visual do fluxo-conversa
```

### Comandos Okteto
```
$ okteto stack deploy --build // Buildando do docker-compose
```

### Configurando Pipeline
```
$ pip install spacy
$ python3 -m spacy download pt_core_news_md
```
