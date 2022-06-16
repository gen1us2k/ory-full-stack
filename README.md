# Ory full stack demo (Hydra, Kratos, Keto, Oathkeeper)

The example is a simplified version of Reddit.

## Project structure

```
api - A Flask application that implements Reddit REST API using Flask-Restful. Uses Oauth.
cli - Go client for the API that uses OpenID Connect for authentication
consent - A Flask application that enables integration between Kratos and Hydra
hydra - Configuration folder for Ory Hydra
keto - Configuration folder for Ory Keto
kratos - Configuration folder for Ory Kratos
oathkeeper - Configuration folder for Ory Oathkeeper
```

## Prerequisites

1. Docker
2. Go
3. make
4. docker-compose
5. Python 3.10 and poetry (for local development without docker)

## Arhitecture

The example uses two flask applications: API and consent. API is secured by Oauth2 and requires `access_token`

## CLI App

CLI App is a simple Go app that makes the following steps

1. Initializes oauth2 login flow 
2. Runs HTTP server with a callback handler on `:9999` port
3. Makes request to create Subreddit and Get all subreddits

### API Service
Exposes two public endpoints

1. /login to initialize Oauth2 login flow
2. /complete to complete Oauth2 login flow
3. /api group of CRUD like endpoints for Subreddit, Thread, comments models

### Consent Service

Consent service implements Oauth2 flows and makes requests to Hydra. Also, you can create Oauth2 apps to configure `API` service. Exposes the following endpoints

1. / - main page with `Create app` button
2. /app/create - create app webpage
3. /apps - list of created apps with needed information
4. /login - handles login request against Ory Hydra
5. /consent - handles consent request against Ory Hydra

### Request flow

1. CLI app generates oauth2 login URL and makes request to Ory Hydra `oauth2/auth` endpoint
2. Ory Hydra initializes login flow and redirects to `consent/login` endpoint with generated `login_challenge`
3. `consent/login` accepts login request automatically against Ory Hydra and redirects to `consent/consent` page
4. `consent/consent` page shows to a user a consent screen with `accept` and `reject` buttons. On the button click it sends request either to accept or to reject request against Ory Hydra and redirects to `cli/callback` url
5. CLI app checks token against Ory Hydra and gets `access_token` and `refresh_token`. It does not store it and for every run of the app a user needs to re-login.
6. CLI App makes requests to `api`

### Ory products

1. Ory Kratos is used as identity provider and implements login/registration flows for the project
2. Ory Keto implements a simple RBAC
3. Ory oathkeeper and flask middlewares checks authentication/authorization for the service (You can use it either with middlewares or without by using oathkeeper)



## Running locally
Prerequisites

1. Docker
2. docker-compose
3. make

```
  git clone git@github.com:gen1us2k/ory-full-stack
  cd ory-full-stack
  make all
```

You can use the following make commands to run it locally

```
all                            Runs everything (Flask apps, Kratos, Keto, Hydra and Oathkeeper)
down                           Shut downs everything
with_keto                      Runs flask apps with Keto
with_kratos                    Runs flask apps with Kratos
```


1. Open http://127.0.0.1:8080/apps
2. Create an account and login
3. Create an app (callback url value is http://127.0.0.1:9999/oauth/callback)
4. Run `python keto/create_policies.py` to create policies in Keto
5. Run `python keto/add_admin.py youremail` to grant admin permissions for yourself
6. Run `cd cli`
7. Use `CLIENT_ID` and `CLIENT_SECRET` environment variables to configure the CLI app
8. Run `go run cmd/cli/main.go`


## Configuration
### CLI
Environment variables

```
DISCOVERY_URL - an URL to openid-configuration. By Default http://127.0.0.1:4444/.well-known/openid-configuration
CLIENT_ID - Oauth2 client id
CLIENT_SECRET - Oauth2 client secret
API_URL - an URL to API service. By default http://127.0.0.1:5000
SKIP_TLS - Configuration for HTTP transport to skip TLS verification. By default is true
```

### API

You can check environment variables in `/api/config/settings.py` file

### Consent

You can check environment variables in `/api/config/settings.py` file

## Ory 
### Keto

Policies and groups. For the advanced RBAC configuration you can check [this guide](https://www.ory.sh/docs/keto/guides/rbac)

```
app:subreddit#edit@(groups:admin#member)
app:subreddit#create@(groups:admin#member)
app:subreddit#delete@(groups:admin#member)
app:subreddit#edit@(groups:moderator#member)
app:subreddit#create@(groups:moderator#member)
```

### Oathkeeper

Oathkeeper proxies only authenticated requests to `api` and `consent` services. It uses `cookie_session` authenticator to check authentication. Check `oathkeeper/access-rules.yml` for additional information

## Contribute

Feel free to [open a discussion](https://github.com/ory/examples/discussions/new) to provide feedback or talk about ideas, or
[open an issue](https://github.com/ory/examples/issues/new) if you want to add your example to the repository or encounter a bug.
You can contribute to Ory in many ways, see the [Ory Contributing Guidelines](https://www.ory.sh/docs/ecosystem/contributing) for
more information.


