from .models import Tokens, GroupUser, ChatUser, UserRecipient, Message, ChatGroup

#check token and return username
#check username and return groups

def getUsernameToken(token):
    t = Tokens.objects.filter(token = token).first()
    try:
        return t.user.username
    except:
        return None

def getUserGroupList(username):
    user = ChatUser.objects.filter(username=username).first()
    gu = GroupUser.objects.filter(user=user).all()
    if gu.count() > 0:
        return [g.group.groupname for g in gu]
    return []

def fetch_user_messages(username):
    user = ChatUser.objects.filter(username=username).first()
    msgs = UserRecipient.objects.filter(user=user,receive_date__isnull=True).all()
    if msgs.count() > 0:
        return [m.get_for_fetch() for m in msgs]
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
    
    
    
    
    