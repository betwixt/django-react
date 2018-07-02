

# howdy/urls.py
from django.conf.urls import url
from howdy import views

urlpatterns = [
    url(r'^$', views.get_input),
    url(r'^show/', views.show_spots, name="show_weather"),
    url(r'^about/$', views.AboutPageView.as_view()),
]


