from django import template
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.utils.http import int_to_base36
from inviter.models import OptOut
from inviter.views import import_attribute, TOKEN_GENERATOR
import shortuuid


FROM_EMAIL = getattr(settings, 'INVITER_FROM_EMAIL', settings.DEFAULT_FROM_EMAIL)

token_generator = import_attribute(TOKEN_GENERATOR)

def send_invite(invitee, inviter, url=None, opt_out_url=None, **kwargs):
    """
    Send the default invitation email assembled from 
    ``inviter/email/subject.txt`` and ``inviter/email/body.txt``
    
    Both templates will receive all the ``kwargs``.
    
    :param invitee: The invited user
    :param inviter: The inviting user
    :param url: The invite URL
    :param subject_template: The template to render for the subject
    :param body_template: The template to render for the body
    :param opt_out_url: A URL where users can permanently opt out of invitations
    """
    ctx = {'invitee': invitee, 'inviter': inviter}
    ctx.update(kwargs)
    ctx.update(site=Site.objects.get_current(), url=url)
    ctx = template.Context(ctx)
    
    subject_template = kwargs.pop('subject_template', 'inviter/email/subject.txt')
    body_template = kwargs.pop('body_template', 'inviter/email/body.txt')
    
    subject = template.loader.get_template(subject_template)
    body = template.loader.get_template(body_template)
    
    subject = subject.render(ctx)
    body = body.render(ctx)
    
    subject = ' '.join(subject.split('\n')) # No newlines in subject lines allowed
    
    send_mail(subject, body, FROM_EMAIL, [invitee.email])

def invite(email, inviter, sendfn=send_invite, resend=True, **kwargs):
    """
    Invite a given email address and return a ``(User, sent)`` tuple similar
    to the Django :meth:`django.db.models.Manager.get_or_create` method.
    
    If a user with ``email`` address does not exist:
    
    * Creates a :class:`django.contrib.auth.models.User` object 
    * Set ``user.email = email``
    * Set ``user.is_active = False``
    * Set a random password
    * Send the invitation email
    * Return ``(user, True)``
    
    If a user with ``email`` address exists and ``user.is_active == False``:
    
    * Re-send the invitation 
    * Return ``(user, True)``
    
    If a user with ``email`` address exists:
    
    * Don't send  the invitation
    * Return ``(user, False)``
    
    If the email address is blocked:
    
    * Don't send the invitation
    * Return ``(None, False)``
     
    To customize sending, pass in a new ``sendfn`` function as documented by
    :attr:`inviter.utils.send_invite`:
    
    ::
    
        sendfn = lambda invitee, inviter, **kwargs: 1
        invite("foo@bar.com", request.user, sendfn = sendfn)         

    
    :param email: The email address
    :param inviter: The user inviting the email address
    :param sendfn: An email sending function. Defaults to :attr:`inviter.utils.send_invite`
    :param resend: Resend email to users that are not registered yet    
    """
    
    if OptOut.objects.is_blocked(email): 
        return None, False
    try:
        user = User.objects.get(email=email)
        if user.is_active:
            return user, False
        if not resend:
            return user, False
    except User.DoesNotExist:
        user = User.objects.create(
            username=shortuuid.uuid(),
            email=email,
            is_active=False
        )
        user.set_unusable_password()
        user.save()
    
    url_parts = int_to_base36(user.id), token_generator.make_token(user)
    url = reverse('inviter:register', args=url_parts)
    
    opt_out_url = reverse('inviter:opt-out', args=url_parts)
    kwargs.update(opt_out_url=opt_out_url)
    
    sendfn(user, inviter, url=url, **kwargs)
    return user, True
    
