# Reddit Clone example using Ory products (Kratos, Keto, Hydra, Oathkeeper)

The example is a simplified version of Reddit that shows example.

## Project structure

```
api - A Flask application that implements Reddit REST API using Flask-Restful. Uses Oauth.
auth - A Flask application that enables integration between Kratos and Hydra
hydra - Configuration folder for Ory Hydra
keto - Configuration folder for Ory Keto
kratos - Configuration folder for Ory Kratos
oathkeeper - Configuration folder for Ory Oathkeeper
```

## Running locally

You can use the following make commands to run it locally

```
all                            Runs everything (Flask apps, Kratos, Keto, Hydra and Oathkeeper)
down                           Shut downs everything
with_keto                      Runs flask apps with Keto
with_kratos                    Runs flask apps with Kratos
```

## Prerequisites

1. Docker
2. make
3. docker-compose
5. Python 3.10 and poetry (for local development without docker)

## Arhitecture

The example uses two flask applications: API and auth. API is secured by Oauth2 and requires `access_token`

### API Service
Exposes two public endpoints

1. /login to initialize Oauth2 login flow
2. /complete to complete Oauth2 login flow
3. /api group of CRUD like endpoints for Subreddit, Thread, comments models

### Auth Service

Auth service implements Oauth2 flows and makes requests to Hydra. Also, you can create Oauth2 apps to configure `API` service. Exposes the following endpoints

1. / - main page with `Create app` button
2. /app/create - create app webpage
3. /apps - list of created apps with needed information
4. /login - handles login request against Ory Hydra
5. /consent - handles consent request against Ory Hydra 

### Request flow

1. api/login generates oauth2 login url and redirects to Ory Hydra oauth2/auth endpoint
2. hydra/oauth2/auth endpoint initializes login flow and redirects to auth/login endpoint with generated `login_challenge`
3. auth/login accepts login request automatically agaist Ory Hydra and redirects to auth/consent page 
4. auth/consent page shows you consent screen with accept and reject request buttons. On the button click it sends request either accept request or reject request against Ory Hydra and redirects request to api/complete endpoint
5. api/complete takes `code` passed by consent screen, makes request to token endpoint, validates the `code` and passes json array as response with `id_token`, `access_token`, `refresh_token`

### Auth service
Auth service is responsible for authentication and authorization

1. Request lands the endpoint
2. Middleware checks if the user is authenticated against Ory Kratos
3. One can create oauth2 apps using simple frontend
4. Handles oauth2 flows and validates everything against Hydra

### API service
API service implements a simple CRUD-like REST API

1. Requires Tokens issued by Hydra passed within `Autorization` header
2. Middleware checks tokens against Ory Hydra


### Ory products

1. Ory Kratos is used as identity provider and implements login/registration flows for the project
2. Ory Keto implements a simple RBAC 
3. Ory oathkeeper and flask middlewares checks authentication/authorization for the service (You can use it either with middlewares or without by using oathkeeper)
