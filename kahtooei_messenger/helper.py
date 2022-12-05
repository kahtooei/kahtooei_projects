from .models import Tokens, GroupUser, ChatUser

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