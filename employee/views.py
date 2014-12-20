from django.http.response import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
import json
from django.contrib.auth.decorators import login_required
from employee.models import DailyReport
from projects.models import Project
from employee.forms import DailyReportForm


@login_required
def reports_list(request):
    reports = DailyReport.objects.all()
    return render_to_response('admin/staff/reports.html',{'reports':reports})


@login_required
def new_report(request):
	if request.method == 'POST':
		validate_report = DailyReportForm(request.POST)
		errors = {}
		if validate_report.is_valid():
			new_report = validate_report.save(commit=False)
			new_report.employee = request.user
			new_report.save()
			data = {'error':False,'response':'Report created'}
		else:
			data = {'error':True,'response':validate_blog.errors}
		return HttpResponse(json.dumps(data))
	projects = Project.objects.all()
	c = {}
	c.update(csrf(request))
	return render_to_response('admin/staff/new_report.html',{'projects':projects,'csrf_token':c['csrf_token']})


@login_required
def edit_report(request,pk):
    if request.method == 'POST':
        current_report = DailyReport.objects.get(id=pk)
        validate_report = DailyReportForm(request.POST,instance=current_report)
        if validate_report.is_valid():
            new_report = validate_report.save(commit=False)
            new_report.user=request.user
            new_report.save()
            data = {'error':False,'response':'Report edited'}
        else:
            data = {'error':True,'response':validate_report.errors}
        return HttpResponse(json.dumps(data))

    new_report = DailyReport.objects.get(id=pk)
    c = {}
    c.update(csrf(request))
    return render_to_response('admin/staff/edit_report.html',{'new_report':new_report,'csrf_token':c['csrf_token']})


@login_required
def delete_report(request,pk):
    report = DailyReport.objects.get(id=pk)
    report.delete()
    return HttpResponseRedirect('/portal/staff/')
