"""ExamOnline URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import xadmin
from django.urls import path, include, re_path
from django.views.generic.base import TemplateView
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter
from rest_framework_jwt.views import obtain_jwt_token

from exam.views import GradeListViewSet, ExamListViewSet, PracticeListViewSet
from question.views import ChoiceListViewSet, FillListViewSet, JudgeListViewSet, ProgramListViewSet, CheckProgramApi
from record.views import ChoiceRecordListViewSet, FillRecordListViewSet, JudgeRecordListViewSet, \
    ProgramRecordListViewSet, StudyRecordListViewSet
from user.views import RegisterViewSet, StudentViewSet, UpdatePwdApi, ClazzListViewSet
from study.views import StudyListViewSet, ContentView, LearnView

router = DefaultRouter()

# 配置exams的url
router.register(r'exams', ExamListViewSet)
router.register(r'grades', GradeListViewSet)
router.register(r'choices', ChoiceListViewSet)
router.register(r'fills', FillListViewSet)
router.register(r'judges', JudgeListViewSet)
router.register(r'programs', ProgramListViewSet)
router.register(r'register', RegisterViewSet)
router.register(r'clazzs', ClazzListViewSet)
router.register(r'students', StudentViewSet)
router.register(r'practices', PracticeListViewSet)
router.register(r'records/choices', ChoiceRecordListViewSet)
router.register(r'records/fills', FillRecordListViewSet)
router.register(r'records/judges', JudgeRecordListViewSet)
router.register(r'records/programs', ProgramRecordListViewSet)
router.register(r'records/study', StudyRecordListViewSet)
router.register(r'studies', StudyListViewSet)


##打包后
router.register(r'api/exams', ExamListViewSet)
router.register(r'api/grades', GradeListViewSet)
router.register(r'api/choices', ChoiceListViewSet)
router.register(r'api/fills', FillListViewSet)
router.register(r'api/judges', JudgeListViewSet)
router.register(r'api/programs', ProgramListViewSet)
router.register(r'api/register', RegisterViewSet)
router.register(r'api/clazzs', ClazzListViewSet)
router.register(r'api/students', StudentViewSet)
router.register(r'api/practices', PracticeListViewSet)
router.register(r'api/records/choices', ChoiceRecordListViewSet)
router.register(r'api/records/fills', FillRecordListViewSet)
router.register(r'api/records/judges', JudgeRecordListViewSet)
router.register(r'api/records/programs', ProgramRecordListViewSet)
router.register(r'api/records/study', StudyRecordListViewSet)
router.register(r'api/studies', StudyListViewSet)
urlpatterns = [
    path(r'', TemplateView.as_view(template_name="index.html")),  ## 这里将url的根路径指向vue中的index页面
    path('xadmin/', xadmin.site.urls),
    path('docs/', include_docs_urls('Python在线考试系统')),
    path(r'api-auth/', include('rest_framework.urls')),
    path(r'jwt-auth/', obtain_jwt_token),
    path('check-program/', CheckProgramApi.as_view()),
    path('update-pwd/', UpdatePwdApi.as_view()),
    path("content/", ContentView.as_view()),  # 学习内容的目录
    path("learn/", LearnView.as_view()),  # 章节对应的学习内容
    # re_path(r'.*', TemplateView.as_view(template_name='index.html')),

    # 打包后
    path('api/xadmin/', xadmin.site.urls),
    path('api/docs/', include_docs_urls('Python在线考试系统')),
    path('api/api-auth/', include('rest_framework.urls')),
    path('api/jwt-auth/', obtain_jwt_token),
    path('api/check-program/', CheckProgramApi.as_view()),
    path('api/update-pwd/', UpdatePwdApi.as_view()),
    path("api/content/", ContentView.as_view()),  # 学习内容的目录
    path("api/learn/", LearnView.as_view()),  # 章节对应的学习内容
]
urlpatterns+=router.urls
# urlpatterns.append(path('api/exams', ExamListViewSet.as_view()))
# urlpatterns.append(path('api/grades', GradeListViewSet.as_view()))
# urlpatterns.append(path('api/choices', ChoiceListViewSet.as_view()))
# urlpatterns.append(path('api/fills', FillListViewSet.as_view()))
# urlpatterns.append(path('api/judges', JudgeListViewSet.as_view()))
# urlpatterns.append(path('api/programs', ProgramListViewSet.as_view()))
# urlpatterns.append(path('api/register', RegisterViewSet.as_view()))
# urlpatterns.append(path('api/clazzs', ClazzListViewSet.as_view()))
# urlpatterns.append(path('api/students', StudentViewSet.as_view()))
# urlpatterns.append(path('api/practices', PracticeListViewSet.as_view()))
# urlpatterns.append(path('api/records/choices', ChoiceRecordListViewSet.as_view()))
# urlpatterns.append(path('api/records/fills', FillRecordListViewSet.as_view()))
# urlpatterns.append(path('api/records/judges', JudgeRecordListViewSet.as_view()))
# urlpatterns.append(path('api/records/programs', ProgramRecordListViewSet.as_view()))
# urlpatterns.append(path('api/records/study', StudyRecordListViewSet.as_view()))
# urlpatterns.append(path('api/studies', StudyListViewSet.as_view()))
