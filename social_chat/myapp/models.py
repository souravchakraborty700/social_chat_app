# models.py
from django.db import models
from django.contrib.auth.models import User

class Interest(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_interests')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_interests')
    message = models.TextField()
    accepted = models.BooleanField(default=False)
    rejected = models.BooleanField(default=False)
    sender_notified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.sender} -> {self.recipient}"

class Message(models.Model):
    interest = models.ForeignKey(Interest, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)  # New field

    def __str__(self):
        return f"{self.sender}: {self.text[:20]}"
