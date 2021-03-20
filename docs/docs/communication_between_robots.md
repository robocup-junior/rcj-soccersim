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

Imagine we would like to send values `v1`, `v2`, ... , `vn`.
Before the message is sent to the channel, it must be converted into a packet.
Simply put, the packet is just a bytes object representing values `v1`, `v2`, ... , `vn`.
To convert our values into bytes object we can use built-in library
called [struct](https://docs.python.org/3/library/struct.html), which is
shipped together with Python.

We need to know the type of each value we want to pack into a packet. Let's see a
quick example. The values we want to send are `v1 = 3.14`, `v2 = 5` and `v3 = True`.
It is obvious that `v1` is floating point number, `v2` is integer and `v3`
is boolean. Knowing the type of each variable, we need to define the
structure of the message.

```python
message_format = "di?"
```

The `struct` library defines various symbols we might use in order to represent
a variable type. In our example `"d"` is representing floating point number,
`"i"` is representing integer and `"?"` is representing boolean value.
*If you want to use other variable types, check out
[the struct format characters documentation](https://docs.python.org/3/library/struct.html#format-characters)*.
Since we now know the structure of the message, we can create the packet

```python
packet = struct.pack(message_format, v1, v2, v3)
```

**Keep in mind that the order of variables passed to `pack()` function MUST be
in the same order as specified in `message_format`, otherwise you might get
a broken packet.**

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
packet = self.team_receiver.getData()
self.team_receiver.nextPacket()
```

In the first row we call the `getData()` method, which returns the packet and assigns
it to the `packet` variable. The `nextPacket()` method is used to move the pointer
to the next packet in the queue, so next time we are calling `getData()`, we are going
to read next packet in the queue.

Okay, now we have packet. How do we unpack it? Well, remember our cool `struct`
library? We are going to use it for unpacking the packet, too.

First of all, we need to know what data we expect. In our example, we sent
three variables in this order - floating point number, integer and boolean. Therefore,
we can define the format of the message here as well.

```python
message_format = 'di?'
```

Knowing what data to expect, we can unpack the packet by following command:

```python
unpacked = struct.unpack(message_format, packet)
```

The variable `unpacked` is a tuple with our values. If we print it, we will get
`(3.14, 5, True)`. We can access the values as we would for list
(or array in other languages)

```python
v1 = unpacked[0]
v2 = unpacked[1]
v3 = unpacked[2]
```


**WARNING: There are 3 robots within the team running asynchronously. If all of them
are sending messages, it is always good to empty the queue before moving on, otherwise
the queue might grow and you will be reading old messages. You can use
a `while` loop for example**

```python
while self.team_receiver.getQueueLength() > 0:
    packet = self.team_receiver.getData()
    self.team_receiver.nextPacket()
    # Do something with the packet
```
