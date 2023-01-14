
from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("edit_profile", views.edit_profile, name="edit_profile"),
    path("get_hometown/", views.get_hometown, name="get_hometown"),
    path("add_post", views.add_post, name="add_post"),
    path("delete_post/<int:post_id>", views.delete_post, name="delete_post"),

]
