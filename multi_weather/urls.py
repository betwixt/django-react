

# multi_weather/urls.py
from django.conf.urls import url
from multi_weather import views

urlpatterns = [
    url(r'^$', views.show_spots, name="show_weather"),
    url(r'^weatherspot/(?P<pk>\d+)/hourly$', views.chart_data, name='chart_data'),
    url(r'^new$', views.NewSpotView.as_view(), name="wspot_new"),
    url(r'^weatherspot/(?P<pk>\d+)/edit$', views.SpotUpdateView.as_view(), name='wspot_edit'),
    url(r'^weatherspot/(?P<pk>\d+)/delete$', views.DeleteSpotView.as_view(), name='wspot_del'),
    
    url(r'^trial/$', views.get_input, name="trial"),

]


