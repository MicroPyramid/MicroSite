from django.http.response import HttpResponse
from django.shortcuts import render_to_response, render
from django.core.context_processors import csrf
import json
from django.contrib.auth.decorators import login_required
from employee.models import DailyReport, Leaves
from micro_admin.models import User
from employee.forms import DailyReportForm, LeaveForm
import math
import datetime

@login_required
def reports_list(request):
    reports = User.objects.filter().exclude(is_admin=True)
    return render(request,'admin/staff/all_reports.html',{'reports':reports})


@login_required
def employee_report(request,pk):
    user=User.objects.get(pk=pk)
    if request.user == user or request.user.is_admin:
        items_per_page = 10
        if "page" in request.GET:
            page = int(request.GET.get('page'))
        else:
            page = 1
        no_pages = int(math.ceil(float(DailyReport.objects.filter(employee=user).count()) / items_per_page))
        reports = DailyReport.objects.filter(employee=user).order_by('created_on')[(page - 1) * items_per_page:page * items_per_page]
        return render(request,'admin/staff/reports.html',{'reports':reports,'current_page':page,'last_page':no_pages})
    else:
        return render_to_response('admin/accessdenied.html')

@login_required
def view_report(request,pk):
    reports = DailyReport.objects.get(pk=pk)
    if reports.employee == request.user or request.user.is_admin:
        return render_to_response('admin/staff/view_report.html',{'reports':reports})
    else:
        return render_to_response('admin/accessdenied.html')

@login_required
def new_report(request):
    if request.method == 'POST':
        datestring_format = datetime.datetime.strptime(request.POST.get('date'),"%d/%m/%Y").strftime("%Y-%m-%d")
        date=datetime.datetime.strptime(datestring_format, "%Y-%m-%d")
        validate_report = DailyReportForm(request.POST)
        if validate_report.is_valid():
            new_report = DailyReport.objects.create(report=request.POST.get('report'),employee=request.user,date=date)
            new_report.save()
            data = {'error':False,'response':'Report created successfully'}
        else:
            data = {'error':True,'response':validate_report.errors}
        return HttpResponse(json.dumps(data))
    c = {}
    c.update(csrf(request))
    return render(request,'admin/staff/new_report.html',{'csrf_token':c['csrf_token'],'date':datetime.date.today()})

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
    if request.user.is_admin or request.user.email == new_report.employee.email:
        c = {}
        c.update(csrf(request))
        return render(request,'admin/staff/edit_report.html',{'new_report':new_report,'csrf_token':c['csrf_token']})
    else:
        return render_to_response('admin/accessdenied.html')

@login_required
def delete_report(request,pk):
    report = DailyReport.objects.get(id=pk)
    if request.user.is_admin or request.user == report.employee:
        report.delete()
        data = {'error':False,'response':'report deleted' }
        return HttpResponse(json.dumps(data))
    else:
        return render_to_response('admin/accessdenied.html')


@login_required
def new_leave(request):
    if request.method == 'POST':
        leaves=Leaves.objects.filter(date=request.POST.get('date'))
        if leaves:
            datestring_format = datetime.datetime.strptime(request.POST.get('date'),"%d/%m/%Y").strftime("%Y-%m-%d")
            date=datetime.datetime.strptime(datestring_format, "%Y-%m-%d")
            validate_leave = LeaveForm(request.POST)
            if validate_leave.is_valid():
                new_leave = Leaves.objects.create(reason=request.POST.get('reason'),user=request.user,date=date)
                new_leave.save()
                data = {'error':False,'response':'Report created successfully'}
            else:
                data = {'error':True,'response':validate_leave.errors}
        else:
            data = {'error':True,'response':'Leave already created on that day'}
        return HttpResponse(json.dumps(data))
            
    c = {}
    c.update(csrf(request))
    return render(request,'admin/staff/new_leave.html',{'csrf_token':c['csrf_token']})

@login_required
def leaves_list(request):
    users = User.objects.filter().exclude(is_admin=True)
    return render(request,'admin/staff/all_leaves.html',{'users':users})


@login_required
def employee_leaves(request,pk):
    user=User.objects.get(pk=pk)
    if request.user == user or request.user.is_admin:
        items_per_page = 10
        if "page" in request.GET:
            page = int(request.GET.get('page'))
        else:
            page = 1
        no_pages = int(math.ceil(float(Leaves.objects.filter(user=user).count()) / items_per_page))
        leaves = Leaves.objects.filter(user=user).order_by('created_on')[(page - 1) * items_per_page:page * items_per_page]
        return render(request,'admin/staff/leaves.html',{'leaves':leaves,'current_page':page,'last_page':no_pages})
    else:
        return render_to_response('admin/accessdenied.html')
    
    
@login_required
def delete_leaves(request,pk):
    leave = Leaves.objects.get(id=pk)
    if request.user.is_admin or request.user == leave.user:
        leave.delete()
        data = {'error':False,'response':'report deleted' }
        return HttpResponse(json.dumps(data))
    else:
        return render_to_response('admin/accessdenied.html')

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
                data = {'error':False,'response':'Leave updated successfully'}
            else:
                data = {'error':True,'response':validate_leave.errors}
        else:
            data = {'error':True,'response':'You cannot edit this report' }
        return HttpResponse(json.dumps(data))
    new_leave = Leaves.objects.get(id=pk)
    if new_leave.user==request.user or request.user.is_admin:
        c = {}
        c.update(csrf(request))
        return render(request,'admin/staff/edit_leaves.html',{'new_leave':new_leave,'csrf_token':c['csrf_token']})
    else:
        return render_to_response('admin/accessdenied.html')


@login_required
def view_leaves(request,pk):
    leaves = Leaves.objects.get(pk=pk)
    if request.user == leaves.user or request.user.is_admin:
        return render_to_response('admin/staff/view_leaves.html',{'leaves':leaves})
    else:
        return render_to_response('admin/accessdenied.html')