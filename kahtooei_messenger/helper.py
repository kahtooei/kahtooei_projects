from .models import Tokens, GroupUser, ChatUser, UserRecipient, Message, ChatGroup
from datetime import datetime
from uuid import uuid4
#check token and return username
#check username and return groups

def checkLogin(username,password):
    user = ChatUser.objects.filter(username=username,password=password,inactive_date__isnull=True).first()
    if user == None:
        return {'status': False}
    else:
        return {'status': True, 'user': user}

def registerUser(fullName,username,password):
    user = ChatUser(username=username,name=fullName,password=password)
    try:
        user.save()
        return {'status': True, 'user': user}
    except Exception as e:
        return {'status': False, 'error': str(e)}

def createNewToken():
    return str(uuid4()).replace("-","")

def createNewChatGroup(groupname,name,user):
    group = ChatGroup(groupname=groupname,name=name,creator=user)
    try:
        group.save()
        return {'status': True, 'group': group}
    except Exception as e:
        return {'status': False, 'error': str(e)}

def addUserToGroup(user,group):
    join = GroupUser.objects.filter(user=user,group=group).first()
    if not join:
        join = GroupUser(user=user,group=group)
        join.save()
        return {'status':True}
    else:
        if join.separate_date:
            return {'status': False, 'error': 'Duplicate Join'}
        else:
            join.separate_date = None
            join.save()
            return {'status':True}

def joinToGroup(user,groupname):
    group = ChatGroup.objects.filter(groupname=groupname).first()
    if group:
        join = GroupUser.objects.filter(user=user,group=group).first()
        if join:
            return True
        else:
            return False
    else:
        return False

def addNewUserToken(user,token):
    try:
        token = Tokens(user=user,token=token)
        token.save()
        return True
    except:
        return False

def getUsernameToken(token):
    t = Tokens.objects.filter(token = token).first()
    try:
        return t.user
    except:
        return None

def getUserByUsername(username):
    user = ChatUser.objects.filter(username=username,inactive_date__isnull=True).first()
    if user != None:
        return user
    else:
        return None

def checkExistGroup(groupname):
    group = ChatGroup.objects.filter(groupname=groupname).first()
    if group != None:
        return group
    else:
        return None

def getUserGroupList(username):
    user = ChatUser.objects.filter(username=username).first()
    gu = GroupUser.objects.filter(user=user).all()
    if gu.count() > 0:
        return [g.group.as_json() for g in gu]
    return []

def fetch_user_messages(username):
    user = ChatUser.objects.filter(username=username).first()
    msgs = UserRecipient.objects.filter(user=user,receive_date__isnull=True).all()
    if msgs.count() > 0:
        return [m.get_for_fetch(username) for m in msgs]
    return []

def checkUserValidation(username):
    user = ChatUser.objects.filter(username=username,inactive_date__isnull = True).first()
    if user:
        return True
    return False

def add_new_message_db(author,content):
    sender = ChatUser.objects.filter(username=author).first()
    msg = Message(author=sender, content=content)
    msg.save()
    return msg.as_json()

def add_new_recipient_db(messageID,receiver,groupname):
    user = ChatUser.objects.filter(username=receiver).first()
    msg = Message.objects.get(pk=messageID)
    grp = None
    if groupname:
        grp = ChatGroup.objects.filter(groupname=groupname).first()
    recipient = UserRecipient(user=user, message=msg, group=grp)
    recipient.save()
    # return recipient

def checkGroupValidation(username,groupname):
    user = ChatUser.objects.filter(username=username,inactive_date__isnull = True).first()
    group = ChatGroup.objects.filter(groupname=groupname ,delete_date__isnull=True).first()
    if user and group:
        groupuser = GroupUser.objects.filter(group=group,user=user,separate_date__isnull=True).first()
        if groupuser:
            return True
    return False

def getGroupMembers(group):
    members = GroupUser.objects.filter(group=group,separate_date__isnull=True).all()
    if members.count() > 0:
        return [m.user for m in members]
    return []

def add_group_recipients(messageID,groupname,author):
    group = ChatGroup.objects.filter(groupname=groupname).first()
    members = getGroupMembers(group)
    members = [m for m in members if m.username != author]
    for m in members:
        add_new_recipient_db(messageID,m.username,groupname)
    
def set_message_received(messageID,username):
    message = Message.objects.get(pk=messageID)
    user = ChatUser.objects.filter(username=username).first()
    recipient = UserRecipient.objects.filter(message=message,user=user, receive_date__isnull=True).first()
    if recipient:
        recipient.receive_date = datetime.utcnow()
        recipient.save()
    
def set_message_seen(messageID,username):
    message = Message.objects.get(pk=messageID)
    user = ChatUser.objects.filter(username=username).first()
    recipient = UserRecipient.objects.filter(message=message,user=user, seen_date__isnull=True).first()
    if recipient:
        current_time = datetime.utcnow()
        recipient.seen_date = datetime.utcnow()
        if not recipient.receive_date:
            recipient.receive_date = current_time
        recipient.save()





    