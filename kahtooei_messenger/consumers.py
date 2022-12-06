from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
import json
from asgiref.sync import async_to_sync
from .models import Message
from .helper import getUsernameToken, getUserGroupList, fetch_user_messages
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
        self.username = getUsernameToken(self.token)
        self.allGroups = []
        if self.username:
            self.personalGroup = "chat_%s" % self.username
            async_to_sync(self.channel_layer.group_add)(
                self.personalGroup, self.channel_name
            )
            groupList = getUserGroupList(self.username)
            if len(groupList) > 0:
                for gname in groupList:
                    grp = "groupchat_%s" % gname
                    self.allGroups.append(grp)
                    async_to_sync(self.channel_layer.group_add)(grp, self.channel_name)
            self.accept()

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
        # async_to_sync(self.channel_layer.group_send)(
        #     self.mygroup, {"type": "chat_message", "message": message}
        # )

    # Receive message from room group
    def chat_message(self, event):
        message = event["message"]
        # Send message to WebSocket
        self.send(text_data=json.dumps({"message": message}))
    
    def fetch_messages(self):
        mesgs = fetch_user_messages(self.username)
        self.self_send(mesgs)
    def new_message(self,content,receiver):
        print("send-message : {}".format(content))
    def self_send(self, message):
        rs = self.send(text_data=str(message))
    def other_send(self, message, group):
        async_to_sync(self.channel_layer.group_send)(
            group, {"type": "chat_message", "message": str(message)}
        )
    def receive_message(self,messageID):
        print("add to database message received for this user")
    def seen_message(self,messageID):
        print("add to database message received for this user")
    