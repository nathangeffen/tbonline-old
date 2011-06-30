# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'QuestionCategory'
        db.create_table('faq_questioncategory', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=200)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('last_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('date_added', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('faq', ['QuestionCategory'])

        # Adding model 'QuestionAndAnswer'
        db.create_table('faq_questionandanswer', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['faq.QuestionCategory'])),
            ('question', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('answer', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('position', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('last_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('date_added', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('faq', ['QuestionAndAnswer'])


    def backwards(self, orm):
        
        # Deleting model 'QuestionCategory'
        db.delete_table('faq_questioncategory')

        # Deleting model 'QuestionAndAnswer'
        db.delete_table('faq_questionandanswer')


    models = {
        'faq.questionandanswer': {
            'Meta': {'ordering': "['category', 'position']", 'object_name': 'QuestionAndAnswer'},
            'answer': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['faq.QuestionCategory']"}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'position': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'question': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        'faq.questioncategory': {
            'Meta': {'ordering': "['last_modified']", 'object_name': 'QuestionCategory'},
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'})
        }
    }

    complete_apps = ['faq']
