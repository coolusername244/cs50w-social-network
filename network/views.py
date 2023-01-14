from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse

from .models import User, Hometown


def index(request):
    return render(request, "network/index.html")


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
                "bio": user.bio,
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