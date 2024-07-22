from django.db import models
from django.contrib.auth.models import User

class Friend(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10)
    dob = models.DateField()
    email = models.EmailField()

    def __str__(self):
        return self.user

class Message(models.Model):
    friend = models.ForeignKey(Friend, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.sender} to {self.receiver}: {self.text}'
    
