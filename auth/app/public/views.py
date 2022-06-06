import random
import requests
import string

from flask import Blueprint, request, render_template, redirect
from flask import session, abort
from app.public.forms import Oauth2CreateForm, LoginForm, ConsentForm
from app.models import App
from app.security import oauth2
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
            owner_id=session.get('user_id'),
        )
        app.save()
        return redirect('/apps', code=302)

    return render_template('oauth/create_client.html', form=form)

@bp.route('/app/<id>', methods=['GET'])
def app_detail():
    return render_template('oauth/list_client.html')


@bp.route('/apps', methods=['GET'])
def apps_list():
    apps = App.query.filter(App.owner_id==session.get('user_id'))
    return render_template('oauth/list_client.html', apps=apps)


@bp.route('/login', methods=['GET'])
def login():
    form = LoginForm(request.args)
    if form.validate():
        data = oauth2.get_login_request(form.login_challenge.data)
        traits = session.get('traits')
        if not traits:
            traits = session.get('email')
        data = oauth2.accept_login_request(form.login_challenge.data, traits)
        return redirect(data.get('redirect_to'), code=302)

    return redirect(f"{settings.KRATOS_UI_URL}/login", code=302)


@bp.route('/consent', methods=['GET', 'POST'])
def consent():
    form = ConsentForm(request.form)
    if request.method == 'POST' and form.validate():
        data = oauth2.get_consent_request(form.consent_challenge.data)

        if form.submit.data == 'accept':
            accept = oauth2.accept_consent_request(
                form.consent_challenge.data,
                data.get('requested_scopes'),
                session.get('email'),
            )
            return redirect(accept.get('redirect_to'), code=302)

        if form.submit.data == 'reject':
            reject = oauth2.reject_consent_request(
                form.consent_challenge.data,
            )
            return redirect(reject.get('redirect_to'), code=302)

    challenge = request.args.get('consent_challenge')
    if not challenge:
        abort(403)

    data = oauth2.get_consent_request(challenge)
    app = App.query.filter(App.client_id==data.get('client').get('client_id')).first()

    return render_template(
        'oauth/consent.html', app=app,
        scopes=data.get('requested_scopes', []),
        challenge=challenge
    )



def generate_client_id():
    alphabet = string.ascii_lowercase + string.digits + string.ascii_uppercase
    return ''.join(random.choice(alphabet) for i in range(CLIENT_LENGTH))

