import subprocess
import json
import os

from django.db.models import F
from django.http import JsonResponse
from rest_framework import mixins, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from datetime import datetime
from study.models import Study
from study.serializers import StudySerializer
from study.utils import get_list_from_tree, update_tree, write_json_to_file
from record.models import StudyRecord


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


class ContentView(APIView):

    def get(self, request):
        with open("./study/content.json","r", encoding="utf-8") as f:
            content = json.load(f)
        # 获取数据库中的最大id
        max_id = Study.objects.all().order_by("-id")[0].id
        # 获取树形结构拆解后的列表
        wrap_content = get_list_from_tree(content)
        # 将数据库中的数据更新到树形结构中
        student_id = request.query_params.get("student_id")
        # 在studyRecord中查询学生的学习记录
        study_record = StudyRecord.objects.filter(student_id=student_id)
        for item in wrap_content:
            for record in study_record:
                if item.get("id") == record.study_id_id:
                    item["is_study"] = True
                    item["study_times"] = record.study_times
                    item["study_time"] = record.study_time
                else:
                    item["is_study"] = False
                    item["study_times"] = 0
                    item["study_time"] = "--"

        # 将wrap_content根据study_time和study_times排序
        wrap_content = sorted(wrap_content, key=lambda x: (x["study_times"], x["id"]), reverse=True)
        res = {
            "code": 200,
            "msg": "success",
            "data": {
                "tree":content,
                "table": wrap_content,
            },
            "max_id": max_id
        }
        return JsonResponse(res)

    def post(self, request):
        new_content = request.data.get("content")
        desc = request.data.get("desc")
        name = request.data.get("name")
        _id = request.data.get("_id")

        # 遍历树修改值
        new_content = update_tree(new_content, int(_id), "label", name)
        # 有新的内容则更新本地json
        if new_content:
            write_json_to_file(new_content, "./study/content.json")
            new_content = get_list_from_tree(new_content)
            # 有新的内容则更新数据库
            for item in new_content:
                # update the database use django orm
                Study.objects.update_or_create(
                    id=item.get("id"),
                    defaults={
                        "name": item.get("label"),
                    }
                )
        if desc:
            Study.objects.filter(id=_id).update(desc=desc)
        if name:
            Study.objects.filter(id=_id).update(name=name)
        res = {
            "code": 200,
            "msg": "success",
            "data": new_content
        }
        return JsonResponse(res)


class LearnView(APIView):
    # 根据目录获取章节内容以及学习次数
    def get(self, request):
        _id = request.query_params.get("id")
        student_id = request.query_params.get("student_id")
        desc = Study.objects.filter(id=_id).first()
        student_info = StudyRecord.objects.filter(student_id=int(student_id), study_id_id=int(_id)).first()
        if student_info:
            study_times = student_info.study_times
            study_time = student_info.study_time
        else:
            study_times = 0
            study_time = "--"
        res = {
            "code": 200,
            "msg": "success",
            "data": {
                "desc": desc.desc,
                "points": desc.relate_points,
                "study_times": study_times,
                "study_time": study_time
            }
        }

        return JsonResponse(res)

    # post请求将更新数据库中的学习次数以及学习记录
    def post(self, request):
        res = {
            "code": 200,
            "msg": "success"
        }
        try:
            study_id = request.data.get("study_id")
            student_id = request.data.get("student_id")
            record= StudyRecord.objects.filter(study_id_id=study_id, student_id=student_id).first()
            if record:
                record.study_times = F("study_times") + 1
                record.study_time = datetime.now()
                record.save()
            else:
                StudyRecord.objects.create(study_id_id=study_id, student_id=student_id)
        except Exception as e:
            res["code"] = 500
            res["msg"] = str(e)
        return JsonResponse(res)
