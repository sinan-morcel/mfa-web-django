# from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login
from django.urls import reverse
from django.conf import settings
import requests  # for web API requests
import logging as log
from django.contrib.auth.models import User
from acceptto_mfa.backends import AccepttoMFABackend
from acceptto_mfa.apps import AccepttoMfaConfig
from django.contrib.auth.decorators import login_required

from django.contrib import messages

from django.views import generic

# Create your views here.
def index_login_view(request):
  return render(request, 'acceptto_mfa/login.html')

def wait_view(request):
  username = request.POST['username']
  password = request.POST['password']
  user = authenticate(request, username=username, password=password)
  if user is not None: # the user is valid
    # don't login the user just yet, perform MFA
    print(user.accepttocredentials.mfa_email == '')
    if user.accepttocredentials.mfa_email is not '':  # if the email is set
      payload = {
        "uid": AccepttoMfaConfig.mfa_app_uid,
        "secret": AccepttoMfaConfig.mfa_app_secret,
        "email": user.accepttocredentials.mfa_email,
        "message": "Would you like to login into Acceptto MFA enalbed Django Sample App?",
      }
      response = requests.post(AccepttoMfaConfig.mfa_site + "/api/v9/authenticate_with_options", data=payload)
      if response.status_code == 200:  # success
        channel = response.json()["channel"]
        return render(request, 'acceptto_mfa/wait.html', {"channel": channel, "username": username})
      elif response.status_code == 401:  # Email address provided is not a valid registered Acceptto account!
        error_message = "The account is not registered with Acceptto."
        messages.add_message(request, messages.ERROR, error_message)
        return HttpResponseRedirect(reverse('acceptto_mfa:index_login'))
      elif response.status_code == 403:  # Invalid uid and secret combination, Application not found!
        raise RuntimeError("The Application's UID or Secret were incorrect. Make sure that you have set them correctly in the site's settings.py file, or that you have created an application in the eGuardian® dashboard.")  # just crash... for now
      else:  # other errors (shouldn't happen)
        log.warn("The MFA server returned an unexpected error code.")
        error_message = "An unexpected error occured."
        messages.add_message(request, messages.ERROR, error_message)
        return HttpResponseRedirect(reverse('acceptto_mfa:index_login'))
    else:
      login(request,user, 'django.contrib.auth.backends.ModelBackend')
      return HttpResponseRedirect(reverse('acceptto_mfa:dashboard', args=(username,)))
  else:
    error_message = "The username or password is incorrect."
    messages.add_message(request, messages.ERROR, error_message)
    return HttpResponseRedirect(reverse('acceptto_mfa:index_login'))

def auth_decision_view(request, username, channel):
  user = get_object_or_404(User, username=username)
  payload = {
    "uid": AccepttoMfaConfig.mfa_app_uid,
    "secret": AccepttoMfaConfig.mfa_app_secret,
    "email": user.accepttocredentials.mfa_email,
    "channel": channel,
  }
  response = requests.post(AccepttoMfaConfig.mfa_site + "/api/v9/check", data=payload)
  if (response.status_code == 200):  # success
    if (response.json()["status"] == "approved"):
      print("approved")
      login(request,user, 'django.contrib.auth.backends.ModelBackend')
      return HttpResponseRedirect(reverse('acceptto_mfa:dashboard', args=(username,)))
    elif (response.json()["status"] == "rejected"):
      error_message = "The authentication request was rejected."
      messages.add_message(request, messages.ERROR, error_message)
      return HttpResponseRedirect(reverse('acceptto_mfa:index_login'))
    elif (response.json()["status"] == "expired"):
      error_message = "The authentication request expired."
      messages.add_message(request, messages.ERROR, error_message)
      return HttpResponseRedirect(reverse('acceptto_mfa:index_login'))
    elif (response.json()["status"] == "pending" or response.json()["status"] == "null"):
      error_message = "The authentication request is pending."
      messages.add_message(request, messages.ERROR, error_message)
      return HttpResponseRedirect(reverse('acceptto_mfa:wait'))
    else:  # shouldn't happen
      error_message = "An unexpected server error happened. Please try again."
      messages.add_message(request, messages.ERROR, error_message)
      log.warn("The v9 MFA server returned an unsupported authentication status.") 
      return HttpResponseRedirect(reverse('acceptto_mfa:index_login'))
  elif (response.status_code == 401):  # Email address provided is not a valid registered Acceptto account!
    error_message = "Email address provided is not a valid registered Acceptto account!"
    messages.add_message(request, messages.ERROR, error_message)
    return HttpResponseRedirect(reverse('acceptto_mfa:index_login'))
  elif (response.status_code == 403):  # Invalid uid and secret combination, Application not found!
    # create a new user in Django, if the user is not there already
    raise RuntimeError("The Application's UID or Secret were incorrect. Make sure that you have set them correctly in the site's settings.py file, or that you have created an application in the eGuardian® dashboard.")  # just crash... for now
  else:
    error_message = "An unexpected server error happened. Please try again."
    messages.add_message(request, messages.ERROR, error_message)
    log.warn("The v9 MFA server returned an unsupported error code.") 
    return HttpResponseRedirect(reverse('acceptto_mfa:index_login'))

@login_required(login_url='/acceptto_mfa/login/')
def dashboard_view(request, username):
  return render(request, 'acceptto_mfa/dashboard.html', {"username": username})
