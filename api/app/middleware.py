from flask import Request
from flask import Response


class OathkeeperMiddleware:
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):

        pass

