from django.shortcuts import render_to_response

# Create your views here.
def index(request):
	if request.user.is_authenticated():
		return render_to_response('admin/index.html')
	else:
		return render_to_response('admin/login.html')