import unittest
from chat import ChatBackend, app
from mock import MagicMock


class ChatBackendTest(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_site_up(self):
        rv = self.app.get('/')
        self.assertEqual(rv.status_code, 200)

    def test_create_backend(self):
        chat = ChatBackend()
        self.assertEqual(chat.subscriptions, [])

    def test_subscribe(self):
        chat = ChatBackend()
        chat.subscribe('websocket1', ['channelX', 'channelY'])
        chat.subscribe('websocket2', ['channelX', 'channelY'])
        self.assertEqual(len(chat.subscriptions), 2)

    def test_publish_subscribed(self):
        chat = ChatBackend()
        mock_websocket = MagicMock()
        mock_websocket.send = MagicMock()
        chat.subscribe(mock_websocket, ['channelX', 'channelY'])
        message = "{'handle': 'channelX', 'text': 'test message'}"
        chat.publish(message)
        mock_websocket.send.assert_called_once_with(message)

    def test_publish_unsubscribed(self):
        chat = ChatBackend()
        mock_websocket = MagicMock()
        mock_websocket.send = MagicMock()
        chat.subscribe(mock_websocket, ['channelX', 'channelY'])
        message = "{'handle': 'channelZ', 'text': 'test message'}"
        chat.publish(message)
        self.assertFalse(mock_websocket.send.called)

    def test_publish_no_client(self):
        chat = ChatBackend()
        mock_websocket = MagicMock()
        mock_websocket.send = MagicMock()
        mock_websocket.send = Exception("Boom!")
        chat.subscribe(mock_websocket, ['channelX', 'channelY'])
        message = "{'handle': 'channelX', 'text': 'test message'}"
        self.assertRaises(Exception, chat.publish(message))


if __name__ == '__main__':
    unittest.main()
