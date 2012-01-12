from django.conf import settings
from django.utils.crypto import salted_hmac, constant_time_compare

class TokenGenerator(object):
    def make_token(self, user):
        return self._make_token(user)
    
    def _make_token(self, user):
        value = u'-'.join([unicode(user.id), unicode(user.last_login),
            user.password])
        return salted_hmac(settings.SECRET_KEY, value).hexdigest()[::2]
    
    def check_token(self, user, token):
        return constant_time_compare(token, self._make_token(user))
    
generator = TokenGenerator()