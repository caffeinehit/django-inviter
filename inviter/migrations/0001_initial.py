# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'OptOut'
        db.create_table('inviter_optout', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('hash', self.gf('django.db.models.fields.CharField')(max_length=32)),
        ))
        db.send_create_signal('inviter', ['OptOut'])


    def backwards(self, orm):
        
        # Deleting model 'OptOut'
        db.delete_table('inviter_optout')


    models = {
        'inviter.optout': {
            'Meta': {'object_name': 'OptOut'},
            'hash': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['inviter']
