class Chatroom:

    def __init__(self, room_name):
        self.room_name = room_name
        self.messages = list()
        self.message_observers = []

    def publish(self, message):
        self.messages.append(message)
        for observer in self.message_observers:
            observer.chatroom_callback(message, self.room_name)

    def subscribe(self, observer):
        print "Subscribed: "
        print observer
        self.message_observers.append(observer)

    def listen(self):
        for message in self.messages:
            yield message


class ChatroomObserver:

    def __init__(self, observer_name):
        self.name = observer_name

    def chatroom_callback(self, message, room_name):
        print self.name + " observed a new message in " + room_name
        print "The message says: " + message


# >>> from observer import *

# >>> cr1 = Chatroom("ch1")

# >>> alice = ChatroomObserver("alice")
# >>> bob = ChatroomObserver("bob")

# >>> cr1.subscribe(bob)
# >>> cr1.subscribe(alice)

# >>> cr1.publish("blik")

# bob observed a new message in ch1
# The message says: blik
# alice observed a new message in ch1
# The message says: blik
