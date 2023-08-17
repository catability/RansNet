from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
import os

# Create your views here.


def info(request):
    if request.method == "GET":
        data = {"message": "This is Info page"}
        return JsonResponse(data)


def guide(request):
    media_root = settings.MEDIA_ROOT
    media_url = settings.MEDIA_URL

    report_files = []
    guide_files = []
    other_files = []

    for root, dirs, files in os.walk(media_root):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            relative_path = os.path.relpath(file_path, media_root)
            file_url = os.path.join(media_url, relative_path).replace("\\", "/")

            base_name = os.path.splitext(file_name)[0]

            if "보고서" in base_name:
                report_files.append({"url": file_url, "name": base_name})
            elif "가이드" in base_name:
                guide_files.append({"url": file_url, "name": base_name})
            else:
                other_files.append({"url": file_url, "name": base_name})

    data = {
        "report_files": report_files,
        "guide_files": guide_files,
        "other_files": other_files,
    }
    return JsonResponse(data)
