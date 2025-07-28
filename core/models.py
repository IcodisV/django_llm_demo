from django.db import models

class Conversation(models.Model):
    question = models.TextField()
    answer = models.TextField()
    is_vegetarian = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
