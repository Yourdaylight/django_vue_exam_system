import xadmin

from study.models import Study
from study.resource import StudyResource

class StudyAdmin(object):
    list_display = ['id', 'name', 'desc', 'relate_points', 'relate_questions', 'study_times', 'add_time']
    search_fields = ['name', 'desc', 'relate_points', 'relate_questions']
    list_filter = ['name', 'desc', 'relate_points', 'relate_questions', 'study_times', 'add_time']
    import_export_args = {'import_resource_class': StudyResource, 'export_resource_class': StudyResource}




xadmin.site.register(Study, StudyAdmin)
