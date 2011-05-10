# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Credit'
        db.create_table('credit_credit', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('is_person', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('first_names', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
        ))
        db.send_create_signal('credit', ['Credit'])

        # Adding model 'OrderedCredit'
        db.create_table('credit_orderedcredit', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('credit', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['credit.Credit'])),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('position', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal('credit', ['OrderedCredit'])

        # Adding unique constraint on 'OrderedCredit', fields ['credit', 'content_type', 'object_id']
        db.create_unique('credit_orderedcredit', ['credit_id', 'content_type_id', 'object_id'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'OrderedCredit', fields ['credit', 'content_type', 'object_id']
        db.delete_unique('credit_orderedcredit', ['credit_id', 'content_type_id', 'object_id'])

        # Deleting model 'Credit'
        db.delete_table('credit_credit')

        # Deleting model 'OrderedCredit'
        db.delete_table('credit_orderedcredit')


    models = {
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'credit.credit': {
            'Meta': {'ordering': "['last_name']", 'object_name': 'Credit'},
            'first_names': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_person': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        'credit.orderedcredit': {
            'Meta': {'ordering': "['position']", 'unique_together': "(('credit', 'content_type', 'object_id'),)", 'object_name': 'OrderedCredit'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'credit': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['credit.Credit']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'position': ('django.db.models.fields.PositiveIntegerField', [], {})
        }
    }

    complete_apps = ['credit']
