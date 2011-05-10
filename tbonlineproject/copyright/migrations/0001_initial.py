# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Copyright'
        db.create_table('copyright_copyright', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('easy_text', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('legal_text', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('html_text', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
        ))
        db.send_create_signal('copyright', ['Copyright'])


    def backwards(self, orm):
        
        # Deleting model 'Copyright'
        db.delete_table('copyright_copyright')


    models = {
        'copyright.copyright': {
            'Meta': {'ordering': "['title']", 'object_name': 'Copyright'},
            'easy_text': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'html_text': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'legal_text': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        }
    }

    complete_apps = ['copyright']
