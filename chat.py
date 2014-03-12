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
    """Interface for registering and updating WebSocket clients."""

    def __init__(self):
        self.subscriptions = list()

    def publish(self, message):
        channel = ast.literal_eval(message)['handle']
        for subscription in self.subscriptions:
            for subscribed_channel in subscription['channels']:
                if subscribed_channel == channel:
                    subscription['client'].send(message)

    def subscribe(self, client, channels):
        """Register a WebSocket connection."""
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
