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
  
   To install Gulp using npm:
   		'$sudo npm install gulp'

   If u want to install gulp in vertual environment just remove sudo in above command
         '$npm install gulp'
   
   To install Gulp pluggines use
   		
   		'$npm install pluggin_name'
   		ex: 'npm install gulp-minify-css'

   To include gulp in gulpfile.js

      // Including gulp
         var gulp = require('gulp'); 

   To include gulpluggines in gulpfile.js

         var pluggin_name = require('pluggin_name');

         ex: var concat = require('gulp-concat');

   To define task in gulpfile.js;

      gulp.task('scripts', function() {
         #your code here

      )}

   To run gulp default task;
      '$ gulp'

   to run specific task;
      '$ gulp task_name'
      ex: '$gulp css'

