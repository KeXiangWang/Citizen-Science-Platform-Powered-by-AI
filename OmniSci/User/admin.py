from django.contrib import admin
from .models import UserInfo
from .models import UnauthorizedUserInfo
from .models import UserVisitRecord


class UserAdmin(admin.ModelAdmin):
    list_display = ['user_name', 'register_date', 'credit', 'user_introduction']
    search_fields = ['user_name']
    list_filter = ['register_date','sex']
    list_per_page = 30
# Register your models here.
admin.site.register(UserInfo,UserAdmin)
admin.site.register(UnauthorizedUserInfo)
admin.site.register(UserVisitRecord)