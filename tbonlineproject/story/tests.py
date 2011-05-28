"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

import datetime

from django.test import TestCase
from django.test.client import Client

from story.models import Story
from post.tests import add_posts, delete_posts

class SimpleTest(TestCase):
    def setUp(self):
        """
        Create some stories
        """
        self.test_posts = add_posts()

        self.story1 = Story.objects.create(title="The title",
                                           slug="story-1",
                                           description="<p>The description</p>")
        self.story1.orderedpost_set.create(post=self.test_posts[5])
        self.story1.orderedpost_set.create(post=self.test_posts[0])
        self.story1.orderedpost_set.create(post=self.test_posts[3])
        self.story1.orderedpost_set.create(post=self.test_posts[2])
        self.story1.save()

        self.story2 = Story.objects.create(title="The title",
                                           slug="story-2",
                                           description="<p>The description</p>",
                                           date_published=datetime.datetime.now()+datetime.timedelta(days=1))
        self.story2.orderedpost_set.create(post=self.test_posts[3])
        self.story2.orderedpost_set.create(post=self.test_posts[1])
        self.story2.orderedpost_set.create(post=self.test_posts[4])
        self.story2.orderedpost_set.create(post=self.test_posts[5])
        self.story2.save()

        self.story3 = Story.objects.create(title="The title",
                                           slug="story-3",
                                           description="<p>The description</p>",
                                           date_published=datetime.datetime.now())
        self.story3.orderedpost_set.create(post=self.test_posts[3])
        self.story3.orderedpost_set.create(post=self.test_posts[1])
        self.story3.orderedpost_set.create(post=self.test_posts[4])
        self.story3.orderedpost_set.create(post=self.test_posts[5])
        self.story3.save()


    def testCountStories(self):
        stories = Story.objects.all()
        self.assertEqual(len(stories), 3)
        self.assertEqual(len(stories[0].orderedpost_set.all()),4)

    def testCountPublishedStories(self):
        stories = Story.objects.filter(date_published__lte=datetime.datetime.now())
        self.assertEqual(len(stories), 1)
        self.assertEqual(stories[0].slug, "story-3")

    def testStoryPublishedListView(self):
        c = Client()
        response = c.get('/stories/')     
        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(response.context['stories']),1)

    def testStoryDetailView(self):
        c = Client()
        response = c.get('/stories/1/')
        self.assertEquals(response.status_code, 404)
        response = c.get('/stories/1/1/')
        self.assertEquals(response.status_code, 404)
        response = c.get('/stories/3/')
        self.assertEquals(response.status_code, 200)        
        response = c.get('/stories/3/1/')
        self.assertEquals(response.status_code, 404)
        response = c.get('/stories/3/6/')
        self.assertEquals(response.status_code, 200)
        
    def testStoryDraftView(self):

        c = Client()
#        response = c.get('/stories/1/', follow=True)
#
#        # Should return 404 because user is not logged in and this post is not published
#        self.assertEquals(response.status_code, 200)
#        self.assertEquals(response.redirect_chain[0][0], 'http://testserver/accounts/login/?next=/posts/draft/1/')
#        
#        
#        u = User.objects.create(username="joebloggs", email="joebloggs@example.com", is_superuser=True, is_staff=True)
#        u.set_password('abcde')
#        u.save()
#        self.assertEquals(c.login(username='joebloggs', password='abcde'), True)
#
#        # Should return 200 for logged in user
#        response = c.get('/posts/draft/1/', follow=True)
#        self.assertEquals(response.status_code, 200)
#        self.assertEquals(response.context['post'].id, 1)



    def tearDown(self):
        delete_posts()
        
        