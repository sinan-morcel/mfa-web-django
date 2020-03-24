from django.apps import AppConfig
from django.conf import settings
import json

# fetch credentials
f = open(settings.BASE_DIR + '/credentials.json', "r")
# lines = f.readlines()
obj = json.load(f)
f.close()

class AccepttoMfaConfig(AppConfig):
    name = 'acceptto_mfa'
    # Acceptto MFA Integration
    mfa_app_uid = obj["uid"]
    mfa_app_secret = obj["secret"]
    mfa_site = "https://mfa.acceptto.com"
