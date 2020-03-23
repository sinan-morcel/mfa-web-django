from django.conf import settings
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User

class AccepttoMFABackend(BaseBackend):
  """
  Authenticate using the Acceptto MFA API using the UID and secret defined in the settings MFA_APP_UID and MFA_APP_SECRET.
  """
  pass
