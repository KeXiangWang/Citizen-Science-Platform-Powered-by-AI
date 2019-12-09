from django.contrib import admin
from .models import *
# from ..User.models import UserInfo
# Register your models here.


class ProjectAdmin(admin.ModelAdmin):
    list_display = ['projection_name', 'publisher', 'area', 'publish_time']
    search_fields = ['projection_name', 'projection_introduction']
    list_filter = ['publisher','area','publish_time']
    list_per_page = 30


class DataInfoAdmin(admin.ModelAdmin):
    # list_display = ['data_name', 'data_location', 'uid']
    list_filter = ['data_time', 'data_name', 'data_location']
    search_fields = ['data_name', 'data_path', 'data_location']
    list_per_page = 30


admin.site.register(ProjectInfo, ProjectAdmin)
admin.site.register(ProjectImage)
admin.site.register(DataInfo, DataInfoAdmin)
admin.site.register(DomainInfo)
admin.site.register(ModelInfo)
admin.site.register(UserProjectAuthority)
admin.site.register(IssueInfo)
admin.site.register(CommentInfo)
admin.site.register(ProjectIssue)
# admin.site.register(UserInfo)