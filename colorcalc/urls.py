
from django.conf.urls import url
from . import views

urlpatterns = [
        url(r'^subjects/$', views.SubjectList.as_view() ),
        url(r'^subjects/(?P<pk>\d+)/$', views.SubjectDetail.as_view() ),
]
