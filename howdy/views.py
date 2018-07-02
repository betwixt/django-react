

from django.shortcuts import render,redirect
from django.views.generic import TemplateView
from .forms import InputForm
from .aeris_weather import getConditions, getForecasts
from .models import WeatherSpot

# From previous example
class HomePageView(TemplateView):
    def get(self, request, **kwargs):
        return render(request, 'index.html', context=None)


# From previous example
class AboutPageView(TemplateView):
    template_name = "about.html"
    
# Form to ask user location for weather report; results are displayed under form

def get_input(request):

    wspot = WeatherSpot()
    
    if request.method =="POST":
        form = InputForm(request.POST)
        if form.is_valid():
            loc = form.cleaned_data["location"]
            wspot.location = loc
            wspot.observation = getConditions(loc)
            
    else:
        form = InputForm()
        
        
    return render(request, 'index.html', {'infields': form, 'wspot': wspot})
    


def show_spots(request):

    spots = WeatherSpot.objects.all().order_by('pk')
    for sp in spots:
        # use location of each spot to request current conditions and forecasts
        sp.observation = getConditions(sp.location)
        sp.forecasts = getForecasts(sp.location)
    
    return render(request, 'weather_spots.html', {'spots': spots})  
#
