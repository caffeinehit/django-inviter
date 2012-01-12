"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
from django.conf import settings
from django.contrib.auth.models import User
from django.core import mail
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils.http import int_to_base36
from inviter.utils import invite, token_generator
import shortuuid

from django.contrib.auth import tests


class InviteTest(TestCase):
    def setUp(self):
        self.original_email_backend = settings.EMAIL_BACKEND
        settings.EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'
        self.inviter = User.objects.create(username = shortuuid.uuid())
        self.existing = User.objects.create(username = shortuuid.uuid(),
            email = 'existing@example.com')
        
    def tearDown(self):
        settings.EMAIL_BACKEND = self.original_email_backend

    def test_inviting(self):
        user = invite("foo@example.com", self.inviter)        
        self.assertFalse(user.is_active)
        self.assertEqual(1, len(mail.outbox))
        self.assertEqual(3, User.objects.count())
        
        user = invite("foo@example.com", self.inviter)
        self.assertFalse(user.is_active)
        self.assertEqual(2, len(mail.outbox))
        self.assertEqual(3, User.objects.count())
        
        user = invite("existing@example.com", self.inviter)
        self.assertTrue(user.is_active)
        self.assertEqual(2, len(mail.outbox))
        self.assertEqual(3, User.objects.count())
        
    def test_views(self):
        user = invite("foo@example.com", self.inviter)
        url_parts = int_to_base36(user.id), token_generator.make_token(user)
        
        url = reverse('inviter:register', args = url_parts)
        
        resp = self.client.get(url)
        
        self.assertEqual(200, resp.status_code, resp.status_code)
        
        resp = self.client.post(url, {'username': 'testuser', 'email': 'foo@example.com',
            'password': 'test-1234'})
        
        self.assertEqual(302, resp.status_code, resp.content)
        
        self.client.login(username = 'testuser', password = 'test-1234')
        
        resp = self.client.get(reverse('inviter:done'))

        self.assertEqual(200, resp.status_code, resp.status_code)        
        
        

