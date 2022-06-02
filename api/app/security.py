from app.auth.kratos import Authentication
from config import settings

authentication = Authentication(settings.KRATOS_API_URL)
