# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'BasicPost.pullout_text'
        db.add_column('post_basicpost', 'pullout_text', self.gf('django.db.models.fields.CharField')(default='', max_length=400, blank=True), keep_default=False)

        # Changing field 'BasicPost.body'
        db.alter_column('post_basicpost', 'body', self.gf('enhancedtext.fields.EnhancedTextField')())

        # Changing field 'BasicPost.introduction'
        db.alter_column('post_basicpost', 'introduction', self.gf('enhancedtext.fields.EnhancedTextField')())


    def backwards(self, orm):
        
        # Deleting field 'BasicPost.pullout_text'
        db.delete_column('post_basicpost', 'pullout_text')

        # Changing field 'BasicPost.body'
        db.alter_column('post_basicpost', 'body', self.gf('django.db.models.fields.TextField')())

        # Changing field 'BasicPost.introduction'
        db.alter_column('post_basicpost', 'introduction', self.gf('django.db.models.fields.TextField')())


    models = {
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'copyright.copyright': {
            'Meta': {'ordering': "['title']", 'object_name': 'Copyright'},
            'easy_text': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'html_text': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'legal_text': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
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
        },
        'gallery.gallery': {
            'Meta': {'ordering': "['-last_modified']", 'object_name': 'Gallery'},
            'copyright': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['copyright.Copyright']", 'null': 'True', 'blank': 'True'}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'gallery.image': {
            'Meta': {'ordering': "['-last_modified']", 'object_name': 'Image'},
            'caption': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'copyright': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['copyright.Copyright']", 'null': 'True', 'blank': 'True'}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'file': ('filebrowser.fields.FileBrowseField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'gallery': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['gallery.Gallery']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        'post.basicpost': {
            'Meta': {'ordering': "['-sticky', '-date_published']", 'unique_together': "(('slug', 'date_published'),)", 'object_name': 'BasicPost'},
            'allow_comments': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'body': ('enhancedtext.fields.EnhancedTextField', [], {'default': '<enhancedtext.fields.EnhancedText object at 0x221e410>', 'blank': 'True'}),
            'copyright': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['copyright.Copyright']", 'null': 'True', 'blank': 'True'}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_published': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'homepage': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'introduction': ('enhancedtext.fields.EnhancedTextField', [], {'default': '<enhancedtext.fields.EnhancedText object at 0x221e350>', 'blank': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'many_post_template': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'pullout_text': ('django.db.models.fields.CharField', [], {'max_length': '400', 'blank': 'True'}),
            'single_post_template': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'}),
            'sticky': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'subtitle': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'teaser': ('enhancedtext.fields.EnhancedTextField', [], {'default': '<enhancedtext.fields.EnhancedText object at 0x221e250>', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'post.orderedimage': {
            'Meta': {'object_name': 'OrderedImage'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gallery.Image']"}),
            'position': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'post_with_slideshow': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['post.PostWithSlideshow']"})
        },
        'post.postwithembeddedobject': {
            'Meta': {'object_name': 'PostWithEmbeddedObject'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'many_post_embedded_html': ('enhancedtext.fields.EnhancedTextField', [], {}),
            'single_post_embedded_html': ('enhancedtext.fields.EnhancedTextField', [], {})
        },
        'post.postwithimage': {
            'Meta': {'ordering': "['-sticky', '-date_published']", 'object_name': 'PostWithImage', '_ormbases': ['post.BasicPost']},
            'basicpost_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['post.BasicPost']", 'unique': 'True', 'primary_key': 'True'}),
            'image': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gallery.Image']"}),
            'many_post_height': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'many_post_width': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'single_post_height': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'single_post_width': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'post.postwithslideshow': {
            'Meta': {'ordering': "['-sticky', '-date_published']", 'object_name': 'PostWithSlideshow', '_ormbases': ['post.BasicPost']},
            'basicpost_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['post.BasicPost']", 'unique': 'True', 'primary_key': 'True'}),
            'images': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['gallery.Image']", 'through': "orm['post.OrderedImage']", 'symmetrical': 'False'}),
            'many_post_height': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'many_post_width': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'single_post_height': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'single_post_width': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'tagging.tag': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Tag'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'})
        },
        'tagging.taggeditem': {
            'Meta': {'unique_together': "(('tag', 'content_type', 'object_id'),)", 'object_name': 'TaggedItem'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'items'", 'to': "orm['tagging.Tag']"})
        }
    }

    complete_apps = ['post']
