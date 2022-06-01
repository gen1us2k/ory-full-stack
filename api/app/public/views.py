from flask import Blueprint, request, render_template
from app.public.forms import Oauth2CreateForm


bp = Blueprint('bp', __name__, url_prefix='/', template_folder='templates')


@bp.route('/', methods=['GET'])
def index():
    return render_template('base.html')


@bp.route('/app/create', methods=['GET', 'POST'])
def create_app():
    form = Oauth2CreateForm(request.form)
    return render_template('oauth/create_client.html', form=form)
