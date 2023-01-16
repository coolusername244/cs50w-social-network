from django.contrib import admin

from .models import User, Hometown, UserInfo, Posts


class UserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "username"
    )

class UserInfoAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "profile_pic",
        "birthday",
        "location",
        "bio",
    )

class PostAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "post",
        "date",
        "likes_count",
    )

class HometownAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "hometown"
    )


admin.site.register(User, UserAdmin)
admin.site.register(Hometown, HometownAdmin)
admin.site.register(UserInfo, UserInfoAdmin)
admin.site.register(Posts, PostAdmin)
