from datetime import datetime, timedelta
from django.conf import settings
from django.contrib import auth
from SIP.views import *

class Suspendlogin:
  def process_request(self, request):
    if not request.user.is_authenticated() :
      #Can't log out if not logged in
      return

    try:
      if datetime.now() - request.session['lastaccess'] > timedelta( 0, settings.LOGOUT_TIME * 60, 0):
        
        del request.session['lastaccess']
        return logout(request)
    except KeyError:
      pass

    request.session['lastaccess'] = datetime.now()
