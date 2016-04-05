MicroSite
=========

Full featured and completely customizable django site for organizations.

.. image:: https://travis-ci.org/MicroPyramid/MicroSite.svg?branch=master
   :target: https://travis-ci.org/MicroPyramid/MicroSite

.. image:: https://readthedocs.org/projects/microsite/badge/?version=latest
   :target: https://readthedocs.org/projects/microsite/?badge=latest
   :alt: Documentation Status

.. image:: https://coveralls.io/repos/MicroPyramid/MicroSite/badge.png?branch=master
   :target: https://coveralls.io/r/MicroPyramid/MicroSite?branch=master

.. image:: https://landscape.io/github/MicroPyramid/MicroSite/master/landscape.svg
   :target: https://landscape.io/github/MicroPyramid/MicroSite/master
   :alt: Code Health

head to http://microsite.readthedocs.org/ for latest documentation

This project contains the following modules.
   * Dynamic Pages.
   * Configurable Menu.
   * Blog.
   * Books.

After installing/cloning this, add the following settings in the virtual env/bin/activate file::

   # SendGrid details
   SGUSER="Your Sendgrid Username"
   SGPWD="Your Sendgrid password"

   # Raven Settings(Sentry)
   SENTRYDSN="Your site DSN"

   GOOGLE_ANALYTICS_CODE = "Your site analytics id"

   export SGUSER
   export SGPWD
   export SENTRYDSN
   export GOOGLE_ANALYTICS_CODE



