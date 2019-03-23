

from django.shortcuts import render,redirect,get_object_or_404
from django.http import JsonResponse

from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views import generic
from bootstrap_modal_forms.mixins import PassRequestMixin
from datetime import date

from .forms import InputForm
from .aeris_weather import getConditions, getForecasts, getHourly
from .models import WeatherSpot
from .errors import ConnectionError, InputValueError

from django.views.generic import CreateView, UpdateView


class NewSpotView(CreateView):
    model = WeatherSpot
#    form_class = InputForm
    fields = ('location', 'start_date', )
    success_url = reverse_lazy('show_weather')
    template_name = 'new_spot.html'

#    fields = ('location', 'start_date', )    
class SpotUpdateView(PassRequestMixin, SuccessMessageMixin, UpdateView):
    model = WeatherSpot
    form_class = InputForm
    template_name = 'spot_edit.html'
    pk_url_kwarg = 'pk'
    context_object_name = 'spot'
    success_message = 'Settings saved'
    success_url = reverse_lazy('show_weather')

    
# Form to ask user location for weather report; results are displayed under form
# ** Oldest version with everything displayed on same page **
def get_input(request):

    wspot = get_object_or_404(WeatherSpot, pk=1)
    
    if request.method =="POST":
        form = InputForm(request.POST, instance=wspot)
        if form.is_valid():
            loc = form.cleaned_data["location"]
            wspot.location = loc
            wspot.observation = getConditions(loc)
            wspot.forecasts = getForecasts(loc)
            wspot = form.save()
            
    else:
        form = InputForm()   
        
        
    return render(request, 'index.html', {'infields': form, 'wspot': wspot})
    
    
# Original view for editing WeatherSpot location    
def edit_spot(request, pk):
    ws = get_object_or_404(WeatherSpot, pk=pk)
    
    if request.method == "POST":
        form = InputForm(request.POST, instance=ws)
        if form.is_valid():
            ws = form.save()
            return redirect('show_weather')
    else:
        form = InputForm(instance=ws)
    return render(request, 'spot_edit.html', {'infields': form, 'ws': ws})
    


    
def show_spots(request):

    spots = WeatherSpot.objects.all().order_by('pk')
    try:
        for sp in spots:
            # use location of each spot to request current conditions and forecasts
            sp.observation = getConditions(sp.location)
            sp.forecasts = getForecasts(sp.location)
    except ConnectionError as e:
        pass
        # don't redraw weather info, display a message
    except InputValueError as e:
        # return to form, display error message with whatever value caused the problem
        pass
    return render(request, 'weather_spots.html', {'spots': spots})


def chart_data(request, pk):

    # Combine hourly data from different days in the weather spot
    ws = get_object_or_404(WeatherSpot, pk=pk)
    print('In chart_data, pk is {}'.format(pk))
    fc = getHourly(ws.location, date.today())

    data = fc['hour_temps']

    # for day in fc:
        # data.extend( day['hour_temps'] )
    # print ('Hourly data array: {}'.format(data))
    
    chart = {
            'time': {
                'timezone': fc['tz'],
                'useUTC': False
            },

            'title': {
                'text': ''
            },
            'xAxis': {
                'type': 'datetime'
            },
            'yAxis': {
                'title': {
                    'text': None
                },
                'labels': {
                    'format': '{value} \u00b0'
                }
            },
            'legend': {
                'enabled': False
            },
            'plotOptions': {
                'line': {
                    'marker': { 'symbol': 'diamond', 'radius': 2 },
                    'states': {
                        'hover': { 
                            'halo': { 'size': 2 },
                            'lineWidthPlus': 0
                        }
                    },
                    'animation': False
                }
            },
            'tooltip': {
                'dateTimeLabelFormats': {
                    'hour': '%a, %I%p'
                },
                'borderRadius': 1,
                'backgroundColor': '#FFFFFF',
                'pointFormat': '<b>{point.y}</b><br/>',
                'valueSuffix': '\u00b0 F',
                'padding': 2,
                'style': { 'fontSize': '10px', 'color': 'red' },
                'crosshairs': [True, False],
                'split': True,
                'borderWidth': 0,
                'shadow': False
            },

            'series': [{
                'type': 'line',
                'name': 'Hourly Temp',
                'color': 'red',
                'data': data
            }]
        }
    return JsonResponse(chart)

#
#
                # 'area': {
                    # 'marker': {
                        # 'radius': 2
                    # },
                    # 'lineWidth': 1,
                    # 'states': {
                        # 'hover': {
                            # 'lineWidth': 1
                        # }
                    # },
                    # 'threshold': None
                # }
