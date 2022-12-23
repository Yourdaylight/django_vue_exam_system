from import_export import resources

from study.models import Study

class StudyResource(resources.ModelResource):
    class Meta:
        model = Study
        fields = ('id', 'name', 'desc', 'relate_points', 'relate_questions', 'study_times', 'add_time')
