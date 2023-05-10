from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import Permission
# Create your models here.
class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    subject = models.CharField(max_length=255)
    body = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    message_id = models.AutoField(primary_key=True)

    @staticmethod
    def search(query):
        messages = Message.objects.filter(subject__icontains=query)
        return messages
    def __str__(self):
        return f"From: {self.sender.username}, To: {self.recipient.username}, Subject: {self.subject}"
class MessageRequest(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages_request')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages_request')
    subject = models.CharField(max_length=255)
    body = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    def __str__(self):
        return f"From: {self.sender.username}, To: {self.recipient.username}, Subject: {self.subject}"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to='item_pictures', blank=True, null=True)
    id=models.AutoField(primary_key=True)
    def __str__(self):
        return f'{self.user.username} Profile'
