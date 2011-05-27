"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

import datetime

from django.utils import unittest
from django.test.client import Client
from django.test.client import RequestFactory

from post.models import BasicPost, PostWithImage
from gallery.models import Image

class PostTest(unittest.TestCase):

    def setUp(self):
        """
        Create some posts
        """
        self.basicpost1 = BasicPost.objects.create(title='The title',
                                           slug='basicpost-1',                                                   
                                           subtitle='The subtitle',
                                           teaser='<p>The teaser</p>',
                                           introduction='<p>The introduction</p>',
                                           body='<p>The body</p>'
                                           )

        self.basicpost2 = BasicPost.objects.create(title='The title',
                                           slug='basicpost-2',                                                   
                                           subtitle='The subtitle',
                                           teaser='<p>The teaser</p>',
                                           introduction='<p>The introduction</p>',
                                           body='<p>The body</p>',
                                           date_published=datetime.datetime.now()+datetime.timedelta(days=1)
                                           )

        self.basicpost3 = BasicPost.objects.create(title='The title',
                                           slug='basicpost-3',                                                   
                                           subtitle='The subtitle',
                                           teaser='<p>The teaser</p>',
                                           introduction='<p>The introduction</p>',
                                           body='<p>The body</p>',
                                           date_published=datetime.datetime.now()
                                           )


        self.image1 = Image.objects.create(title="Image title",
                                           slug='image1') 

        self.postwithimage1 = PostWithImage.objects.create(title='The title',
                                           slug='postwithimage-1',
                                           subtitle='The subtitle',
                                           teaser='<p>The teaser</p>',
                                           introduction='<p>The introduction</p>',
                                           body='<p>The body</p>',
                                           image=self.image1
                                           )

        self.postwithimage2 = PostWithImage.objects.create(title='The title',
                                           slug='postwithimage-2',
                                           subtitle='The subtitle',
                                           teaser='<p>The teaser</p>',
                                           introduction='<p>The introduction</p>',
                                           body='<p>The body</p>',
                                           date_published=datetime.datetime.now()+datetime.timedelta(days=1),
                                           image=self.image1
                                           )

        self.postwithimage3 = PostWithImage.objects.create(title='The title',
                                           slug='postwithimage-3',
                                           subtitle='The subtitle',
                                           teaser='<p>The teaser</p>',
                                           introduction='<p>The introduction</p>',
                                           body='<p>The body</p>',
                                           date_published=datetime.datetime.now(),
                                           image=self.image1
                                           )
        self.factory = RequestFactory()

    def tearDown(self):
        BasicPost.objects.all().delete()
        Image.objects.all().delete()
        self.factory = None

    def testCountAllPosts(self):
        posts = BasicPost.objects.select_subclasses()
        self.assertEqual(len(posts), 6)
        
    def testCountPublishedPosts(self):
        posts = BasicPost.objects.filter(date_published__lte=datetime.datetime.now()).select_subclasses()
        self.assertEqual(len(posts), 2)
        self.assertEqual(type(posts[0]), PostWithImage)
        self.assertEqual(type(posts[1]), BasicPost)
        self.assertEqual(posts[0].pk, 6)
        self.assertEqual(posts[1].pk, 3)

    def testPostPublishedListView(self):
        c = Client()
        response = c.get('/posts/')     
        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(response.context['posts']),2)

    def testPostDetailView(self):
        c = Client()
        response = c.get('/posts/id/1/')
        self.assertEquals(response.status_code, 404)
        response = c.get('/posts/id/3/')
        self.assertEquals(response.status_code, 200)

        response = c.get('/posts/id/4/')
        self.assertEquals(response.status_code, 404)
        response = c.get('/posts/id/6/')
        self.assertEquals(response.status_code, 200)



    def testPostDraftView(self):

        c = Client()
        response = c.get('/posts/draft/1/', follow=True)

        # Should return 404 because user is not logged in and this post is not published
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.redirect_chain[0][0], 'http://testserver/accounts/login/?next=/posts/draft/1/')
        
        
        u = User.objects.create(username="joebloggs", email="joebloggs@example.com", is_superuser=True, is_staff=True)
        u.set_password('abcde')
        u.save()
        self.assertEquals(c.login(username='joebloggs', password='abcde'), True)

        # Should return 200 for logged in user
        response = c.get('/posts/draft/1/', follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.context['post'].id, 1)

        
from django.contrib.auth.models import User

class AccountTest(unittest.TestCase):

    
    def setUp(self):
        User.objects.create(username="janebloggs", email="janebloggs@example.com", password="abcde")
        
    def tearDown(self):
        User.objects.all().delete()
        
    def testUser(self):
        self.assertEquals(len(User.objects.all()),1) 
        
    
    def testLogin(self):
        c = Client()      
        response = c.post('/accounts/login/', {'username': 'joebloggs@example.com', 'password': 'abcde'})
        self.assertEquals(response.status_code, 200)
        response = c.post('/accounts/logout/')
        self.assertEquals(response.status_code, 200)
        response = c.post('/accounts/login/', {'username': 'joebloggs', 'password': 'abcde'})
        self.assertEquals(response.status_code, 200)
