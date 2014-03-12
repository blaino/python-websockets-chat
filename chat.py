# -*- coding: utf-8 -*-

"""
Chat Server
===========

This simple application uses WebSockets to run a primitive chat server.
"""

import ast
import os
import time
from flask import Flask, render_template
from flask_sockets import Sockets

app = Flask(__name__)
app.debug = 'DEBUG' in os.environ

sockets = Sockets(app)


class ChatBackend(object):

    def __init__(self):
        """Maintain list of subscriptions (client, list of channels pair)."""
        self.subscriptions = list()

    def publish(self, message):
        """Send message to client if client is subsribed."""
        for subscription in self.subscriptions:
            for subscribed_channel in subscription['channels']:
                channel = ast.literal_eval(message)['handle']
                if subscribed_channel == channel:
                    try:
                        subscription['client'].send(message)
                    except Exception:
                        self.subscriptions.remove(subscription)

    def subscribe(self, client, channels):
        """Add a subscription (client, list of channels pair)."""
        subscription = {'client': client, 'channels': channels}
        self.subscriptions.append(subscription)


chats = ChatBackend()


@app.route('/')
def hello():
    return render_template('index.html')


@sockets.route('/submit')
def inbox(ws):
    """Receives incoming chat messages, inserts them into Redis."""
    while ws.socket is not None:
        # Sleep to prevent *contstant* context-switches.
        time.sleep(0.1)
        message = ws.receive()

        if message:
            chats.publish(message)


@sockets.route('/receive')
def outbox(ws):
    """Sends outgoing chat messages, via `ChatBackend`."""
    chats.subscribe(ws, ['channel1', 'channel2'])

    while ws.socket is not None:
        # Context switch while `ChatBackend` is running in the background.
        time.sleep()
