from django import forms
from employee.models import DailyReport,Leaves


class DailyReportForm(forms.ModelForm):
    class Meta:
        model = DailyReport
        fields = ['report']

class LeaveForm(forms.ModelForm):
    class Meta:
        model = Leaves
        fields = ['reason']