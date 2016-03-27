# The Portable Personal Air Conditioner

This project is a system to run a hexacopter that tracks a human head and follows it. The idea is to make the hexacopter hold an umbrella-like object to provide shelter from the sun, along with the air it blows while providing thrust to fly. The hexacopter should balance itself and keep following the owner to keep him cool in the heat of QATAR (Jihannam heat).

## Directory Structure
- debugger: This is a Django-based debugger/visualizer for the hexacopter to be run on a separate machine on the same network as the hexacopter.
- gyro: This is the code responsible for stabilization using the gyroscope. The directory has Arduino code and Raspberry Pi code.
- vision: This is a module to help tracking the owner's head using OpenCV.

## Requirements:
- Django framework
- openCV 2.4
- memcached
- Arduino IDE
- Python modules: requests, python-memcached, netifaces, pyserial, json
