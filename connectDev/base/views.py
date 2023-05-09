"""_summary_"""
from urllib.parse import unquote
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import RoomForm, UserForm, NewUserCreationForm
from .models import Room, Topic, Message, User

# Create your views here.
def login_page(request):
    page = "login"
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        email = request.POST.get("email").lower()
        password = request.POST.get("password")
        try:
            user = User.objects.get(email=email)
        except: # pylint: disable=bare-except
            messages.error(request, "User does not exists")

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user=user)
            return redirect("home")
        else:
            messages.error(request, "Email or Password does not exists")
    context = {"page": page}
    return render(request, "base/login.html", context)


def logout_User(request):
    logout(request)
    return redirect("home")


def register_page(request):
    form = NewUserCreationForm()
    if request.method == "POST":
        form = NewUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "An error occured during regisitration")

    context = {"form": form}
    return render(request, "base/login.html", context)


def home_page(request):
    q = unquote(request.GET.get("q")) if request.GET.get("q") is not None else ""
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) | Q(name__icontains=q) | Q(description__icontains=q)
    )
    recent_messages = Message.objects.filter(Q(room__topic__name__icontains=q))
    topics = Topic.objects.all()
    rooms_count = rooms.count()

    context = {
        "rooms": rooms,
        "topics": topics[:5],
        "rooms_count": rooms_count,
        "recent_messages": recent_messages,
    }
    return render(request, "base/home.html", context)


def room_page(request, index):
    room = Room.objects.get(id=index)
    room_messages = room.message_set.all().order_by("-created")  # type: ignore
    participants = room.participants.all()
    if request.method == "POST":
        message = Message.objects.create(
            user=request.user, room=room, body=request.POST.get("body")
        )
        message.save()
        room.participants.add(request.user)
        return redirect("room", index=room.pk)
    context = {
        "room": room,
        "room_messages": room_messages,
        "participants": participants,
    }
    return render(request, "base/room.html", context)


def profile_page(request, index):
    user = User.objects.get(id=index)
    rooms = user.room_set.all()  # type: ignore
    recent_messages = user.message_set.all()  # type: ignore
    topics = Topic.objects.all()
    context = {
        "user": user,
        "rooms": rooms,
        "topics": topics,
        "recent_messages": recent_messages,
    }
    return render(request, "base/profile.html", context)


@login_required(login_url="login")
def create_room(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == "POST":
        form = RoomForm(request.POST)
        topic = Topic.objects.get_or_create(name=request.POST.get("topic"))
        if form.is_valid():
            room = form.save(commit=False)
            room.host = request.user
            room.topic = topic[0]
            room.save()
            return redirect("home")
    context = {"form": form, "type": "Create", "topics": topics}
    return render(request, "base/create-room.html", context)


@login_required(login_url="login")
def update_room(request, index):
    room = Room.objects.get(id=index)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()
    if request.method == "POST":
        form = RoomForm(request.POST, instance=room)
        topic = Topic.objects.get_or_create(name=request.POST.get("topic"))
        if form.is_valid():
            room = form.save(commit=False)
            room.topic = topic[0]
            room.save()
            return redirect("home")

    context = {"form": form, "type": "Update", "topics": topics, "room": room}
    return render(request, "base/create-room.html", context)


@login_required(login_url="login")
def delete_room(request, index):
    room = Room.objects.get(id=index)
    if request.user != room.host:
        return HttpResponse("Your are not allowed here")
    if request.method == "POST":
        room.delete()
        return redirect("home")

    context = {"obj": "Room"}
    return render(request, "base/delete.html", context)


@login_required(login_url="login")
def delete_message(request, index):
    message = Message.objects.get(id=index)
    if request.user != message.user:
        return HttpResponse("Your are not allowed here")

    if request.method == "POST":
        message.delete()
        return redirect("home")

    context = {"obj": "message"}
    return render(request, "base/delete.html", context)


@login_required(login_url="login")
def update_user(request):
    user = request.user
    form = UserForm(instance=user)
    if request.method == "POST":
        form = UserForm(request.POST, instance=user)
        form.save()
        return redirect("user-profile", index=request.user.id)
    context = {"form": form}
    return render(request, "base/update-user.html", context)


def topics_page(request):
    q = unquote(request.GET.get("q")) if request.GET.get("q") is not None else ""
    topics = Topic.objects.filter(Q(name__icontains=q))
    context = {"topics": topics}
    return render(request, "base/topics.html", context)


def activity_page(request):
    q = unquote(request.GET.get("q")) if request.GET.get("q") is not None else ""
    recent_messages = Message.objects.filter(Q(room__topic__name__icontains=q))
    context = {"recent_messages": recent_messages}
    return render(request, "base/activity.html", context)
