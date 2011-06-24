# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'BasicPost'
        db.create_table('post_basicpost', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('subtitle', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('teaser', self.gf('enhancedtext.fields.EnhancedTextField')(default='\\W', blank=True)),
            ('introduction', self.gf('enhancedtext.fields.EnhancedTextField')(default='\\W', blank=True)),
            ('body', self.gf('enhancedtext.fields.EnhancedTextField')(default='\\W', blank=True)),
            ('pullout_text', self.gf('django.db.models.fields.CharField')(max_length=400, blank=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, db_index=True)),
            ('homepage', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('sticky', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('date_published', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('last_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('date_added', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('allow_comments', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('single_post_template', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('many_post_template', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('copyright', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['copyright.Copyright'], null=True, blank=True)),
        ))
        db.send_create_signal('post', ['BasicPost'])

        # Adding unique constraint on 'BasicPost', fields ['slug', 'date_published']
        db.create_unique('post_basicpost', ['slug', 'date_published'])

        # Adding model 'PostWithImage'
        db.create_table('post_postwithimage', (
            ('basicpost_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['post.BasicPost'], unique=True, primary_key=True)),
            ('image', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gallery.Image'])),
            ('single_post_width', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('single_post_height', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('many_post_width', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('many_post_height', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('post', ['PostWithImage'])

        # Adding model 'PostWithSlideshow'
        db.create_table('post_postwithslideshow', (
            ('basicpost_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['post.BasicPost'], unique=True, primary_key=True)),
            ('single_post_width', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('single_post_height', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('many_post_width', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('many_post_height', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('post', ['PostWithSlideshow'])

        # Adding model 'OrderedImage'
        db.create_table('post_orderedimage', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('post_with_slideshow', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['post.PostWithSlideshow'])),
            ('image', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gallery.Image'])),
            ('position', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal('post', ['OrderedImage'])

        # Adding model 'PostWithEmbeddedObject'
        db.create_table('post_postwithembeddedobject', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('single_post_embedded_html', self.gf('enhancedtext.fields.EnhancedTextField')()),
            ('many_post_embedded_html', self.gf('enhancedtext.fields.EnhancedTextField')()),
        ))
        db.send_create_signal('post', ['PostWithEmbeddedObject'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'BasicPost', fields ['slug', 'date_published']
        db.delete_unique('post_basicpost', ['slug', 'date_published'])

        # Deleting model 'BasicPost'
        db.delete_table('post_basicpost')

        # Deleting model 'PostWithImage'
        db.delete_table('post_postwithimage')

        # Deleting model 'PostWithSlideshow'
        db.delete_table('post_postwithslideshow')

        # Deleting model 'OrderedImage'
        db.delete_table('post_orderedimage')

        # Deleting model 'PostWithEmbeddedObject'
        db.delete_table('post_postwithembeddedobject')


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
        'gallery.image': {
            'Meta': {'ordering': "['-last_modified']", 'object_name': 'Image'},
            'caption': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'copyright': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['copyright.Copyright']", 'null': 'True', 'blank': 'True'}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'file': ('filebrowser.fields.FileBrowseField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        'post.basicpost': {
            'Meta': {'ordering': "['-sticky', '-date_published']", 'unique_together': "(('slug', 'date_published'),)", 'object_name': 'BasicPost'},
            'allow_comments': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'body': ('enhancedtext.fields.EnhancedTextField', [], {'default': "'\\\\W'", 'blank': 'True'}),
            'copyright': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['copyright.Copyright']", 'null': 'True', 'blank': 'True'}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_published': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'homepage': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'introduction': ('enhancedtext.fields.EnhancedTextField', [], {'default': "'\\\\W'", 'blank': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'many_post_template': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'pullout_text': ('django.db.models.fields.CharField', [], {'max_length': '400', 'blank': 'True'}),
            'single_post_template': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'}),
            'sticky': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'subtitle': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'teaser': ('enhancedtext.fields.EnhancedTextField', [], {'default': "'\\\\W'", 'blank': 'True'}),
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
