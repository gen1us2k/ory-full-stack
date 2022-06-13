from oauthlib.oauth2 import WebApplicationClient
from config import settings


oauth2client = WebApplicationClient(settings.HYDRA_CLIENT_ID)
