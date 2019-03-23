from django import forms
from django.utils.translation import ugettext_lazy as _

from bootstrap_modal_forms.mixins import PopRequestMixin, CreateUpdateAjaxMixin


from .models import WeatherSpot
from .aeris_weather import validate_place

class InputForm(PopRequestMixin, CreateUpdateAjaxMixin, forms.ModelForm):

    class Meta:
        model = WeatherSpot
        fields = ['location', 'start_date']
#    location = forms.CharField(label="Location", max_length=100)
#    start_date = forms.CharField(label="Start Date", max_length=100, required=False)

    # Check field input to ensure it will be understood by the weather service
    def clean_location(self):
        data = self.cleaned_data['location']
        # print('Running in clean_location')
        if not validate_place(data):
            raise forms.ValidationError(_('Unknown location! Enter a zip code or city, state'), code='bad_location')
        
        return data
