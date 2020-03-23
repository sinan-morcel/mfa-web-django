from django.conf import settings
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User
import requests
import logging as log

class AccepttoMFABackend(BaseBackend):
  """
  Authenticate using the Acceptto MFA API using the UID and secret defined in the settings MFA_APP_UID and MFA_APP_SECRET.
  """
  def authenticate(self, request, username=None):
    app_uid = settings.MFA_APP_UID
    app_secret = settings.MFA_APP_SECRET
    mfa_site = settings.MFA_SITE

    payload = {
      "uid": app_uid,
      "secret": app_secret,
      "email": username,
      "message": "Would you like to login into Acceptto MFA enalbed Django Sample App?",
    }
    response = requests.post(mfa_site + "/api/v9/authenticate_with_options", data=payload)
    if (response.status_code == 200):  # success
      # create a new user in Django, if the user is not there already
      channel = response.json()["channel"]  # pass it somehow to the view
      try:
        user = User.objects.get(username=username)
      except User.DoesNotExist:
        # create a new user
        user = User(username=username)
        user.channel = channel  # pass the channel to the view's scope
        user.is_staff = False
        user.is_superuser = False
        user.save()
      return user
    elif response.status_code == 401:  # Email address provided is not a valid registered Acceptto account!
      return None
    elif response.status_code == 403:  # Invalid uid and secret combination, Application not found!
      # create a new user in Django, if the user is not there already
      log.error("The Application's UID or Secret were incorrect. Make sure that you have set them correctly in the site's settings.py file, or that you have created an application in the eGuardian® dashboard.")
      raise RuntimeError()  # just crash... for now
    else:  # other errors (shouldn't happen)
      log.error("An unexpected error occured.")
      raise RuntimeError() 

  def get_user(self, user_id):
    try:
      return User.objects.get(pk=user_id)
    except User.DoesNotExist:
      return None
