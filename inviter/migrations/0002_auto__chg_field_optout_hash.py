# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Changing field 'OptOut.hash'
        db.alter_column('inviter_optout', 'hash', self.gf('django.db.models.fields.CharField')(max_length=255))


    def backwards(self, orm):
        
        # Changing field 'OptOut.hash'
        db.alter_column('inviter_optout', 'hash', self.gf('django.db.models.fields.CharField')(max_length=32))


    models = {
        'inviter.optout': {
            'Meta': {'object_name': 'OptOut'},
            'hash': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['inviter']
