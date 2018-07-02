from django import forms

class InputForm(forms.Form):
    location = forms.CharField(label="Location", max_length=100)
    start_date = forms.CharField(label="Start Date", max_length=100, required=False)
	
