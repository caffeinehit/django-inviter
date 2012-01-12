Welcome to django-inviter's documentation!
==========================================

django-inviter allows you to invite users to your Django application. Invited
users are saved as inactive users in your database and activated upon
registration.

Installation
------------

::

    pip install django-inviter
    

Configuration
-------------

Add ``inviter`` and ``django.contrib.sites`` to your ``INSTALLED_APPS``

::

    INSTALLED_APPS = (
        'django.contrib.sites',
        'inviter'
    )
    
Include ``inviter.urls`` into your root ``urls.py`` file under the ``inviter``
namespace
  
::
    
    urlpatterns = patterns('',
        url('^invites/', include('inviter.urls', namespace = 'inviter'))


   
Usage
-----

To invite people make use of ``inviter.utils.invite``

::

    from inviter.utils import invite
    
    invite("foo@example.com", request.user, current_time = datetime.now())

``inviter.utils.invite`` also allows you to make use of a custom email sending
function, say to send HTML emails

:: 

    from inviter.utils import invite
    
    def sendhtml(invitee, inviter, **kwargs):
        # Load templates, send the email here
        pass
        
    invite("foo@example.com", request.user, sendfn=sendhtml)

A useful application of this is keeping track of who invites whom:

::

    from inviter import utils
    from app.models import Invites
    
    def send(invitee, inviter, **kwargs):
        Invites.objects.get_or_create(invitee = invitee, inviter = inviter)
        utils.send_invite(invitee, inviter, **kwargs)

    utils.invite("foo@example.com", request.user, sendfn=send)       
    
Consult ``inviter.utils.invite`` and ``inviter.utils.send_invite`` for more 
information.

By default ``inviter.utils.send_invite`` will render ``inviter/email/subject.txt``
and ``inviter/email/body.txt`` for the email.

``/inviter/register.html`` and ``inviter/done.html`` are rendered when 
registering respectively when done.

If you need a post registration hook, override the registration form with the
settings below.


Settings
--------

There are a couple of editable settings

.. attribute:: INVITER_FORM

    :Default: ``'inviter.forms.RegistrationForm'``
    :type: str
    
    The form to be used when an invited user signs up.
    
.. attribute:: INVITER_REDIRECT
    
    :Default: ``'inviter:done'``
    :type: str
    
    The URL to redirect the user to when the signup completes. This is either a
    URL to reverse via ``reverse(INVITER_REDIRECT)`` or a simple string. 
    Reversing the URL is tried before using the string.
    
.. attribute:: INVITER_TOKEN_GENERATOR

    :Default: ``'inviter.tokens.generator'``
    :type: str
    
    The generator used to create a token which is used to assemble an invite
    URL    
    
.. attribute:: INVITER_FROM_EMAIL

    :Default: ``settings.DEFAULT_FROM_EMAIL``
    
    The email address used to send invites from    
    

Made by `Caffeinehit Ltd <http://www.caffeinehit.com/>`_. 