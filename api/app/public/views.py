import random
import requests
import string

from flask import Blueprint, request, render_template, redirect
from app.public.forms import Oauth2CreateForm
from app.models import App
from config import settings


bp = Blueprint('bp', __name__, url_prefix='/', template_folder='templates')
CLIENT_LENGTH = 32

@bp.route('/', methods=['GET'])
def index():
    return render_template('base.html')


@bp.route('/app/create', methods=['GET', 'POST'])
def create_app():
    form = Oauth2CreateForm(request.form)
    if request.method == 'POST' and form.validate():
        client_id = generate_client_id()
        resp = requests.post(
            f"{settings.HYDRA_ADMIN_URL}/clients",
            json={
                "client_id": client_id,
                "client_name": form.app_name.data,
                "grant_types": ["authorization_code", "refresh_token"],
                "redirect_uris": [form.callback_url.data],
                "response_types": ["code", "id_token"],
                "scope": "openid offline",
            },
        )

        if resp.status_code != 201:
            return render_template('oauth/create_client.html', form=form)

        data = resp.json()
        app = App(
            name=form.app_name.data,
            description=form.description.data,
            website_url=form.website_url.data,
            client_id=client_id,
            client_secret=data.get('client_secret'),
            callback_url=form.callback_url.data,
        )
        app.save()
        return redirect('/apps', code=302)

    return render_template('oauth/create_client.html', form=form)

@bp.route('/app/<id>', methods=['GET'])
def app_detail():
    pass

@bp.route('/apps', methods=['GET'])
def apps_list():
    pass


def generate_client_id():
    alphabet = string.ascii_lowercase + string.digits + string.ascii_uppercase
    return ''.join(random.choice(alphabet) for i in range(CLIENT_LENGTH))

