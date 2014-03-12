import unittest
from chat import ChatBackend


class ChatBackendTest(unittest.TestCase):

    def test_create_backend(self):
        chat = ChatBackend()
        self.assertEqual(chat.subscriptions, [])

    def test_subscribe(self):
        chat = ChatBackend()
        chat.subscribe("websocket1", ['channelX', 'channelY'])
        chat.subscribe("websocket2", ['channelX', 'channelY'])
        self.assertEqual(len(chat.subscriptions), 2)

    def test_publish(self):
        pass

if __name__ == '__main__':
    unittest.main()
