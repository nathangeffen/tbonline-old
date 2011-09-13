'''Security and authentication middleware classes.

AutologoutMiddleware class to logout users after AUTO_LOGOUT_DELAY minutes have elapsed.
Taken from: http://djangosnippets.org/snippets/449/

WebfactionFixMiddleware class replaces REMOTE_ADDR with HTTP_X_FORWARDED_FOR.
Taken from 
http://docs.webfaction.com/software/django/troubleshooting.html?highlight=django%20remote%20addres#accessing-remote-addr

'''

from django.conf import settings
from django.contrib import auth
from datetime import datetime, timedelta

# Default AUTO_LOGOUT_DELAY TO 4 hours
AUTO_LOGOUT_DELAY = getattr(settings, "AUTO_LOGOUT_DELAY", 240)

class AutoLogoutMiddleware:
    
    def process_request(self, request):
        
        if not request.user.is_authenticated() :
            #Can't log out if not logged in
            try:
                del request.session['last_touch']
            except KeyError:
                pass
            return
        
        try:
            if datetime.now() - request.session['last_touch'] > timedelta( 0, AUTO_LOGOUT_DELAY * 60, 0):
                auth.logout(request)
                del request.session['last_touch']
                return
        except KeyError:
            pass

        request.session['last_touch'] = datetime.now()


class WebfactionFixMiddleware:
    """Sets 'REMOTE_ADDR' based on 'HTTP_X_FORWARDED_FOR', if the latter is
    set.

    Based on http://djangosnippets.org/snippets/1706/
    """
    def process_request(self, request):
        if 'HTTP_X_FORWARDED_FOR' in request.META:
            ip = request.META['HTTP_X_FORWARDED_FOR'].split(",")[0].strip()
            request.META['REMOTE_ADDR'] = ip
