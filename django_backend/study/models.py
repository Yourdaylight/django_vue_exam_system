from django.db import models


# Create your models here.
class Study(models.Model):
    """学习资料"""
    name = models.CharField("学习资料目录名称", max_length=100)
    desc = models.TextField("学习内容描述", null=True, blank=True)
    relate_points = models.TextField("相关知识点", null=True, blank=True)
    relate_questions = models.TextField("相关题目", null=True, blank=True)
    study_times = models.IntegerField("学习次数", default=0)
    add_time = models.DateTimeField("添加时间", auto_now_add=True)

    class Meta:
        ordering = ['id']
        verbose_name = '资料库'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
