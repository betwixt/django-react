from django import forms
from .models import WeatherSpot
from bootstrap_modal_forms.mixins import PopRequestMixin, CreateUpdateAjaxMixin


class InputForm(PopRequestMixin, CreateUpdateAjaxMixin, forms.ModelForm):

    class Meta:
        model = WeatherSpot
        fields = ('location', 'start_date',)
#    location = forms.CharField(label="Location", max_length=100)
#    start_date = forms.CharField(label="Start Date", max_length=100, required=False)
	
