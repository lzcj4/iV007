from django.conf.urls import url

from cms import views

app_name = "cms"
urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^center/$', views.center, name="center"),
    url(r'^camera/group/add/$', views.add_camera_group, name="add_camera_group"),
    url(r'^camera/add/$', views.add_camera, name="add_camera"),
    url(r'^file/upload/', views.file_upload, name="file_upload"),

    url(r'^video/playback/$', views.video_playback, name="video_playback"),
]
