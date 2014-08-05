MicroSite
=========

Full featured and completely customizable django site for organizations.

#### This is intended to host the following in the site
1. Static Pages.
2. Configurable Menu.
3. Blog.
4. Employee payroll.
5. Internal knowledge base.
6. Projects the company is dealing.


#### Heroku-Staging

Install django toolbelt
`$ pip instal django-toobelt`

Add Heroku remote to your git repo and name it staging:

`git remote add staging <<heroku repository url>>`

Create staging master to stage changes to heroku for testing

`$ git checkout -b staging_master master`

nce you are on staging_master, pull from the staging repository from heroku:

`$ git pull staging master`

Merge your branch

`$ git merge <branch you want to merge for staging>`

Finally, deploy

`$ git push staging staging_master:master`

view it in browser
`$heroku open`

=========================================================
Introduction to gulpjs

Gulp GULP

   Gulp is task runner.

   by gulp u can combine all javascript, jquery, to single file and u can find any mistakes in ur file.

   Gulp also convert less files to css files.. etc..

   we can do all this by assigning the tasks to gulp

   gulp need pluggins to run the tasks so u have to first install all those pluggins using npm command. this pluggins automatically strored in node_modules folder

   install Gulp using npm:
   		npm install gulp
   
   To install Gulp pluggines use
   		
   		npm install pluggin_name
   		ex: npm install gulp-minify-css.

   