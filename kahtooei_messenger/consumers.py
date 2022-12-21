from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
import json
from asgiref.sync import async_to_sync
from .models import Message
from .helper import getUsernameToken, getUserGroupList, fetch_user_messages, checkUserValidation, add_new_message_db, add_new_recipient_db, checkGroupValidation, add_group_recipients, set_message_received, set_message_seen,joinToGroup
# from channels import Group

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        # self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        # self.room_group_name = "chat_%s" % self.room_name
        self.room_group_name = "chat_kahtooei"
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    def receive(self, text_data):
        # text_data_json = json.loads(text_data)
        # message = text_data_json["message"]
        message = text_data

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "chat_message", "message": message}
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event["message"]

        # Send message to WebSocket
        self.send(text_data=json.dumps({"message": message}))

class ChatRoomConsumerAsync(AsyncWebsocketConsumer):
    async def connect(self):
        self.myroom = self.scope["url_route"]["kwargs"]["room_name"]
        self.mygroup = "chat_%s" % self.myroom
        # Join room group
        await self.channel_layer.group_add(
            self.mygroup, self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.mygroup, self.channel_name
        )

    async def receive(self, text_data):
        # text_data_json = json.loads(text_data)
        # message = text_data_json["message"]
        message = text_data

        # Send message to room group
        await self.channel_layer.group_send(
            self.mygroup, {"type": "chat_message", "message": message}
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]
        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message}))

class ChatRoomConsumer(WebsocketConsumer):
    def connect(self):
        self.token = self.scope["url_route"]["kwargs"]["token"]
        self.user = getUsernameToken(self.token)
        self.username = self.user.username
        self.allGroups = []
        if self.username:
            self.personalGroup = "chat_{}".format(self.username)
            async_to_sync(self.channel_layer.group_add)(
                self.personalGroup, self.channel_name
            )
            self.groupList = getUserGroupList(self.username)
            if len(self.groupList) > 0:
                for gname in self.groupList:
                    grp = "groupchat_{}".format(gname['groupname'])
                    self.allGroups.append(grp)
                    async_to_sync(self.channel_layer.group_add)(grp, self.channel_name)
            self.accept()
            self.self_send({"groups": self.groupList, "type_data": "groups"})
    def disconnect(self, close_code):
        if self.username:
            async_to_sync(self.channel_layer.group_discard)(
                self.personalGroup, self.channel_name
            )
        if len(self.allGroups) > 0:
            for grp in self.allGroups:
                async_to_sync(self.channel_layer.group_discard)(grp, self.channel_name)
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json.get('message',None)
        command = text_data_json.get('command',None)
        values = text_data_json.get('values',None)
        if command :
            if command == "fetch":
                self.fetch_messages()
            elif command == "send":
                self.new_message(message,values)
            elif command == "receive":
                self.receive_message(values)
            elif command == "seen":
                self.seen_message(values)
            elif command == "addMyGroup":
                self.add_mygroup(values)
    def fetch_messages(self):
        mesgs = fetch_user_messages(self.username)
        for msg in mesgs:
            msg['type_data'] = "fetch_message"
            self.self_send(msg)
    def new_message(self,content,receiver):
        groupname = receiver.get("groupname",None)
        username = receiver.get("username",None)
        if username:
            if checkUserValidation(username):
                chat = "chat_{}".format(username)
                message = add_new_message_db(self.username,content)
                message['receiver'] = username
                add_new_recipient_db(message.get("id"),username,None)
                message['status'] = 1 #message from user
                message['type_data'] = "new_message"
                self.other_send(message,chat)
                message['status'] = 3 #self message
                message['type_data'] = "new_message"
                self.self_send(message)
            else:
                invalid = dict(type="invalid user",status=-1)
                self.self_send(invalid)
        if groupname:
            if checkGroupValidation(self.username,groupname):
                groupchat = "groupchat_{}".format(groupname)
                message = add_new_message_db(self.username,content)
                add_group_recipients(message.get("id"),groupname,self.username)
                message['groupname'] = groupname
                message['status'] = 2 #message from group
                message['type_data'] = "new_message"
                self.other_send(message,groupchat)
            else:
                invalid = dict(type="invalid group",status=-2)
                self.self_send(invalid)      
    def self_send(self, message):
        rs = self.send(text_data=json.dumps({"message": message}))
    def other_send(self, message, group):
        async_to_sync(self.channel_layer.group_send)(
            group, {"type": "chat_message", "message": message}
        )
    def receive_message(self,data):
        messageID = data.get("messageID",None)
        if messageID:
            set_message_received(messageID,self.username)
    def seen_message(self,data):
        messageID = data.get("messageID",None)
        if messageID:
            set_message_seen(messageID,self.username)
    def add_mygroup(self,data):
        groupname = data.get("groupname",None)
        if groupname:
            res = joinToGroup(self.user,groupname)
            if res:
                self.groupList.append(groupname)
                grp = "groupchat_{}".format(groupname)
                self.allGroups.append(grp)
                async_to_sync(self.channel_layer.group_add)(grp, self.channel_name)
            
            
    def chat_message(self, event):
        message = event["message"]
        # Send message to WebSocket
        self.send(text_data=json.dumps({"message": message}))