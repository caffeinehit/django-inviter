"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
from django.contrib.auth.models import User
from django.core.mail import outbox
from django.test import TestCase
from inviter.utils import invite
import shortuuid


class InviteTest(TestCase):
    def setUp(self):
        self.inviter = User.objects.create(username = shortuuid.uuid())
        self.existing = User.objects.create(username = shortuuid.uuid(),
            email = 'existing@example.com')
        self.outbox = outbox

    def test_inviting(self):
        user = invite("foo@example.com", self.inviter)        
        self.assertFalse(user.is_active)
        self.assertEqual(1, len(self.outbox))
        self.assertEqual(3, User.objects.count())
        
        user = invite("foo@example.com", self.inviter)
        self.assertFalse(user.is_active)
        self.assertEqual(2, len(self.outbox))
        self.assertEqual(3, User.objects.count())
        
        user = invite("existing@example.com", self.inviter)
        self.assertTrue(user.is_active)
        self.assertEqual(2, len(self.outbox))
        self.assertEqual(3, User.objects.count())
        

