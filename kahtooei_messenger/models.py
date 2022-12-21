from django.db import models
from django.contrib.auth import get_user_model

# user = get_user_model()

class ChatUser(models.Model):
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=50, null=False, unique=True)
    password = models.CharField(max_length=50, null=False)
    inactive_date = models.DateTimeField(null=True)
    
    def for_message(self):
        return dict(
            name = self.name,
            username = self.username
        )

class Tokens(models.Model):
    user = models.ForeignKey(ChatUser,on_delete=models.CASCADE)
    token = models.CharField(max_length=100)
    create_date = models.DateTimeField(auto_now_add=True)

class ChatGroup(models.Model):
    name = models.CharField(max_length=100)
    groupname = models.CharField(max_length=50, null=False, unique=True)
    creator = models.ForeignKey(ChatUser,on_delete=models.CASCADE)
    delete_date = models.DateTimeField(null=True)
    
    def as_json(self):
        return dict(
            name = self.name,
            groupname = self.groupname,
            creator = self.creator.for_message()
        )

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
            id = self.id,
            content=self.content,
            author=self.author.for_message(),
            create_date=str(self.create_date)
        )
    
    def __str__(self):
        return self.sender.username

class UserRecipient(models.Model):
    message = models.ForeignKey(Message,on_delete=models.CASCADE)
    user = models.ForeignKey(ChatUser,on_delete=models.CASCADE)
    group = models.ForeignKey(ChatGroup,on_delete=models.CASCADE, null=True)
    send_date = models.DateTimeField(auto_now_add=True)
    receive_date = models.DateTimeField(null=True)
    seen_date = models.DateTimeField(null=True)
    def get_for_fetch(self,username):
        return dict(
            id = self.id,
            message = self.message.as_json(),
            group = self.group.as_json() if self.group else None,
            receiver = username,
            send_date = str(self.send_date)
        )






# class GroupRecipient(models.Model):
#     message = models.ForeignKey(Message,on_delete=models.CASCADE)
#     group = models.ForeignKey(ChatGroup,on_delete=models.CASCADE)
#     send_date = models.DateTimeField(auto_now_add=True)

# class GroupRecipientDetails(models.Model):
#     group_recipient = models.ForeignKey(GroupRecipient,on_delete=models.CASCADE)
#     user = models.ForeignKey(ChatUser,on_delete=models.CASCADE)
#     recive_date = models.DateTimeField(auto_now_add=True)
#     seen_date = models.DateTimeField(null=True)
    
    
