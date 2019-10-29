from django.conf.urls import url
from . import views

urlpatterns = [
    url('^$', views.index),
    url('^register_process$', views.register_process),
    url('^login_process$', views.login_process),
    url('^dashboard$', views.dashboard),
    url('^logout$', views.logout),
    url('^trips/new$', views.newtrip),
    url('^trips/process_new$', views.process_new),
    url('^trips/(?P<trip_id>\d+)$', views.viewtrip),
    url('^trips/(?P<trip_id>\d+)/remove$', views.remove),
    url('^trips/edit/(?P<trip_id>\d+)$', views.edittrip),
    url('^edit$', views.edit),
    url('update$', views.update),

]