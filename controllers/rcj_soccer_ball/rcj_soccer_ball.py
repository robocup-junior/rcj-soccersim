import struct

from controller import Robot

robot = Robot()
ball_emitter = robot.getDevice("ball emitter")
ball_emitter_short = robot.getDevice("ball emitter short")

data = [True]  # Packet cannot be empty
packet = struct.pack("?", *data)

while robot.step(32) != -1:
    ball_emitter.send(packet)
    ball_emitter_short.send(packet)
