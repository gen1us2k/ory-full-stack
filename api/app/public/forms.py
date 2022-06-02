from wtforms import Form, BooleanField, StringField, PasswordField, validators


class Oauth2CreateForm(Form):
    app_name = StringField(
        'App Name', [validators.DataRequired()],
        render_kw={"placeholder": "App Name"}
    )
    description = StringField(
        'App Description', [validators.DataRequired()],
        render_kw={"placeholder": "App Description"}
    )
    website_url = StringField(
        'Website URL', [validators.URL()],
        render_kw={"placeholder": "WebSite URL"}
    )
    callback_url = StringField(
        'Callback URL', [validators.URL()],
        render_kw={"placeholder": "Callback URL"}
    )


class LoginForm(Form):
    login_challenge = StringField('Login Challenge', [validators.DataRequired()])
