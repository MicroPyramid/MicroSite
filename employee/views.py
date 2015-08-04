from django.http.response import HttpResponse
from django.shortcuts import render_to_response, render
from django.core.context_processors import csrf
import json
from django.contrib.auth.decorators import login_required
from employee.models import DailyReport
from micro_admin.models import User
from employee.forms import DailyReportForm
import datetime

@login_required
def reports_list(request):
    reports = User.objects.filter().exclude(is_superuser=True)
    return render(request, 'admin/staff/all_reports.html', {'reports': reports})


@login_required
def employee_report(request,pk):
    user = User.objects.get(pk=pk)
    
    if request.user == user or request.user.is_superuser:
        reports = DailyReport.objects.filter(employee=user).order_by('-created_on')
        return render(request, 'admin/staff/reports.html', {'reports': reports})
    
    else:
        return render_to_response('admin/accessdenied.html')


@login_required
def view_report(request,pk):
    reports = DailyReport.objects.get(pk=pk)
    if reports.employee == request.user or request.user.is_superuser:
        return render_to_response('admin/staff/view_report.html', {'reports': reports})
    else:
        return render_to_response('admin/accessdenied.html')


@login_required
def new_report(request):
    if request.method == 'POST':
        validate_report = DailyReportForm(request.POST)
        if validate_report.is_valid():
            datestring_format = datetime.datetime.strptime(request.POST.get('date'), "%m/%d/%Y").strftime("%Y-%m-%d")
            date = datetime.datetime.strptime(datestring_format, "%Y-%m-%d")
            new_report = DailyReport.objects.create(report=request.POST.get('report'), employee=request.user, date=date)
            new_report.save()
            data = {'error': False, 'response': 'Report created successfully'}
        else:
            data = {'error': True, 'response': validate_report.errors}
        return HttpResponse(json.dumps(data), content_type='application/json; charset=utf-8')
    c = {}
    c.update(csrf(request))
    return render(request, 'admin/staff/new_report.html', {'csrf_token': c['csrf_token'], 'date': datetime.date.today()})


@login_required
def edit_report(request,pk):
    if request.method == 'POST':
        current_report = DailyReport.objects.get(id=pk)
        if current_report.employee == request.user or request.user.is_superuser:
            validate_report = DailyReportForm(request.POST, instance=current_report)
            if validate_report.is_valid():
                new_report = validate_report.save(commit=False)
                new_report.user = request.user
                new_report.save()
                data = {'error': False, 'response': 'Report updated successfully'}
            else:
                data = {'error': True, 'response': validate_report.errors}
        else:
            data = {'error': True, 'response': 'You cannot edit this report' }
        return HttpResponse(json.dumps(data), content_type='application/json; charset=utf-8')

    new_report = DailyReport.objects.get(id=pk)
    if request.user.is_superuser or request.user.email == new_report.employee.email:
        c = {}
        c.update(csrf(request))
        return render(request, 'admin/staff/edit_report.html', {'new_report': new_report, 'csrf_token': c['csrf_token']})
    else:
        return render_to_response('admin/accessdenied.html')

@login_required
def delete_report(request,pk):
    report = DailyReport.objects.get(id=pk)
    if request.user.is_superuser or request.user == report.employee:
        report.delete()
        data = {'error': False, 'response': 'Report deleted.'}
        return HttpResponse(json.dumps(data), content_type='application/json; charset=utf-8')
    else:
        return render_to_response('admin/accessdenied.html')
