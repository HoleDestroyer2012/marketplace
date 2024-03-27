from channels.consumer import SyncConsumer, AsyncConsumer
from channels.exceptions import StopConsumer


class MySyncConsumer(SyncConsumer):

    def websocket_connect(self, event):
        print('Websocket connected', event)
        self.send({
            'type': 'websocket.accept'
        })

    def websocket_receive(self, event):
        print('Message is ', event['text'])
        self.send({
            'type': 'websocket.send',
            'text': 'Message Sent to Client'
        })

    def websocket_disconnect(self, event):
        print('Websocket Disconnected', event)
        raise StopConsumer()


class MyAsyncConsumer(AsyncConsumer):

    async def websocket_connect(self, event):
        print('Websocket connected', event)
        await self.send({
            'type': 'websocket.accept'
        })

    async def websocket_receive(self, event):
        print('Message is ', event['text'])
        await self.send({
            'type': 'websocket.send',
            'text': 'Message Sent to Client'
        })

    async def websocket_disconnect(self, event):
        print('Websocket Disconnected', event)
        raise StopConsumer()
