MicroSite's documentation!
=====================================

Introduction:
=============

This is complete code powering the very micropyramid company site www.micropyramid.com.
We intend to opensource our code to be used by other companies or people.
This is completely extensible and documented.

Modules used:
    * Pillow
    * Haystack with elasticsearch
    * Sorl
    * Akismet


Installation procedure
======================

Install git and supporting packages
-----------------------------------

.. code-block:: shell

  apt-get install -y git software-propeties-common libxml2-dev libxslt1-dev libffi-dev python-virtualenv python3-pip libpq-dev python3-dev redis-server postgresql-9.4 npm ruby


Manual Install Elastic Search
-----------------------------

Setup Java
----------

.. code-block:: shell

  add-apt-repository ppa:webupd8team/java
  apt-get update
  apt-get install oracle-java8-installer

Download Latest version of elasticsearch from https://www.elastic.co/downloads/elasticsearch. At time of this tutorial elasticsearch 5.1.1 was available stable version


.. code-block:: shell

  wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-5.1.1.deb
  dpkg -i elasticsearch-5.1.1.deb
  service elasticsearch start

Setting up Project
------------------
The below commands will download latest code of MicroSite and move the project to /webapps/microsite/microsite setup virtualenv with python3, install required pip, ruby and node packages and create a symlink of nodejs to node


.. code-block:: shell

  git clone https://github.com/MicroPyramid/MicroSite.git
  mkdir -p /webapps/microsite
  mv MicroSite /webapps/microsite/microsite
  cd /webapps/microsite
  virtualenv -p python3 env
  source env/bin/activate
  pip3 install -r microsite/requirements.txt
  gem install sass
  npm install -g less
  ln -s /usr/bin/nodejs /usr/bin/node

Login into postgresql shell

.. code-block:: shell

  CREATE DATABASE microsite;
  CREATE USER microsite with password 'password';
  GRANT ALL PRIVILEGES ON DATABASE microsite TO microsite;


To Do
-----

- Modify database details in settings.py
- Add your hostname to ALLOWED_HOSTS
- Run the following project manage.py commands

.. code-block:: shell

  python manage.py makemigrations
  python manage.py migrate
  python manage.py createsuperuser # to add Admin User

Note that all the above commands should be executed when virtualenv is activated


Working modules
===============
* Create static pages.
* Dynamic configurable menu.
* A complete blog system with comments.

Planned Modules
===============
* Internal Knowledgebase.

We are always looking to help you customize the whole or part of the code as you like.
