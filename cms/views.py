import json
import math
import os
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from cms.models import User

http_get = "GET"
http_post = "POST"
upload_folder_name = "foldername"
upload_file_name = "filename"
upload_file_len = "filelen"
upload_file_infos = "fileinfos"
upload_chunk_count = "chunkcount"
upload_chunk_no = "chunkno"
upload_temp_file_format = '{0}.tmp'
upload_merge_chunk_size = 51 * 1024

erro_code = "code"
erro_code_succeed = 200
erro_code_failed = 500

error_msg = "msg"


def index(request):
    if request.method == http_post:
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
    if request.method == http_post:
        jObj = json.loads(request.body)
        folder_name = jObj[upload_folder_name]
        if folder_name:
            folder_path = get_upload_folder(folder_name)
            file_dict = get_file_list(folder_path)
            jArray = []
            for k, v in file_dict.items():
                jArray.append({upload_file_name: k, upload_file_len: v})

            return HttpResponse(
                json.dumps({erro_code: erro_code_succeed, error_msg: "succeed", upload_file_infos: jArray}))
        return HttpResponse(json.dumps({erro_code: erro_code_succeed, error_msg: "folder is not existed"}))


def get_file_list(folder_path):
    file_dict = {}
    if folder_path and os.path.exists(folder_path):
        files = os.listdir(folder_path)
        for f_name in files:
            f_size = os.stat(os.path.join(folder_path, f_name)).st_size
            file_dict[f_name] = f_size
    return file_dict


@csrf_exempt
def file_upload(request):
    if request.method == http_post:
        file_info = request.POST.get(upload_file_infos)
        json_file_info = json.loads(file_info)
        folder_name = json_file_info[upload_folder_name]
        file_name = json_file_info[upload_file_name]
        chunk_count = json_file_info[upload_chunk_count]
        chunk_no = json_file_info[upload_chunk_no]
        file_len = int(json_file_info[upload_file_len])

        src_file = request.FILES.get("file", None)

        if not folder_name or not src_file:
            return HttpResponse(json.dumps({erro_code: 502, 'msg': "no files for upload!"}))

        if chunk_count != chunk_no:
            file_name = upload_temp_file_format.format(chunk_no)

        try:
            folder_path = get_upload_folder(folder_name)
            file_dict = get_file_list(folder_path)
            exist_file_size = file_dict.get(file_name)
            if exist_file_size == file_len:
                return HttpResponse(
                    json.dumps({erro_code: 200, error_msg: u" file:{0} already existed".format(file_name)}))

            if not os.path.exists(folder_path):
                os.makedirs(folder_path, exist_ok=True)
            det_file = os.path.join(folder_path, file_name)
            if os.path.exists(det_file) and os.stat(det_file).st_size == file_len:
                return HttpResponse(
                    json.dumps({erro_code: 200, error_msg: u" file:{0} already existed".format(file_name)}))

            with open(det_file, 'wb+') as destFile:
                for chunk in src_file.chunks(upload_merge_chunk_size):
                    destFile.write(chunk)
            print("File upload succeed:{}".format(det_file))
            return HttpResponse(json.dumps({erro_code: 200, error_msg: " upload succeed"}))
        except IOError:
            return HttpResponse(json.dumps({erro_code: 200, error_msg: "File upload IO error"}))
        else:
            return HttpResponse(json.dumps({erro_code: 502, error_msg: "File upload unknown error"}))
    else:
        return render(request, "FileUpload.html")


@csrf_exempt
def file_merge(request):
    if request.method == http_post:
        jArray = json.loads(request.body)
        folder_name = jArray[upload_folder_name]
        file_name = jArray[upload_file_name]
        file_info = jArray[upload_file_infos]
        no_arr = sorted(fi[upload_chunk_no] for fi in file_info)

        folder_path = get_upload_folder(folder_name)
        with open(os.path.join(folder_path, file_name), 'wb+') as outfile:
            for item in no_arr:
                src_file_name = upload_temp_file_format.format(item)
                with open(os.path.join(folder_path, src_file_name), "rb") as infile:
                    outfile.write(infile.read())
                    outfile.flush()
                    print("File merge {0} -> {1} succeed".format(src_file_name, file_name))

        return HttpResponse(json.dumps({erro_code: 200, error_msg: 'merge succeed'}))


def center(request):
    return render(request, "Center.html")


def add_camera_group(request):
    if request.method == http_post:
        group_name = request.POST.get("name", None)
        return HttpResponse(json.dumps({'result': "create succeed"}))
    else:
        return render(request, "AddCameraGroup.html")


def add_camera(request):
    if request.method == http_post:
        group_name = request.POST.get("name", None)
        return HttpResponse(json.dumps({'result': "create succeed"}))
    else:
        return render(request, "AddCamera.html")


def video_playback(request):
    return render(request, "videoplayer.html")
