from django.http.response import HttpResponse
from django.shortcuts import render_to_response, render
from django.contrib.auth.decorators import login_required
from docs.models import Book, Topic
from docs.forms import BookForm

from micro_admin.models import User
import json


@login_required
def books(request):
    books = Book.objects.all()
    return render(request, "docs/books/list_of_books.html",{"books": books})


@login_required
def create_book(request):
    if request.user.is_admin:
        if request.method == "POST":
            book_form = BookForm(request.POST)
            
            if book_form.is_valid():
                book = book_form.save()
                book.status = "Waiting"
                book.authors.add(request.user)
                book.save()
                data = {"error":False, "response":"Book created"}
            
            else:
                data = {"error":True, "response":book_form.errors}
            
            return HttpResponse(json.dumps(data))

        users = User.objects.all()
        return render_to_response("docs/books/create_book.html",{"users": users})

    return render_to_response("admin/accessdenied.html")