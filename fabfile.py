from django.conf import settings as django_settings
from datetime import datetime
from fabric.api import *
import django
import yaml
import os


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "microsite.settings")
django.setup()


def build_documents():
    books_dir = os.path.join(django_settings.BASE_DIR, 'books')
    books_source_dir = os.path.join(django_settings.BASE_DIR, 'books/source')
    documents_file = open(os.path.join(books_dir, 'books.yml'), 'r')
    data = yaml.load(documents_file)

    # Update the books modified date in books.yml file
    for position, book in data.get('documents').iteritems():
        book["updated_date"] = datetime.fromtimestamp(
            os.path.getmtime(books_source_dir + '/' + book.get("folder_name")))

    with open(os.path.join(books_dir, 'books.yml'), 'w') as f:
        yaml.dump(data, f, default_flow_style=False)

    # Remove the templates(build) directory, if exists
    books_templates_dir = os.path.join(
        django_settings.BASE_DIR, 'books/templates')
    if os.path.exists(books_templates_dir):
        local("rm -rf %s" % books_templates_dir)

    # Build documents(.rst files to HTML files) using Sphinx command.
    local("cd books && make html")
