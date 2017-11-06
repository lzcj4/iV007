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


@csrf_exempt
def file_query(request):
    if request.method == "POST":
        jObj = json.loads(request.body)
        folder_name = jObj["foldername"]
        if folder_name:
            folder_path = get_upload_folder(folder_name)
            file_dict = get_file_list(folder_path)
            return HttpResponse(json.dumps({'code': 200, 'msg': "succeed", 'files': file_dict}))
        return HttpResponse(json.dumps({'code': 200, 'msg': "folder is not existed"}))


def get_file_list(folder_path):
    file_dict = {}
    if folder_path and os.path.exists(folder_path):
        files = os.listdir(folder_path)
        for f in files:
            f_size = os.stat(os.path.join(folder_path, f)).st_size
            file_dict[f] = f_size
    return file_dict


@csrf_exempt
def file_upload(request):
    if request.method == "POST":
        file_info = request.POST.get("fileinfo")
        json_file_info = json.loads(file_info)
        folder_name = json_file_info["foldername"]
        file_name = json_file_info["filename"]
        chunk_count = json_file_info["chunkcount"]
        chunk_no = json_file_info["chunkno"]
        file_len = int(json_file_info["filelen"])

        src_file = request.FILES.get("file", None)

        if not folder_name or not src_file:
            return HttpResponse(json.dumps({'code': 502, 'msg': "no files for upload!"}))

        if chunk_count != chunk_no:
            file_name = '{0}.tmp'.format(chunk_no)

        try:
            folder_path = get_upload_folder(folder_name)
            file_dict = get_file_list(folder_path)
            exist_file_size = file_dict.get(file_name)
            if exist_file_size == file_len:
                return HttpResponse(json.dumps({'code': 200, 'msg': u" file:{0} already existed".format(file_name)}))

            if not os.path.exists(folder_path):
                os.makedirs(folder_path, exist_ok=True)
            det_file = os.path.join(folder_path, file_name)
            if os.path.exists(det_file) and os.stat(det_file).st_size == file_len:
                return HttpResponse(json.dumps({'code': 200, 'msg': u" file:{0} already existed".format(file_name)}))

            with open(det_file, 'wb+') as destFile:
                for chunk in src_file.chunks():
                    destFile.write(chunk)
            print("File upload succeed:{}".format(det_file))
            return HttpResponse(json.dumps({'code': 200, 'msg': " upload succeed"}))
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
                with open(os.path.join(folder_path, "{0}.tmp".format(item['chunkno'])), "rb") as infile:
                    outfile.write(infile.read())
                    outfile.flush()

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
