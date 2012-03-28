"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
from django.conf import settings
from django.contrib.auth import tests
from django.contrib.auth.models import User
from django.core import mail
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils.http import int_to_base36
from inviter.models import OptOut
from inviter.utils import invite, token_generator
import shortuuid
import urlparse



class InviteTest(TestCase):
    def setUp(self):
        self.original_email_backend = settings.EMAIL_BACKEND
        settings.EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'
        self.inviter = User.objects.create(username=shortuuid.uuid())
        self.existing = User.objects.create(username=shortuuid.uuid(),
            email='existing@example.com')
        
    def tearDown(self):
        settings.EMAIL_BACKEND = self.original_email_backend

    def test_inviting(self):
        user, sent = invite("foo@example.com", self.inviter)    
        self.assertTrue(sent)    
        self.assertFalse(user.is_active)
        self.assertEqual(1, len(mail.outbox))
        self.assertEqual(3, User.objects.count())
        
        # Resend the mail
        user, sent = invite("foo@example.com", self.inviter)
        self.assertTrue(sent)
        self.assertFalse(user.is_active)
        self.assertEqual(2, len(mail.outbox))
        self.assertEqual(3, User.objects.count())
        
        # Don't resend the mail
        user, sent = invite("foo@example.com", self.inviter, resend = False)
        self.assertFalse(sent)
        self.assertFalse(user.is_active)
        self.assertEqual(2, len(mail.outbox))
        self.assertEqual(3, User.objects.count())        
        
        # Don't send the email to active users
        user, sent = invite("existing@example.com", self.inviter)
        self.assertFalse(sent)
        self.assertTrue(user.is_active)
        self.assertEqual(2, len(mail.outbox))
        self.assertEqual(3, User.objects.count())
        
    def test_views(self):
        user, sent = invite("foo@example.com", self.inviter)
        self.assertTrue(sent)
        url_parts = int_to_base36(user.id), token_generator.make_token(user)
        
        url = reverse('inviter:register', args=url_parts)
        
        resp = self.client.get(url)
        
        self.assertEqual(200, resp.status_code, resp.status_code)
        
        resp = self.client.post(url, {'username': 'testuser', 'email': 'foo@example.com',
            'new_password1': 'test-1234', 'new_password2': 'test-1234'})
        
        self.assertEqual(302, resp.status_code, resp.content)
        
        self.client.login(username='testuser', password='test-1234')
        
        resp = self.client.get(reverse('inviter:done'))

        self.assertEqual(200, resp.status_code, resp.status_code)        
        
    def test_opt_out(self):
        self.assertEqual(2, User.objects.count())
        
        user, sent = invite("foo@example.com", self.inviter)
        self.assertTrue(sent)
        self.assertEqual(1, len(mail.outbox))
        self.assertEqual(3, User.objects.count())
        
        url_parts = int_to_base36(user.id), token_generator.make_token(user)
        url = reverse('inviter:opt-out', args=url_parts)
       
        resp = self.client.get(url)
        self.assertEqual(200, resp.status_code, resp.status_code)

        resp = self.client.post(url, {})
        self.assertEqual(302, resp.status_code, resp.status_code)
        self.assertEqual(reverse('inviter:opt-out-done'), urlparse.urlparse(resp['Location']).path)
        self.assertEqual(2, User.objects.count())
        
        user, sent = invite("foo@example.com", self.inviter)
        self.assertFalse(sent)
        self.assertEqual(1, len(mail.outbox))
        self.assertEqual(1, OptOut.objects.count())
        self.assertTrue(OptOut.objects.is_blocked("foo@example.com"))
        self.assertIsNone(user)
        
        
        
