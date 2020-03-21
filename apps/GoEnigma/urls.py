from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^login$', views.login),
    url(r'^loginPg$',views.loginPg),
    url(r'^registerPg$',views.regPg),
    url(r'^register$', views.register),
    url(r'^dashboard$', views.dash),
    url(r'^process$', views.processInput),
    url(r'^logOut$', views.logOut)

]