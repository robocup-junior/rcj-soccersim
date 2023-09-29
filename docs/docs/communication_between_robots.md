# Communication between robots

Each of the robots is equipped with two Receivers and one Emitter. One of the
Receivers is used for receiving data from Supervisor. The Emitter and the second
Receiver can be used for sending and receiving data between robots from the
same team. We are going to describe what needs to be done in order to make use of it.

## Definition in the world file

Our world file defines one Emitter and one Receiver for team communication for
each robot. Blue team is assigned channel 2, while yellow team is assigned
channel 3. Webots supports changing channels, but we turned this feature off so teams
are not able to spam the opponent with a bunch of messages.
The name of the Emitter is set to `team emitter`, while the Receiver can be found
under name `team receiver`.

## Initializing the communication

The first thing we need to do in order to setup the communication is initialize
the Emitter and Receiver. To do so, just call following commands. We are going to use
the [OOP](https://en.wikipedia.org/wiki/Object-oriented_programming) approach here as well (see our sample robot controllers).

```python
self.team_emitter = self.robot.getDevice("team emitter")
self.team_receiver = self.robot.getDevice("team receiver")
self.team_receiver.enable(TIME_STEP)
```

Before using the Receiver, we must enable it with `enable(TIME_STEP)` command,
where `TIME_STEP` is the same value we use in our controller when calling
`self.robot.step(TIME_STEP)`.

## Sending a message

Each time we send a message via a channel, all the receivers listening on
this channel are going to receive it. So, if `robot1` sends a message,
`robot2` and `robot3` from the same team can read it.

### Converting the message into a packet

Webots supports sending the packet in different formats (string, bytes, list of doubles...).
Since our example controllers as well as supervisor use strings, let's describe how to send it.

[JSON](https://en.wikipedia.org/wiki/JSON) (JavaScript Object Notation) is an
open standard file format and data interchange format that uses human-readable
text to store and transmit data objects consisting of attribute–value pairs and
arrays (or other serializable values).
In short, it is very similar to the `dict` data structure that Python uses.
Starting from version 3.0, Python contains a built-in library called [json](https://docs.python.org/3/library/json.html). It
offers encoding Python's dictionaries into JSON string and later decoding it back to a dictionary.
This is very useful in our case because by reading the keys the receiver already knows what the
value means.

Let's create a simple message that we would like to send:

```python
data = {"robot_id": 1, "my_array": [1, 1.0, 2]}
```

Before sending the data, we must convert it to the string so the emitter is able to
encode it. As mentioned above, `json` library contains a method `dumps` that takes care
of that.

```python
packet = json.dumps(data)
```

The only thing we need to do is emit the packet by the Emitter. It is as easy
as just calling 

```python
self.team_emitter.send(packet)
```

and the message is succesfully sent to the channel.

### Receiving a message

When a Receiver receives a message, it adds it to the queue. We are then
able to pull the oldest message out of the queue.

To check the number of messages waiting in the queue, we can call

```python
self.team_receiver.getQueueLength()
```

If the there are new messages, the number of messages will be greater than 0 and
we can proceed with reading the message.

```python
packet = self.team_receiver.getString()
self.team_receiver.nextPacket()
```

In the first row we call the `getString()` method, which returns the packet and assigns
it to the `packet` variable. The `nextPacket()` method is used to move the pointer
to the next packet in the queue, so next time we are calling `getString()`, we are going
to read next packet in the queue.

Okay, now we have packet. How do we decode it? Well, remember our cool `json`
library? We are going to use it for decoding the packet, too.

```python
data = json.loads(packet)
```

The variable `data` now contains the same dictionary we sent by the emitter and can be
accessed as normal dictionary object.


**WARNING: There are 3 robots within the team running asynchronously. If all of them
are sending messages, it is always good to empty the queue before moving on, otherwise
the queue might grow and you will be reading old messages. You can use
a `while` loop for example**

```python
while self.team_receiver.getQueueLength() > 0:
    packet = self.team_receiver.getString()
    self.team_receiver.nextPacket()
    # Do something with the packet
```

**WARNING: Webots does not guarantee the order of messages. Your robot controllers should not rely on the order.
Instead, we recommend sending robot identifier in the message payload so the receiving robots clearly know which robot
originally sent the message.**
