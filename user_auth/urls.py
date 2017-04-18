from django.conf.urls import url
 
from . import views

app_name = "user_auth"
urlpatterns = [
    url(r'^register$', views.register),
    url(r'^login', views.loginView),
    url(r'^greeting', views.formView),
    url(r'^logout', views.logoutView)
]