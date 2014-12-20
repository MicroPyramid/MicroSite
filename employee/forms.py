from django import forms
from employee.models import DailyReport


class DailyReportForm(forms.ModelForm):
    class Meta:
        model = DailyReport
        fields = ['report']