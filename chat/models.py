from enum import unique
from django.db import models
from django.contrib.auth.models import User

class Room(models.Model):
    name = models.CharField(max_length=128, unique=True)
    online = models.ManyToManyField(to=User, blank=True)

    """ Retrieve the total count of online people """
    def get_online_count(self):
        return self.online.count()

    """ When a user joins the chat room """
    def join(self, user):
        self.online.add(user)
        print(f"User added: {user}")
        self.save()

    """ Removing user when leaves the chat room """
    def leave(self, user):
        self.online.remove(user)
        print(f"User removed: {user}")
        self.save()

    """ Getting all the users online """
    def get_online_users(self):
        return [user for user in self.online.all()]


class Message(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    room = models.ForeignKey(to=Room, on_delete=models.CASCADE)
    content = models.CharField(max_length=512)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username}: {self.content} [{self.timestamp}]'
