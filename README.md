MicroSite
=========

Full featured and completely customizable django site for organizations.

This is intended to host the following in the site
==================================================
1. Static Pages.
2. Configurable Menu.
3. Blog.
4. Employee payroll.
5. Internal knowledge base.
6. Projects the company is dealing.


Heroku-Staging
==================================================
-->Add Heroku remote to your git repository and name it as staging:
		$git remote add staging <<git repository url>>

-->To create a branch based on master for your staging deployments.Let's call it `staging_master'
		$ git checkout -b staging_master master

-->Next, once you are on staging_master, pull from the staging repository:
		$ git pull staging master`

-->Merge your branch
		$ git merge <<branch to push to staging>>

Finally, deploy

$ git push staging staging_master:master && heroku run python manage.py migrate -a <<app name>> && heroku run python manage.py collectstatic --noinput -a <<app name>>

-->install django toolbelt
    	$ pip instal django-toobelt

-->push application repository to heroku
-->create a place for our repository in heroku
        $heroku create

-->now we can do a simple push to deploy our application
		$git push heroku master

-->to run our application
		$heroku open

