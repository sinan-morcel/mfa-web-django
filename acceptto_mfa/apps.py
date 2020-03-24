from django.apps import AppConfig
from django.conf import settings

# fetch credentials
f = open(settings.BASE_DIR + '/credentials.txt', "r")
lines = f.readlines()
f.close()

class AccepttoMfaConfig(AppConfig):
    name = 'acceptto_mfa'
    # Acceptto MFA Integration
    mfa_app_uid = lines[0].strip()
    mfa_app_secret = lines[1].strip()
    mfa_site = "https://mfa.acceptto.com"

# override the authentication backend when this app is installed
settings.AUTHENTICATION_BACKENDS = ['acceptto_mfa.backends.AccepttoMFABackend']
