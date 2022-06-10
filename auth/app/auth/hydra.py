import ory_hydra_client
from ory_hydra_client.api import admin_api
from ory_hydra_client.model.accept_consent_request import AcceptConsentRequest
from ory_hydra_client.model.accept_login_request import AcceptLoginRequest
from ory_hydra_client.model.consent_request_session import ConsentRequestSession


class HydraClient:
    def __init__(self, admin_url, public_url):
        self.admin_url = admin_url
        self.public_url = public_url

    def get_login_request(self, login_challenge):
        conf = ory_hydra_client.Configuration(host=self.admin_url)

        with ory_hydra_client.ApiClient(conf) as api_client:
            api_instance = admin_api.AdminApi(api_client)
            return api_instance.get_login_request(login_challenge)

    def accept_login_request(self, login_challenge, traits):
        conf = ory_hydra_client.Configuration(host=self.admin_url)

        with ory_hydra_client.ApiClient(conf) as api_client:
            api_instance = admin_api.AdminApi(api_client)
            return api_instance.accept_login_request(
                login_challenge,
                accept_login_request=AcceptLoginRequest(
                    subject=traits,
                    remember=True,
                    remember_for=3600,
                ),
            )

    def get_consent_request(self, consent_challenge):
        conf = ory_hydra_client.Configuration(host=self.admin_url)

        with ory_hydra_client.ApiClient(conf) as api_client:
            api_instance = admin_api.AdminApi(api_client)
            return api_instance.get_consent_request(
                consent_challenge,
            )

    def accept_consent_request(self, consent_challenge, scope, identity_id):
        conf = ory_hydra_client.Configuration(host=self.admin_url)

        with ory_hydra_client.ApiClient(conf) as api_client:
            api_instance = admin_api.AdminApi(api_client)
            return api_instance.accept_consent_request(
                consent_challenge,
                accept_consent_request=AcceptConsentRequest(
                    # FIXME: Debug it and fix passing scope
                    # grant_scope=StringSlicePipeDelimiter(scope),
                    remember=True,
                    remember_for=3600,
                    session=ConsentRequestSession(id_token={"id": identity_id}),
                ),
            )

    def reject_consent_request(self, consent_challenge):
        conf = ory_hydra_client.Configuration(host=self.admin_url)

        with ory_hydra_client.ApiClient(conf) as api_client:
            api_instance = admin_api.AdminApi(api_client)
            return api_instance.reject_consent_request(consent_challenge)
