# Generated by Django 3.0.3 on 2020-04-01 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
        ('exam', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='exam',
            name='students',
            field=models.ManyToManyField(to='user.Student', verbose_name='可以参加考试的学生'),
        ),
        migrations.AlterField(
            model_name='paper',
            name='program_number',
            field=models.PositiveSmallIntegerField(default=5, verbose_name='编程题数'),
        ),
    ]
