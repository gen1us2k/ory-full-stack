import json

import requests
from app.models import User
from flask import abort
from flask import request


class Authentication:
    def __init__(self, api_url):
        self.api_url = api_url

    def set_email_to_session(self, session) -> None:
        if session.get('email', None):
            return

        resp = requests.get(
            f"{self.api_url}/sessions/whoami",
            cookies=request.cookies,
            headers={"Authorization": request.headers.get("Authorization", "")},
        )
        if resp.status_code == 200:
            data = resp.json()
            traits = data.get("identity", {}).get("traits", {})
            session["email"] = traits.get("email")
            session["kratos_id"] = traits.get("id")
            session["traits"] = json.dumps(traits)

    def set_user_to_session(self, session) -> None:
        self.set_email_to_session(session)
        email = session.get("email", None)
        if not email:
            abort(403)

        user = User.query.filter(User.email == email).first()
        if not user:
            user = User(
                email=session.get('email'),
                kratos_id=session.get('kratos_id'),
            )
            user.save()

        session["user_id"] = user.id

    def get_current_user(self, session):
        user_id = session.get("user_id", None)
        if not user_id:
            abort(403)

        return user_id
