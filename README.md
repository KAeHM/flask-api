# flask-api
Uma Api usando Python e Flask retornando JSON integrando com duas APIs públicas e gratuitas. Esse projeto foi realizada ao fazer uma entrevista técnica para a empresa targetdata.


## Iniciando o projeto
O projeto foi feito com o docker compose, portanto é bem tranquilo inicia-lo. Mesmo assim vou fazer o passo a passo e algumas observações.

### Passo 1
Faça o clone do repositório na sua maquina utilizando o comando básico do git.

### Passo 2
Dentro da pasta do projeto suba a aplicação via docker compose. Aqui é importante se atentar a algumas coisas: O comando padrão para se subir uma aplicação pela primeira vez é utilizando o comando "docker compose up --build -d". 

Nesse caso a flag "-d" irá esconder o terminal que será mostrado e isso pode atrapalhar ao determinar quando o projeto estará pronto para ser utilizado. 

Quando o container do docker é iniciado, o container do elastisearch demora ainda alguns instantes para estar pronto para uso, se você executar qualquer requisição neste instante o server irá responder com um erro 500, isso faz o container ser encerrado, e você terá que reiniciar a aplicação por completo. 

Se você estiver utilizando a tag "-d", você deve aguardar, por segurança, no minimo 30 segundos após a inicialização do container, não deve demorar muito mais que isso. Agora se você não estiver utilizando, poderá ver que o container do "es" estará enviando alguns logs rapidamente, quando esses comandos terminarem de serem executados, a aplicação estará pronta para receber requisições!


### Observações 
Esse projeto utiliza o kibana sendo bom para se utilizar com o elasticsearch. Entretanto ele é bem robusto fazendo com que seja um projeto pesado, na documentação oficia o minimo de RAM para se rodar esse projeto é 4GB, portanto tenha em mente isso ao rodar na sua maquina.

Pegando com base, a minha maquina tem 8 GB, fica um pouco lento em alguns momentos mas eventualmente ele volta ao normal.
