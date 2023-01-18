import json

from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_protect


from .models import User, Hometown, Posts, Likes, UserInfo, Following
from .forms import PostForm, UserInfoForm


def index(request):
    post_form = PostForm()
    posts = Posts.objects.all()
    posts = posts.order_by("-date").all()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    page_range = paginator.get_elided_page_range(number=page_number, on_each_side=1)

    context = {
        "posts": posts,
        "post_form": post_form,
        "page_obj": page_obj,
        "page_range": page_range,
    }

    return render(request, "network/index.html", context)


def my_feed(request):
    user = request.user
    followees = Following.objects.filter(follower=user).values()
    followees_ids = []
    for follwee in followees:
        followees_ids.append(follwee['followee_id'])
    posts = Posts.objects.filter(user__in=followees_ids)
    posts = posts.order_by("-date").all()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    page_range = paginator.get_elided_page_range(number=page_number, on_each_side=1)


    context = {
        "user": user,
        "followees": followees,
        "posts": posts,
        "page_obj": page_obj,
        "page_range": page_range,
    }
    return render(request, "network/my_feed.html", context)


def profile(request, user_id):
    user = User.objects.get(id=user_id)
    userId = user.id
    user_info = UserInfo.objects.get(user=userId)
    post_form = PostForm()
    posts = Posts.objects.filter(user=user)
    posts = posts.order_by("-date").all()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    page_range = paginator.get_elided_page_range(number=page_number, on_each_side=1)
    followers = Following.objects.filter(followee=user_id).count()
    following = Following.objects.filter(follower=user_id).count()
    is_following = Following.objects.filter(follower=request.user.id, followee = user_id)

    context = {
        "user": user,
        "user_info": user_info,
        "posts": posts,
        "post_form": post_form,
        "page_obj": page_obj,
        "page_range": page_range,
        "followers": followers,
        "following": following,
        "is_following": is_following,
    }
    return render(request, "network/profile.html", context)


def follow(request, user_id):
    if request.method == "POST":
        user = User.objects.get(id=user_id)
        Following.objects.create(follower=request.user, followee=user)
        return JsonResponse({"status": 200})



def unfollow(request, user_id):
    if request.method == "DELETE":
        Following.objects.filter(follower=request.user, followee=user_id).delete()
        return JsonResponse({"status": 200})



@csrf_protect
def add_post(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@csrf_protect
def delete_post(request, post_id):
    if request.method == 'DELETE':
        Posts.objects.filter(pk=post_id).delete()
        return JsonResponse({"message": "Message deleted"}, status=200)
    else:
        return HttpResponseRedirect(reverse('index'))


@csrf_protect
def edit_post(request, post_id):
    if request.method == 'PUT':
        data = request.body
        post_data = json.loads(data)
        post = post_data['post'].strip()
        Posts.objects.filter(id=post_id).update(post=post)
        return JsonResponse({"message": "message edited"})
    else:
        return HttpResponseRedirect(reverse('index'))


@csrf_protect
def like_post(request, post_id):
    if request.method == 'POST':
        # exists = 
        if not Likes.objects.filter(post=post_id, user=request.user):
            Likes.objects.create(user=request.user, post = Posts.objects.get(pk=post_id))
            likes = Likes.objects.filter(post=post_id).count()
            Posts.objects.filter(id=post_id).update(likes_count=likes)
            return JsonResponse({"message": "Like added"}, status=200)
        else:
            Likes.objects.filter(user=request.user, post=post_id).delete()
            likes = Likes.objects.filter(post=post_id).count()
            Posts.objects.filter(id=post_id).update(likes_count=likes)
            return JsonResponse({"message": "Like removed"}, status=200)
    else:
        return HttpResponseRedirect(reverse('index'))


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("edit_profile"))
    else:
        return render(request, "network/register.html")


@csrf_protect
def edit_profile(request):
    if request.method == "POST":
        form = UserInfoForm(request.POST, request.FILES)
        # if the user is updating for the second+ time:
        try:
            user_info = UserInfo.objects.get(user=request.user)
            if form.is_valid():
                user_info = get_object_or_404(UserInfo, user=request.user)
                if form.cleaned_data["profile_pic"]:
                    user_info.profile_pic = form.cleaned_data["profile_pic"]
                user_info.location = form.cleaned_data["location"]
                user_info.birthday =form.cleaned_data["birthday"]
                user_info.bio = form.cleaned_data["bio"]
                user_info.save()
                return HttpResponseRedirect(reverse("index"))
            else:
                context = {
                    "form": form
                }
                return render(request, "network/edit_profile.html", context)
        # If the user is updating for the first time:
        except UserInfo.DoesNotExist:   
            if form.is_valid():
                form.instance.user = request.user
                form.save()
                return HttpResponseRedirect(reverse("index"))
            else:
                context = {
                    "form": form
                }
                return render(request, "network/edit_profile.html", context)
    else:
        # check if user has filled form before
        try:
            user_info = UserInfo.objects.get(user=request.user)
            form = UserInfoForm(instance=user_info)
            context = {
                "user_info": user_info,
                "form": form
            }
            return render(request, 'network/edit_profile.html', context)
        # if user hasnt filled form before, render blank form
        except UserInfo.DoesNotExist:
            form = UserInfoForm()
            context = {
                "form": form
            }
            return render(request, 'network/edit_profile.html', context)


def get_hometown(request):
    search = request.GET.get('search')
    payload = []
    if search:
        objs = Hometown.objects.filter(hometown__contains = search)
        for obj in objs:
            payload.append(
                obj.hometown
            )
    return JsonResponse({
        'status': True,
        'payload': payload
    })