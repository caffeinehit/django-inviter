from django.db import models
import hashlib

class OptOutManager(models.Manager):
    def is_blocked(self, email=None):
        """ Check if a given email address is on the block list. """
        return self.filter(hash=hashlib.sha1(email).hexdigest()).count() > 0
    
    def create(self, email=None):
        """ Create an opt out. """
        return super(OptOutManager, self).create(hash=hashlib.sha1(email).hexdigest())
    
class OptOut(models.Model):
    """ Opt-out email addresses are stored as SHA1 hashes to make sure we don't 
    accidentally collect any more data once a person signalled they're not 
    interested in receiving any more invitation emails from us. """
    hash = models.CharField(max_length=255)
    
    objects = OptOutManager()
    
    def __unicode__(self):
        return self.hash



