### MicroSite

Full featured and completely customizable django site for organizations.

# This is intended to host the following in the site
1. Static Pages.
2. Configurable Menu.
3. Blog.
4. Employee payroll.
5. Internal knowledge base.
6. Projects the company is dealing.


## Heroku-Staging

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

