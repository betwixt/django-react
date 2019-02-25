from django import forms
from .models import WeatherSpot

class InputForm(forms.ModelForm):

    class Meta:
        model = WeatherSpot
        fields = ('location', 'start_date',)
#    location = forms.CharField(label="Location", max_length=100)
#    start_date = forms.CharField(label="Start Date", max_length=100, required=False)
	
