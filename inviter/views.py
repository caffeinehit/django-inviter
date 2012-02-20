# Create your views here.
from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponseRedirect, HttpResponseForbidden
from django.utils import importlib
from django.utils.functional import LazyObject
from django.utils.http import base36_to_int
from django.views.generic.base import TemplateView


FORM = getattr(settings, 'INVITER_FORM', 'inviter.forms.RegistrationForm')
REDIRECT = getattr(settings, 'INVITER_REDIRECT', 'inviter:done')
TOKEN_GENERATOR = getattr(settings, 'INVITER_TOKEN_GENERATOR', 'inviter.tokens.generator')

def import_attribute(path):
    """
    Import an attribute from a module.
    """
    module = '.'.join(path.split('.')[:-1])
    function = path.split('.')[-1]

    module = importlib.import_module(module)
    return getattr(module, function)

class Register(TemplateView):
    """
    A registration view for invited users. The user model already exists - this
    view just takes care of setting a password and username, and maybe update
    the email address. Anywho - one can customize the form that is used.
    
    """
    template_name = 'inviter/register.html'
    form = import_attribute(FORM)
    token_generator = import_attribute(TOKEN_GENERATOR)
    redirect_url = REDIRECT
    
    def get_user(self, uidb36):
        try:
            uid_int = base36_to_int(uidb36) 
            user = User.objects.get(id=uid_int)
        except (ValueError, User.DoesNotExist):
            raise Http404("No such invited user.")
        return user

    def get(self, request, uidb36, token):
        """
        Unfortunately just a copy of 
        ``django.contrib.auth.views.password_reset_confirm``
        """
        assert uidb36 is not None and token is not None
        user = self.get_user(uidb36)

        if not self.token_generator.check_token(user, token):
            return HttpResponseForbidden()
        
        return self.render_to_response({'invitee': user, 'form': self.form(instance=user)})
        
    def post(self, request, uidb36, token):
        """
        Unfortunately just a copy of 
        :attr:`django.contrib.auth.views.password_reset_confirm`
        """
        assert uidb36 is not None and token is not None
        user = self.get_user(uidb36)
        
        if not self.token_generator.check_token(user, token):
            return HttpResponseForbidden()
        
        form = self.form(request.POST, instance=user)
        
        if form.is_valid():
            form.save()
            try:
                return HttpResponseRedirect(reverse(self.redirect_url))
            except:
                return HttpResponseRedirect(self.redirect_url)
        return self.render_to_response({'invitee': user, 'form': form})

class Done(TemplateView):
    template_name = 'inviter/done.html'
    
    def get(self, request):
        return self.render_to_response({})
    
