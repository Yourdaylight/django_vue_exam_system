import subprocess
import json
import os
from django.http import JsonResponse
from rest_framework import mixins, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from study.models import Study
from study.serializers import StudySerializer


# Create your views here.


class StudyListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """选择题列表页"""
    # 这里要定义一个默认的排序，否则会报错
    queryset = Study.objects.all().order_by('id')[:0]
    # 序列化
    serializer_class = StudySerializer

    # 重写queryset
    def get_queryset(self):
        # 题目数量
        choice_number = int(self.request.query_params.get("choice_number", 0))
        level = int(self.request.query_params.get("level", 1))
        content = self.request.query_params.get("content", 0)
        if choice_number:
            self.queryset = Study.objects.all().filter(level=level).order_by('?')[:choice_number]
        return self.queryset


def get_content(request):
    with open("./study/content.json",encoding="utf-8") as f:
        content = json.load(f)
    res = {
        "code": 200,
        "msg": "success",
        "data": content
    }
    return JsonResponse(res)
