import requests
from flask import Request, Response
from config import settings


class AuthenticationMiddleware:
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        request = Request(environ)
        resp = requests.get(
            f"{settings.KRATOS_API_URL}/sessions/whoami",
            cookies = request.cookies,
            headers = {"Authorization": request.headers.get("Authorization", "")},
        )
        if resp.status_code != 200:
            response = Response()
            response.status_code = 401
            return response(environ, start_response)
        return self.app(environ, start_response)


class AccessControlMiddlware:
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        return self.app(environ, start_response)
