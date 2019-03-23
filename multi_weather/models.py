from django.db import models
from django.utils import timezone
import datetime

class WeatherSpot(models.Model):
    # From a separate example
    #author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    #text = models.TextField()
    
    location = models.CharField(max_length=200)
    start_date = models.DateField(default=datetime.date.today)
    observation = {}
    forecast = {}

            
    def __str__(self):
        if self.location:
            return ''.join(("Weatherspot for location: ", self.location))
        else:
            return 'Empty WeatherSpot'
        
    
