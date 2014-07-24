from django.shortcuts import render
from django.http.response import HttpResponse, HttpResponseRedirect

# Create your views here.
def home(request):
	return HttpResponse("hi")