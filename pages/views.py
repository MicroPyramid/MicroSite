from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.context_processors import csrf
from django.contrib.auth import login, authenticate, logout
import json
from microsite.settings import BASE_DIR
from django.contrib.auth.decorators import login_required
from pages.models import *
from django.views.decorators.csrf import csrf_exempt
from pages.forms import *


@login_required
def pages(request):
	pagelist=page.objects.all()
	return render_to_response('admin/page/index.html',{'page_list': pagelist})

@login_required
def new(request):
	if request.method=='GET':
		return render_to_response('admin/page/new.html')
	else:
		validate_page = PageForm(request.POST)
		if validate_page.is_valid():
			new_page = validate_page.save(commit = False)
			new_page.status = 'on'
			new_page.save()
		data={"error":False}
		return HttpResponse(json.dumps(data))


@login_required
def deletepage(request, pk):
	page.objects.get(pk = pk).delete()
	return HttpResponseRedirect('/portal/pages/')


@login_required
def editpage(request, pk):
	if request.method=='GET':
		s=page.objects.get(pk=pk)
		return render_to_response('admin/page/edit.html',{'s1':s})
	else:
		
		print request.POST
		a=page.objects.get(pk=pk)
		val_form=PageForm(request.POST,instance=a)
		if val_form.is_valid():
			print "valid"
			new_page=val_form.save()
		data={"error":False}
		return HttpResponse(json.dumps(data))
		

@login_required
def statuspage(request, pk):
	s=page.objects.get(pk = pk)
	if s.status=="on":
		s.status="off"
		s.save()
	elif s.status=="off":
		s.status="on"
		s.save()
	return HttpResponseRedirect('/portal/pages/')


@login_required
def deletemenu(request, pk):
	Menu.objects.get(pk = pk).delete()
	return HttpResponseRedirect('/portal/menu/')


@login_required
def statusmenu(request, pk):
	s=Menu.objects.get(pk = pk)
	if s.status=="on":
		s.status="off"
		s.save()
	else:
		s.status="on"
		s.save()
	return HttpResponseRedirect('/portal/menu/')


@login_required
def menu(request):
	menulist=Menu.objects.all()
	return render_to_response('admin/page/menuindex.html',{'menu_list':menulist})


@login_required
def addmenuitem(request):
	if request.method=='GET':
		return render_to_response('admin/page/newmenuitem.html')
	else:
		validate_page = MenuForm(request.POST)
		if validate_page.is_valid():
			new_page = validate_page.save(commit = False)
			new_page.status = 'on'
			new_page.save()
		data={"error":False}
		return HttpResponse(json.dumps(data))


@login_required
def editmenu(request, pk):
	if request.method=='GET':
		s=Menu.objects.get(pk=pk)
		return render_to_response('admin/page/editmenu.html',{'s1':s})
	else:		
		a=Menu.objects.get(pk=pk)
		val_form=MenuForm(request.POST,instance=a)
		if val_form.is_valid():
			new_page=val_form.save()
		else:
			print "else"
		data={"error":False}
		return HttpResponse(json.dumps(data))