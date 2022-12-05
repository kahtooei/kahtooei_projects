from django.db import models
from django.contrib.auth import get_user_model

# user = get_user_model()

class ChatUser(models.Model):
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=50, null=False, unique=True)
    password = models.CharField(max_length=50, null=False)
    inactive_date = models.BooleanField(default=True)#what happen if a username deleted and want to create again???

class ChatGroup(models.Model):
    name = models.CharField(max_length=100)
    groupname = models.CharField(max_length=50, null=False, unique=True)
    creator = models.ForeignKey(ChatUser,on_delete=models.CASCADE)
    delete_date = models.BooleanField(default=True)

class GroupUser(models.Model):
    group = models.ForeignKey(ChatGroup,on_delete=models.CASCADE)
    user = models.ForeignKey(ChatUser,on_delete=models.CASCADE)
    join_date = models.DateTimeField(auto_now_add=True)
    separate_date = models.DateTimeField(null=True)
    
#join datetime

class Message(models.Model):
    content = models.TextField()
    # sender = models.ForeignKey(user,on_delete=models.CASCADE)
    author = models.ForeignKey(ChatUser,on_delete=models.CASCADE)
    create_date = models.DateTimeField(auto_now_add=True)
    
    def as_json(self):
        return dict(
            content=self.content,
            sender=self.sender.username,
            create_date=self.create_date
        )
    def get_lastMessages():
        return Message.objects.order_by("-create_date").all()
    
    def __str__(self):
        return self.sender.username

class UserRecipient(models.Model):
    message = models.ForeignKey(Message,on_delete=models.CASCADE)
    user = models.ForeignKey(ChatUser,on_delete=models.CASCADE)
    group = models.ForeignKey(ChatGroup,on_delete=models.CASCADE, null=True)
    send_date = models.DateTimeField(auto_now_add=True)
    recive_date = models.DateTimeField(null=True)
    seen_date = models.DateTimeField(null=True)






# class GroupRecipient(models.Model):
#     message = models.ForeignKey(Message,on_delete=models.CASCADE)
#     group = models.ForeignKey(ChatGroup,on_delete=models.CASCADE)
#     send_date = models.DateTimeField(auto_now_add=True)

# class GroupRecipientDetails(models.Model):
#     group_recipient = models.ForeignKey(GroupRecipient,on_delete=models.CASCADE)
#     user = models.ForeignKey(ChatUser,on_delete=models.CASCADE)
#     recive_date = models.DateTimeField(auto_now_add=True)
#     seen_date = models.DateTimeField(null=True)
    
    
