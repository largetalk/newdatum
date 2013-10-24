from django.utils.importlib import import_module
from django.conf import settings as django_settings
from django.contrib.sessions.middleware import SessionMiddleware

#application name
APP = getattr(django_settings, 'APP', None) or ''

#EXAM_SITE_ROOT_URL
EXAM_SITE_ROOT_URL = ('/entry', '/exam')
if django_settings.APPEND_SLASH:
    EXAM_SITE_ROOT_URL = ('/entry/', '/exam/')

URL_PREFIX = django_settings.FORCE_SCRIPT_NAME

#Old session cookie name
RAW_SESSION_COOKIE_NAME = django_settings.SESSION_COOKIE_NAME

def session_cookie(request):
    path = request.path.replace(URL_PREFIX, '', 1)
    return any([path.startswith(x) for x in EXAM_SITE_ROOT_URL]) \
            and '%s_exam_%s' % (APP, RAW_SESSION_COOKIE_NAME) \
            or  '%s_%s' % (APP, RAW_SESSION_COOKIE_NAME)

class SessionPatchMiddleware(SessionMiddleware):
    """
    A patch for distinguish between foreground and background admin sites
    """
    def process_request(self, request):  
        cookie_name = request.__SESSION_COOKIE__ = session_cookie(request) 
        engine = import_module(django_settings.SESSION_ENGINE)
        session_key = request.COOKIES.get(cookie_name, None)
        request.session = engine.SessionStore(session_key)
    
    def process_response(self, request, response):
        response = super(SessionPatchMiddleware, self).process_response(request, response)
        
        if RAW_SESSION_COOKIE_NAME in response.cookies :
            raw_cookie = response.cookies[RAW_SESSION_COOKIE_NAME]
            response.set_cookie(request.__SESSION_COOKIE__, 
                value    = raw_cookie.value,
                max_age  = raw_cookie.get('max_age', None),
                expires  = raw_cookie.get('expires', None), 
                domain   = raw_cookie['domain'],
                path     = raw_cookie['path'],
                secure   = raw_cookie.get('secure', None),
                httponly = raw_cookie.get('httponly', None)
            )
            del response.cookies[RAW_SESSION_COOKIE_NAME]
            
        return response
