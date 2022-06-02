from app.auth.kratos import Authentication
from app.auth.hydra import HydraClient
from config import settings

authentication = Authentication(settings.KRATOS_API_URL)
oauth2 = HydraClient(settings.HYDRA_ADMIN_URL, settings.HYDRA_PUBLIC_URL)
