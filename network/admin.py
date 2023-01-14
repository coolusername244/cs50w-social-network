from django.contrib import admin

from .models import User, Hometown


class UserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "username"
    )

class HometownAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "hometown"
    )


admin.site.register(User, UserAdmin)
admin.site.register(Hometown, HometownAdmin)
