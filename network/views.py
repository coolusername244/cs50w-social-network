import json

from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_protect


from .models import User, Hometown, Posts, Likes
from .forms import PostForm


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


@csrf_protect
def add_post(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            return HttpResponseRedirect(reverse('index'))
        else:
            return HttpResponseRedirect(reverse('index'))
    else:
        return HttpResponseRedirect(reverse('index'))


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
    if request.user.is_authenticated:
        if request.method == "POST":
            # Gather form data
            first_name = request.POST["first_name"]
            last_name = request.POST["last_name"]
            profile_pic = request.POST["profile_pic"]
            birthday = request.POST["birthday"]
            location = request.POST["location"]
            bio = request.POST["bio"]

            # Update user profile
            User.objects.filter(username=request.user).update(
                first_name=first_name,
                last_name=last_name,
                profile_pic=profile_pic,
                birthday=birthday,
                location=location,
                bio=bio,
            )

            # Redirect to home page
            return HttpResponseRedirect(reverse("index"))
        else:
            user = User.objects.get(id=request.user.id)

            context = {
                "first_name": user.first_name,
                "last_name": user.last_name,
                "profile_pic": user.profile_pic,
                "birthday": user.birthday,
                "location": user.location,
                "bio": user.bio.strip(),
            }

            return render(request, "network/edit_profile.html", context)
    else:
        return HttpResponseRedirect(reverse("login"))


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