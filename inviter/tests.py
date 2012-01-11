"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
from django.conf import settings
from django.contrib.auth.models import User
from django.core import mail
from django.test import TestCase
from inviter.utils import invite
import shortuuid


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
        

