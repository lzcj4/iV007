import json

import os
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from cms.models import User


def index(request):
    if request.method == "POST":
        user = request.POST.get("user")
        pwd = request.POST.get("pwd")
        item = User.objects.filter(Name=user, Password=pwd)
        if item:
            return HttpResponseRedirect(reverse("cms:center"))
        else:
            return HttpResponse(json.dumps({"error": "incorrect user or pwd"}))
    else:
        return render(request, "login.html")


def file_upload(request):
    if request.method == "POST":
        srcFile = request.FILES.get("file", None)
        if not srcFile:
            return HttpResponse(json.dumps({'upload': "no files for upload!"}))

        try:
            with open(os.path.join("E:\\upload", srcFile.name), 'wb+') as destFile:
                for chunk in srcFile.chunks():
                    destFile.write(chunk)
            print("File upload succeed:{}".format(os.path.join("E:\\upload", srcFile.name)))
            return HttpResponse(json.dumps({'upload': "succeed"}))
        except IOError:
            return HttpResponse(json.dumps({'upload': "File upload IO error"}))
        else:
            return HttpResponse(json.dumps({'upload': "File upload unknown error"}))

    else:
        return render(request, "FileUpload.html")


def file_merge(request):
    if request.method == "POST":
        jArray = json.loads(request.body)
        for item in jArray:
            pass

        return HttpResponse(json.dumps({'code': 200, 'msg': 'succeed'}))


def center(request):
    return render(request, "Center.html")


def add_camera_group(request):
    if request.method == "POST":
        group_name = request.POST.get("name", None)
        return HttpResponse(json.dumps({'result': "create succeed"}))
    else:
        return render(request, "AddCameraGroup.html")


def add_camera(request):
    if request.method == "POST":
        group_name = request.POST.get("name", None)
        return HttpResponse(json.dumps({'result': "create succeed"}))
    else:
        return render(request, "AddCamera.html")


def video_playback(request):
    return render(request, "videoplayer.html")
