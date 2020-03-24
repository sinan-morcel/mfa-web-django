from django.conf import settings
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User
import requests
import logging as log
from acceptto_mfa.apps import AccepttoMfaConfig

class AccepttoMFABackend(BaseBackend):
  """
  Authenticate using the Acceptto MFA API using the UID and secret defined in the settings MFA_APP_UID and MFA_APP_SECRET.

  This authentication backend simply makes sure the user is a valid Acceptto user registered in the app. This backend can be extended to include password authentication or other forms of authentication which can compelement the MFA service.
  """
  def authenticate(self, request, username=None):
    app_uid = AccepttoMfaConfig.mfa_app_uid
    app_secret = AccepttoMfaConfig.mfa_app_secret
    payload = {
      "uid": app_uid,
      "secret": app_secret,
      "email": username,
    }
    response = requests.post(AccepttoMfaConfig.mfa_site + "/api/v9/is_user_valid", data=payload)
    if (response.status_code == 200):  # success
      if (response.json()["valid"] == True):
        # create a new user in Django, if the user is not there already
        try:
          user = User.objects.get(username=username)
        except User.DoesNotExist:
          # create a new user (we assume they're not staff or superusers)
          user = User(username=username)
          user.is_staff = False
          user.is_superuser = False
          user.save()
        return user
      else:
        log.warn("The user's registration didn't finish yet, or the user is not valid.")
        return None
    elif response.status_code == 401:  # Email address provided is not a valid registered Acceptto account!
      return None
    elif response.status_code == 403:  # Invalid uid and secret combination, Application not found!
      raise RuntimeError("The Application's UID or Secret were incorrect. Make sure that you have set them correctly in the site's settings.py file, or that you have created an application in the eGuardian® dashboard.")  # just crash... for now
    else:  # other errors (shouldn't happen)
      log.warn("The MFA server returned an unexpected error code.")
      return None

  def get_user(self, user_id):
    try:
      return User.objects.get(pk=user_id)
    except User.DoesNotExist:
      return None
