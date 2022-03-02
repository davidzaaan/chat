from django.shortcuts import render
from .models import Room
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def index(request, user_name):
    return render(request, 'chat/index.html', {
        'user_name': user_name
    })

@login_required(login_url='login')
def room(request, user_name, room_name):
    chat_room, created = Room.objects.get_or_create(name=room_name)
    return render(request, 'chat/room.html', {
        'room_name': room_name,
        'user_name': user_name, # sending user authenticated
    })