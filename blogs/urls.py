from django.conf.urls import url
from . import views

app_name = "blogs"
urlpatterns = [
    url(r'^$', views.post_list, name='post_list'),
]