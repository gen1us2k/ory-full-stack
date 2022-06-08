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

The example uses two flask applications: API and auth

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
