from flask_ory_auth.kratos.client import Authentication
from flask_ory_auth.hydra.client import HydraClient
from config import settings

authentication = Authentication(settings.KRATOS_API_URL)
oauth2 = HydraClient(settings.HYDRA_ADMIN_URL, settings.HYDRA_PUBLIC_URL)
