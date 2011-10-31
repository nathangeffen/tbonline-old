====
Zola
====

*WORK IN PROGRESS - USE THIS PROJECT ENTIRELY AT YOUR OWN RISK*

Zola is a work in progress. It is a content management system written in Django. 
Currently it powers the TB Online (www.tbonline.info) website. 

Pre-requisites
--------------

Zola requires Django 1.3. It is developed using Python 2.7. By default it Zola
uses the Xapian search engine, but if you don't want to install Xapian, a simple
edit to the settings file switches off this dependency.

Installation
------------

Installation is manual at present, not properly tested and non-trivial. 

#. Download the zip file from Github, or fork it.

#. All 3rd-party Django dependencies, for example Haystack, Grappelli and 
   Filebrowser, are included with it and are kept in the directory called 
   *external*. So you should not have to download anything else to get the 
   system running. Copy the contents of *external* to a folder on your Python 
   path. Note if any of the third-party libraries are already in a folder in the
   path, make sure to either use a utility like *virtualenv* or fiddle with your
   paths to ensure the the ones supplied with the project are found first. 
   Otherwise you might find you've got different versions running and get 
   strange errors.
   Alternatively you can experiment with different versions of the 3rd-party
   dependencies.   

Once installed, check that it's working (or at least not totally broken) 
by running::

  $ python manage.py test post

How it works
------------

There's a lot of documentation that has to be written here. 

In the meanwhile, take a look at the *post* app, which is the backbone of the 
system. Start with models.py in post. 
