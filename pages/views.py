from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.context_processors import csrf
from django.contrib.auth import login, authenticate, logout
import json
from microsite.settings import BASE_DIR
from django.contrib.auth.decorators import login_required

@login_required
def pages(request):
	return render_to_response('admin/page/index.html')

@login_required
def new(request):
	return render_to_response('admin/page/new.html')

@login_required
def menu(request):
	return render_to_response('admin/page/menuindex.html')

@login_required
def addmenuitem(request):
	return render_to_response('admin/page/newmenuitem.html')
