from django.conf.urls import url
 
from . import views
 
app_name = "file_uploader"
urlpatterns = [
    url(r'^upload$', views.fileUploaderView),
]