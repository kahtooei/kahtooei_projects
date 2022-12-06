from .models import Tokens, GroupUser, ChatUser, UserRecipient

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
    msgs = UserRecipient.objects.filter(user=user,receive_date__isnull=True)
    if msgs.count() > 0:
        return [m.get_for_fetch() for m in msgs]
    return []
    