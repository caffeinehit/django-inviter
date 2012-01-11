from django.conf.urls.defaults import patterns, url
from inviter.views import Register, Done

urlpatterns = patterns('',
    url(r'^done/$', Done.as_view(), name = 'done'),
    url(r'^register/(?P<uidb36>[0-9A-Za-z]{1,13})-(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        Register.as_view(), name = 'register'),
)