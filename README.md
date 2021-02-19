# Super OrgContact - Organização de Contatos

Projeto desenvolvido para seleção da Conecta Nuvem, utilizando [VueJS](https://vuejs.org/) para o build do frontend e [Flask](https://flask.palletsprojects.com/en/1.1.x/) como backend.

## Instalar dependências

Python:

    $ python -m venv env
    $ source env/bin/activate
    (env)$ pip install -r requirements.txt

Frontend:

    $ npm install

## Local run

Run the Vue.js frontend:

    $ npm run serve

Run the backend:

    (env)$ flask run

## Deploy

Frontend:

    $ npm run build

Deploy da aplicação no AppEngine:

    gcloud app deploy

> Para o deploy no AppEngine tenha ativo a People API e obtenha uma credencial OAuth 2.0 em  https://console.cloud.google.com/apis/credentials.
> Em seguida instale a credencial na raíz do projeto e informe o nome do arquivo .json gerado em [.env](.env), tendo como parâmetros da credencial:
> - scopes: https://www.googleapis.com/auth/contacts.readonly e https://www.googleapis.com/auth/userinfo.profile
> - redirect_uris: $URL_APP/api/login/callback