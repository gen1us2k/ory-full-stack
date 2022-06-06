from app.auth.kratos import Authentication
from app.auth.hydra import HydraClient
from config import settings
from oauthlib.oauth2 import WebApplicationClient


oauth2client = WebApplicationClient(settings.HYDRA_CLIENT_ID)
oauth2 = HydraClient(settings.HYDRA_ADMIN_URL, settings.HYDRA_PUBLIC_URL)
