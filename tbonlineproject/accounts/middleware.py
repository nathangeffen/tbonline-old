'''AutologoutMiddleware class to logout users after AUTO_LOGOUT_DELAY minutes have elapsed.

Taken from: http://djangosnippets.org/snippets/449/
'''

from django.conf import settings
from django.contrib import auth
from datetime import datetime, timedelta

AUTO_LOGOUT_DELAY = getattr(settings, "AUTO_LOGOUT_DELAY", 60)

class AutoLogoutMiddleware:
    
    def process_request(self, request):
        if not request.user.is_authenticated() :
            #Can't log out if not logged in
            return

        try:
            if datetime.now() - request.session['last_touch'] > timedelta( 0, AUTO_LOGOUT_DELAY * 60, 0):
                auth.logout(request)
                del request.session['last_touch']
                return
        except KeyError:
            pass

        request.session['last_touch'] = datetime.now()
