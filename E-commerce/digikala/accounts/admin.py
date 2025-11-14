from django.contrib import admin
from .models import User , Profile ,City , Province
# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ['id','username','first_name','last_name','email','mobile','is_active']
    search_fields = ['username']

    def delete_queryset(self, request, queryset):
        for user in queryset:
            user.delete()
admin.site.register(User,UserAdmin)
admin.site.register(Profile)
admin.site.register(Province)
admin.site.register(City)