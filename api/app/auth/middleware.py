import random
import string

import requests
from app.security import oauth2client
from config import settings
from flask import Request
from flask import Response


class IntrospectionMiddleware:
    def __init__(self, app):
        self.app = app

    def get_access_token(self, request):
        header = request.headers.get("Authorization")
        if not header:
            return
        parts = header.split()
        if len(parts) != 2:
            access_token = request.args.get("access_token", "")
            if access_token:
                return access_token
            access_token = request.form.get("access_token", "")
            if access_token:
                return access_token

        return parts[1]

    def generate_state(self):
        alphabet = string.ascii_lowercase + string.digits + string.ascii_uppercase
        return ''.join(random.choice(alphabet) for i in range(32))

    def __call__(self, environ, start_response):
        request = Request(environ)
        token = self.get_access_token(request)

        if request.path.startswith("/complete"):
            return self.app(environ, start_response)

        if not token:
            cfg = requests.get(settings.HYDRA_DISCOVERY_URL).json()

            uri = oauth2client.prepare_request_uri(
                cfg['authorization_endpoint'],
                redirect_uri='http://127.0.0.1:5000/complete',
                scope=settings.HYDRA_SCOPE,
                state=self.generate_state(),
            )
            response = Response()
            response.status_code = 302
            response.headers = [("Location", uri)]
            return response(environ, start_response)

        resp = requests.post(
            f"{settings.HYDRA_ADMIN_URL}/oauth2/introspect",
            data={
                "scope": settings.HYDRA_SCOPE,
                "token": token,
            },
        )
        print(resp.json(), flush=True)
        if resp.status_code != 200:
            response = Response()
            response.status_code = 302
            response.headers = [("Location", settings.KRATOS_UI_URL)]
            return response(environ, start_response)

        if resp.json().get('active', False):
            # FIXME: Handle it
            pass

        return self.app(environ, start_response)


class AccessControlMiddlware:
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        return self.app(environ, start_response)
