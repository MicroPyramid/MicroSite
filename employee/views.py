from django.http.response import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response,render
from django.core.context_processors import csrf
import json
from django.contrib.auth.decorators import login_required
from employee.models import DailyReport,Leaves
from micro_admin.models import User
from employee.forms import DailyReportForm,LeaveForm
import math

@login_required
def reports_list(request):
    if request.user.is_admin:
        reports = User.objects.filter().exclude(is_admin=True)
        return render_to_response('admin/staff/all_reports.html',{'reports':reports})
    else:
        user=User.objects.get(email=request.user.email)
        reports = DailyReport.objects.filter(employee=user)
        return render_to_response('admin/staff/reports.html',{'reports':reports})


@login_required
def employee_report(request,pk):
    user=User.objects.get(pk=pk)
    items_per_page = 10
    if "page" in request.GET:
        page = int(request.GET.get('page'))
    else:
        page = 1
    no_pages = int(math.ceil(float(DailyReport.objects.filter(employee=user).count()) / items_per_page))
    reports = DailyReport.objects.filter(employee=user)[(page - 1) * items_per_page:page * items_per_page]
    return render(request,'admin/staff/reports.html',{'reports':reports,'current_page':page,'last_page':no_pages})


@login_required
def view_report(request,pk):
    reports = DailyReport.objects.get(pk=pk)
    return render_to_response('admin/staff/view_report.html',{'reports':reports})


@login_required
def new_report(request):
    if request.method == 'POST':
        validate_report = DailyReportForm(request.POST)
        if validate_report.is_valid():
            new_report = DailyReport.objects.create(report=request.POST.get('report'),employee=request.user)
            new_report.save()
            data = {'error':False,'response':'Report created successfully'}
        else:
            data = {'error':True,'response':validate_report.errors}
        return HttpResponse(json.dumps(data))
    c = {}
    c.update(csrf(request))
    return render(request,'admin/staff/new_report.html',{'csrf_token':c['csrf_token']})


@login_required
def edit_report(request,pk):
    if request.method == 'POST':
        current_report = DailyReport.objects.get(id=pk)
        if current_report.employee == request.user or request.user.is_admin:
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
    c = {}
    c.update(csrf(request))
    return render(request,'admin/staff/edit_report.html',{'new_report':new_report,'csrf_token':c['csrf_token']})


@login_required
def delete_report(request,pk):
    report = DailyReport.objects.get(id=pk)
    report.delete()
    data = {'error':False,'response':'report deleted' }
    return HttpResponse(json.dumps(data))

@login_required
def new_leave(request):
    if request.method == 'POST':
        validate_leave = LeaveForm(request.POST)
        if validate_leave.is_valid():
            new_leave = Leaves.objects.create(date='1990-09-09',reason=request.POST.get('reason'),user=request.user)
            new_leave.save()
            data = {'error':False,'response':'Report created successfully'}
        else:
            data = {'error':True,'response':validate_leave.errors}
        return HttpResponse(json.dumps(data))
    c = {}
    c.update(csrf(request))
    return render(request,'admin/staff/new_leave.html',{'csrf_token':c['csrf_token']})

@login_required
def leaves_list(request):
    user=User.objects.get(email=request.user.email)
    items_per_page = 10
    if "page" in request.GET:
        page = int(request.GET.get('page'))
    else:
        page = 1
    no_pages = int(math.ceil(float(Leaves.objects.filter(user=user).count()) / items_per_page))
    leaves = Leaves.objects.filter(user=user)[(page - 1) * items_per_page:page * items_per_page]
    return render(request,'admin/staff/leaves.html',{'leaves':leaves,'current_page':page,'last_page':no_pages})

@login_required
def delete_leaves(request,pk):
    leave = Leaves.objects.get(id=pk)
    leave.delete()
    data = {'error':False,'response':'report deleted' }
    return HttpResponse(json.dumps(data))


@login_required
def edit_leaves(request,pk):
    if request.method == 'POST':
        current_leave = Leaves.objects.get(id=pk)
        if current_leave.user == request.user or request.user.is_admin:
            validate_leave = LeaveForm(request.POST, instance=current_leave)
            if validate_leave.is_valid():
                new_leave = validate_leave.save(commit=False)
                new_leave.user=request.user
                new_leave.save()
                data = {'error':False,'response':'Report updated successfully'}
            else:
                data = {'error':True,'response':validate_leave.errors}
        else:
            data = {'error':True,'response':'You cannot edit this report' }
        return HttpResponse(json.dumps(data))
    new_leave = Leaves.objects.get(id=pk)
    c = {}
    c.update(csrf(request))
    return render(request,'admin/staff/edit_leaves.html',{'new_leave':new_leave,'csrf_token':c['csrf_token']})


@login_required
def view_leaves(request,pk):
    leaves = Leaves.objects.get(pk=pk)
    return render_to_response('admin/staff/view_leaves.html',{'leaves':leaves})
