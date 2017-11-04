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


def get_upload_folder(folder_name):
    folder_path = os.path.join("E:\\upload", folder_name)
    return folder_path


def file_merge(request):
    if request.method == "GET":
        folder_name = request.GET.get("foldername")
        file_infos = {}
        if not folder_name:
            folder_path = get_upload_folder(folder_name)
            files = os.listdir(folder_path)
            for f in files:
                f_size = os.stat(os.path.join(folder_path, f)).st_size
                file_infos[f] = f_size
            return HttpResponse(json.dumps({'code': 200, 'msg': "succeed", 'files': file_infos}))
        return HttpResponse(json.dumps({'code': 200, 'msg': "folder is not existed"}))


@csrf_exempt
def file_upload(request):
    if request.method == "POST":
        folder_name = request.POST.get("foldername")
        file_num = request.POST.get("filenum")
        src_file = request.FILES.get("file", None)
        if not folder_name or not file_num or not src_file:
            return HttpResponse(json.dumps({'code': 502, 'msg': "no files for upload!"}))

        try:
            folder_path = get_upload_folder(folder_name)
            if not os.path.exists(folder_path):
                os.makedirs(folder_path, exist_ok=True)
            with open(os.path.join(folder_path, file_num + '.tmp'), 'wb+') as destFile:
                for chunk in src_file.chunks():
                    destFile.write(chunk)
            print("File upload succeed:{}".format(os.path.join("E:\\upload", src_file.name)))
            return HttpResponse(json.dumps({'code': 200,'msg': " upload succeed"}))
        except IOError:
            return HttpResponse(json.dumps({'code': 502, 'msg': "File upload IO error"}))
        else:
            return HttpResponse(json.dumps({'code': 502, 'msg': "File upload unknown error"}))
    else:
        return render(request, "FileUpload.html")


@csrf_exempt
def file_merge(request):
    if request.method == "POST":
        jArray = json.loads(request.body)
        folder_name = jArray["foldername"]
        file_name = jArray["filename"]
        file_info = jArray["files"]

        folder_path = get_upload_folder(folder_name)
        with open(os.path.join(folder_path, file_name), 'wb+') as outfile:
            for item in file_info:
                with open(os.path.join(folder_path, str(item['num']) + '.tmp'), "rb") as infile:
                    outfile.write(infile.read())

        return HttpResponse(json.dumps({'code': 200, 'msg': 'merge succeed'}))


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
