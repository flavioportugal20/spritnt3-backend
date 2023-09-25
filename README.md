# Minha API (Componente C)

Este projeto é parte do meu MVP da disciplina **Arquitetura de Software**.

Consiste em um back-end de um sistema de cadastro de visitantes, onde são disponibilidas rotas para obter, salvar, editar e excluir dados.

O projeto de cadastro de visitantes, permite criar um visitante e cadastrar o seu acesso, a fim de ter um controle de entrada de pessoas.

No cadastro de visitantes você pode criar, alterar, excluir e listar visitantes.

No cadastro de acessos você pode criar e listar acessos..

---

## Como executar

Será necessário ter todas as libs python listadas no `requirements.txt` instaladas.
Após clonar o repositório, é necessário ir ao diretório raiz, pelo terminal, para poder executar os comandos descritos abaixo.

> É fortemente indicado o uso de ambientes virtuais do tipo [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html).

```
(env)$ pip install -r requirements.txt
```

Este comando instala as dependências/bibliotecas, descritas no arquivo `requirements.txt`.

Para executar a API  basta executar:

```
(env)$ flask run --host 0.0.0.0 --port 5000
```

Em modo de desenvolvimento é recomendado executar utilizando o parâmetro reload, que reiniciará o servidor
automaticamente após uma mudança no código fonte.

```
(env)$ flask run --host 0.0.0.0 --port 5000 --reload
```

Abra o [http://localhost:5000/#/](http://localhost:5000/#/) no navegador para verificar o status da API em execução.

## Como executar através do Docker

Certifique-se de ter o [Docker](https://docs.docker.com/engine/install/) instalado e em execução em sua máquina.

Navegue até o diretório que contém o Dockerfile no terminal.
Execute **como administrador** o seguinte comando para construir a imagem Docker:

```
$ sudo docker build -t backend:1.0 .
```

Uma vez criada a imagem, para executar o container basta executar, **como administrador**, seguinte o comando:

```
$ sudo docker run --rm -p 5000:5000 backend:1.0
```

Uma vez executando, para acessar o front-end, basta abrir o [http://localhost:5000/#/](http://localhost:5000/#/) no navegador.
