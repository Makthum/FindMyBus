from django.contrib.admin.widgets import AdminTimeWidget
from bootstrap3_datetime.widgets import DateTimePicker


__author__ = 'zarroc'
from django import forms

agent=(('ttc','ttc'),('yrt','yrt'),)

class SearchForm(forms.Form):
    routeNo=forms.CharField(max_length=10)
   # agent=forms.ChoiceField(choices=agent,widget=forms.RadioSelect())
    searchdate = forms.DateField(
        widget=DateTimePicker(options={"pickTime": False, "format":"YYYY/MM/DD"}))
    searchtime = forms.DateField(
        widget=DateTimePicker(options={"pickDate": False, "format":"HH:mm"}))

   # t = forms.TimeField(widget=SelectTimeWidget(minute_step=15, second_step=30, twelve_hr=True))


