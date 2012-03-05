# Create your views here.
from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponseRedirect, HttpResponseForbidden
from django.utils import importlib
from django.utils.http import base36_to_int
from django.views.generic.base import TemplateView
from inviter.forms import OptOutForm


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

class UserMixin(object):
    """ Handles retrieval of users from the token and does a bit of access
    management. """
    
    token_generator = import_attribute(TOKEN_GENERATOR)
    
    def get_user(self, uidb36):
        try:
            uid_int = base36_to_int(uidb36) 
            user = User.objects.get(id=uid_int)
        except (ValueError, User.DoesNotExist):
            raise Http404("No such invited user.")
        return user
    
    def dispatch(self, request, uidb36, token, *args, **kwargs):
        """ 
        Overriding the default dispatch method on Django's views to do 
        some token validation and if necessary deny access to the resource. 
        
        Also passes the user as first argument after the request argument
        to the handler method.
        """
        assert uidb36 is not None and token is not None
        user = self.get_user(uidb36)

        if not self.token_generator.check_token(user, token):
            return HttpResponseForbidden()
    
        return super(UserMixin, self).dispatch(request, user, *args, **kwargs)
        

class Register(UserMixin, TemplateView):
    """
    A registration view for invited users. The user model already exists - this
    view just takes care of setting a password and username, and maybe update
    the email address. Anywho - one can customize the form that is used.
    
    """
    template_name = 'inviter/register.html'
    form = import_attribute(FORM)
    redirect_url = REDIRECT

    def get(self, request, user):
        """
        Unfortunately just a copy of 
        :attr:`django.contrib.auth.views.password_reset_confirm`
        """
        return self.render_to_response({'invitee': user, 'form': self.form(instance=user)})
        
    def post(self, request, user):
        """
        Unfortunately just a copy of 
        :attr:`django.contrib.auth.views.password_reset_confirm`
        """
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
    
class OptOut(UserMixin, TemplateView):
    """ We want to give the user also the option to *not* receive any
    invitations anymore, which is happening in this view and 
    :class:`inviter.forms.OptOutForm`. """
    template_name = 'inviter/opt-out.html'
    
    def get(self, request, user):
        form = OptOutForm(instance=user)
        
        return self.render_to_response({'form': form})
    
    def post(self, request, user):
        form = OptOutForm(request.POST, instance=user)
        
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('inviter:opt-out-done'))
        return self.render_to_response({'form': form})

class OptOutDone(TemplateView):
    template_name = 'inviter/opt-out-done.html'
    
    def get(self, request):
        return self.render_to_response({})
            
            
