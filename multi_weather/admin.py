from django.contrib import admin

# Register your models here.

from .models import WeatherSpot

admin.site.register(WeatherSpot)
