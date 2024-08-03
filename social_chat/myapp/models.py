from django.db import models
from django.contrib.auth.models import User

class Interest(models.Model):
    sender = models.ForeignKey(User, related_name='sent_interests', on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, related_name='received_interests', on_delete=models.CASCADE)
    message = models.TextField()
    accepted = models.BooleanField(default=False)
    rejected = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Interest from {self.sender} to {self.recipient}"


