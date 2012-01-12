from django import template
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.utils.http import int_to_base36
from inviter.views import import_attribute, TOKEN_GENERATOR
import shortuuid


FROM_EMAIL = getattr(settings, 'INVITER_FROM_EMAIL', settings.DEFAULT_FROM_EMAIL)

token_generator = import_attribute(TOKEN_GENERATOR)

def send_invite(invitee, inviter, url = None, **kwargs):
    """
    Send the default invitation email assembled from 
    `inviter/email/subject.txt` and `inviter/email/body.txt`
    
    Both templates will receive all the optional arguments.
    
    :param invitee: The invited user
    :type invitee: User
    :param inviter: The inviting user
    :type inviter: User
    :param url: The invite URL
    """
    ctx = {'invitee': invitee, 'inviter': inviter}
    ctx.update(kwargs)
    ctx.update(site = Site.objects.get_current(), url = url)
    ctx = template.Context(ctx)
    
    subject = template.loader.get_template('inviter/email/subject.txt')
    body = template.loader.get_template('inviter/email/body.txt')
    
    subject = subject.render(ctx)
    body = body.render(ctx)
    
    subject = ' '.join(subject.split('\n'))
    
    send_mail(subject, body, FROM_EMAIL, [invitee.email])

def invite(email, inviter, sendfn = send_invite, **kwargs):
    """
    Invite a given email address and return a user model with the given email
    address.
    
    If the user does not exist yet, create one, give it a UUID username, mark
    it as inactive and send the email.
    
    If the user does exist, send another email.

    If the user does exist and is *not* inactive, do nothing.

    Returns the user object.
    
    To customize the sent email, pass in a custom sending function. The sending
    function will receive all the optional arguments.
    
    :param email: The email address
    :type email: str
    :param inviter: The user inviting the email address
    :type inviter: User model
    :param sendfn: An email sending function. Defaults to
        `inviter.utils.send_invite`
    :type sendfn: function
    :rtype: User
    """
    
    try:
        user = User.objects.get(email = email)
        if user.is_active:
            return user
    except User.DoesNotExist:
        user = User.objects.create(username = shortuuid.uuid(), email = email,
            is_active = False)
        user.set_password(User.objects.make_random_password())
        user.save()
    
    url_parts = int_to_base36(user.id), token_generator.make_token(user)
    url = reverse('inviter:register', args=url_parts)
    
    sendfn(user, inviter, url = url, **kwargs)
    return user
    