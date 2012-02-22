from django.conf.urls.defaults import patterns, url
from inviter.views import Register, Done, OptOut, OptOutDone

urlpatterns = patterns('',
    url(r'^done/$', Done.as_view(), name='done'),
    url(r'^register/(?P<uidb36>[0-9A-Za-z]{1,13})-(?P<token>[0-9A-Za-z]+)/$',
        Register.as_view(), name='register'),
    url(r'^optout/(?P<uidb36>[0-9A-Za-z]{1,13})-(?P<token>[0-9A-Za-z]+)/$',
        OptOut.as_view(), name='opt-out'),
    url(r'^optout/done/$',
        OptOutDone.as_view(), name='opt-out-done'),
)
"""
.. attribute:: ^done/$
    
    :name: done
    
.. attribute:: ^register/(?P<uidb36>[0-9A-Za-z]{1,13})-(?P<token>[0-9A-Za-z]+)/$

    :name: register

.. attribute:: ^optout/(?P<uidb36>[0-9A-Za-z]{1,13})-(?P<token>[0-9A-Za-z]+)/$

    :name: opt-out
    
.. attribute:: ^optout/done/$

    :name: opt-out-done
"""
