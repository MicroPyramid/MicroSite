from django.http.response import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
import json
from django.contrib.auth.decorators import login_required
from employee.models import DailyReport
from projects.models import Project
from micro_admin.models import User
from employee.forms import DailyReportForm



@login_required
def reports_list(request):
    if request.user.is_admin:
        reports = User.objects.all()
        return render_to_response('admin/staff/all_reports.html',{'reports':reports})
    else:
        user=User.objects.get(email=request.user.email)
        reports = DailyReport.objects.filter(employee=user)
        return render_to_response('admin/staff/reports.html',{'reports':reports})

@login_required
def employee_report(request,email):
    user=User.objects.get(pk=email)
    reports = DailyReport.objects.filter(employee=user)
    return render_to_response('admin/staff/reports.html',{'reports':reports})

@login_required
def new_report(request):
    if request.method == 'POST':
        validate_report = DailyReportForm(request.POST)
        if validate_report.is_valid():
            new_report = DailyReport.objects.create(report=request.POST.get('report'),employee=request.user)
            if request.POST.getlist('project'):
                for i in request.POST.getlist('project'):
                    project=Project.objects.get(pk=i)
                    new_report.project.add(project)
                    new_report.save()
            new_report.save()
            data = {'error':False,'response':'Report created successfully'}
        else:
            data = {'error':True,'response':validate_report.errors}
        return HttpResponse(json.dumps(data))
    projects = Project.objects.all()
    c = {}
    c.update(csrf(request))
    return render_to_response('admin/staff/new_report.html',{'projects':projects,'csrf_token':c['csrf_token']})


@login_required
def edit_report(request,pk):
    if request.method == 'POST':
        current_report = DailyReport.objects.get(id=pk)
        if current_report.employee == request.user:
            validate_report = DailyReportForm(request.POST, instance=current_report)
            if validate_report.is_valid():
                new_report = validate_report.save(commit=False)
                new_report.user=request.user
                new_report.save()
                data = {'error':False,'response':'Report updated successfully'}
            else:
                data = {'error':True,'response':validate_report.errors}
        else:
            data = {'error':True,'response':'You cannot edit this report' }
        return HttpResponse(json.dumps(data))
    new_report = DailyReport.objects.get(id=pk)
    project = Project.objects.all()
    c = {}
    c.update(csrf(request))
    return render_to_response('admin/staff/edit_report.html',{'projects':project,'new_report':new_report,'csrf_token':c['csrf_token']})


@login_required
def delete_report(request,pk):
    report = DailyReport.objects.get(id=pk)
    report.delete()
    return HttpResponseRedirect('/portal/staff/')
