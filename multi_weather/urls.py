

# multi_weather/urls.py
from django.conf.urls import url
from multi_weather import views

urlpatterns = [
    url(r'^trial/$', views.get_input, name="trial"),
    url(r'^weatherspot/(?P<pk>\d+)/hourly$', views.chart_data, name='chart_data'),
    url(r'^$', views.show_spots, name="show_weather"),
    url(r'^weatherspot/(?P<pk>\d+)/edit$', views.edit_spot, name='wspot_edit'),
    url(r'^about/$', views.AboutPageView.as_view()),
]


