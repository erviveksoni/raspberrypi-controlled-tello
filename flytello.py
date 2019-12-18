#!/usr/bin/env python3

import asyncio
import math
import os
import signal
import subprocess
import sys
import threading
import time
import tellopy
import traceback

from evdev import InputDevice, ecodes, ff, list_devices

import gamepad

drone = None
prev_flight_data = None
run_recv_thread = True
flight_data = None
log_data = None
is_drone_connected = False
speed = 100
throttle = 0.0
yaw = 0.0
pitch = 0.0
roll = 0.0


def connect_drone():
    mydrone = tellopy.Tello()
    mydrone.subscribe(mydrone.EVENT_CONNECTED, drone_event_handler)
    mydrone.subscribe(mydrone.EVENT_DISCONNECTED, drone_event_handler)
    mydrone.subscribe(mydrone.EVENT_FLIGHT_DATA, drone_event_handler)
    mydrone.subscribe(mydrone.EVENT_LOG, drone_event_handler)
    mydrone.connect()
    mydrone.wait_for_connection(60.0)
    return mydrone


def drone_event_handler(event, sender, data, **args):
    global prev_flight_event, prev_flight_data, flight_data, log_data, is_drone_connected
    mydrone = sender
    if event is mydrone.EVENT_CONNECTED:
        is_drone_connected = True
    elif event is mydrone.EVENT_DISCONNECTED:
        print("Disconnected from drone!...")
        is_drone_connected = False
        drone.quit()
    elif event is mydrone.EVENT_FLIGHT_DATA:
        if prev_flight_data != str(data):
            print(data)
            prev_flight_data = str(data)
        flight_data = data
    elif event is mydrone.EVENT_LOG:
        log_data = data
        # print(self.log_data)
    else:
        print('event="%s" data=%s' % (event.getname(), str(data)))


def force_stop_drone(drone_flight_data):
    if drone_flight_data is None or len(drone_flight_data) < 1:
        return False

    # ALT:  9 | SPD:  0 | BAT: 31 | WIFI: 70 | CAM:  0 | MODE: 12
    telemetry_data_raw = drone_flight_data.split("|")
    telemetry_data = {}
    for item in telemetry_data_raw:
        telemetry_item = item.replace(" ", "").split(":")
        telemetry_data[telemetry_item[0]] = telemetry_item[1]

    # print ("Original dictionary is : " + str(telemetry_data))
    if int(telemetry_data["ALT"]) <= 0 or int(telemetry_data["BAT"]) <= 10:
        return True
    return False


def connect_gamepad():  # asyncronus read-out of events
    xbox_path = None
    remote_control = None
    devices = [InputDevice(path) for path in list_devices()]
    print('Connecting to xbox controller...')
    for device in devices:
        if str.lower(device.name) == "xbox wireless controller":
            xbox_path = str(device.path)
            remote_control = gamepad.gamepad(file=xbox_path)
            remote_control.rumble_effect = 2
            return remote_control
    return None


def is_gamepad_connected():  # asyncronus read-out of events
    xbox_path = None
    devices = [InputDevice(path) for path in list_devices()]
    for device in devices:
        if str.lower(device.name) == "xbox wireless controller":
            xbox_path = str(device.path)
    if xbox_path is None:
        print("Xbox controller disconnected!!")
        return False
    return True


def update(old, new, max_delta=0.3):
    if abs(old - new) <= max_delta:
        res = new
    else:
        res = 0.0
    return res


async def read_gamepad_inputs():
    print("Ready to fly!!")
    global throttle, yaw, pitch, roll
    while is_drone_connected and is_gamepad_connected() and remote_control.button_b is False:
        # print(" trigger_right = ", round(remote_control.trigger_right,2),end="\r")
        leftx = round(remote_control.joystick_left_x, 2)
        lefty = round(remote_control.joystick_left_y, 2)
        rightx = round(remote_control.joystick_right_x, 2)
        righty = round(remote_control.joystick_right_y, 2)
        # print("x:", x, " y:", y, end="\r")
        # print("x:", x, " y:", y, " direction: ",direction,end="\r")

        if remote_control.joystick_left_y_flag:
            throttle = update(throttle, lefty)
            drone.set_throttle(throttle)
            remote_control.joystick_left_y_flag = False

        if remote_control.joystick_left_x_flag:
            yaw = update(yaw, leftx)
            drone.set_yaw(yaw)
            remote_control.joystick_left_x_flag = False

        if remote_control.joystick_right_y_flag:
            pitch = update(pitch, righty)
            drone.set_pitch(pitch)
            remote_control.joystick_right_y_flag = False

        if remote_control.joystick_right_x_flag:
            roll = update(roll, rightx)
            drone.set_roll(roll)
            remote_control.joystick_right_x_flag = False

        if remote_control.button_menu:
            drone.takeoff()

        if remote_control.button_view:
            drone.land()

        if remote_control.dpad is True:
            if remote_control.dpad_left_right < 0:
                drone.counter_clockwise(speed)
            if remote_control.dpad_left_right == 0:
                drone.clockwise(0)
            if remote_control.dpad_left_right > 0:
                drone.clockwise(speed)
            if remote_control.dpad_up_down < 0:
                drone.up(speed)
            if remote_control.dpad_up_down == 0:
                drone.up(0)
            if remote_control.dpad_up_down > 0:
                drone.down(speed)
            remote_control.dpad = False

        if round(remote_control.trigger_right, 2) == 1.00:
            print("FLIP FORWARD")
            drone.flip_forward()
            remote_control.trigger_right = -1
        if round(remote_control.trigger_left, 2) == 1.00:
            print("FLIP BACK")
            drone.flip_back()
            remote_control.trigger_left = -1
        if remote_control.bump_right:
            print("FLIP RIGHT")
            drone.flip_right()
            remote_control.bump_right = False
        if remote_control.bump_left:
            print("FLIP LEFT")
            drone.flip_left()
            remote_control.bump_left = False

        if remote_control.button_a:
            drone.palm_land()
            remote_control.button_a = False

        await asyncio.sleep(10e-3)  # 10ms
    return


async def removetasks(loop):
    tasks = [t for t in asyncio.all_tasks() if t is not
             asyncio.current_task()]

    for task in tasks:
        # skipping over shielded coro still does not help
        if task._coro.__name__ == "cant_stop_me":
            continue
        task.cancel()

    print("Cancelling outstanding tasks")
    await asyncio.gather(*tasks, return_exceptions=True)
    loop.stop()


async def shutdown_signal(signal, loop):
    print(f"Received exit signal {signal.name}...")
    await removetasks(loop)


if __name__ == "__main__":
    remote_control = None
    loop = asyncio.get_event_loop()
    signals = (signal.SIGHUP, signal.SIGTERM, signal.SIGINT)

    for s in signals:
        loop.add_signal_handler(
            s, lambda s=s: asyncio.create_task(shutdown_signal(s, loop)))
    try:
        remote_control = connect_gamepad()
        if remote_control is None:
            print('Please connect an Xbox controller then restart the program!')
            sys.exit()

        drone = connect_drone()
        remote_control.rumble_effect = 2

        tasks = [remote_control.read_gamepad_input(), remote_control.rumble(), read_gamepad_inputs()]
        loop.run_until_complete(asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED))
        loop.run_until_complete(removetasks(loop))

    except Exception as e:
        # exc_type, exc_value, exc_traceback = sys.exc_info()
        # traceback.print_exception(exc_type, exc_value, exc_traceback)
        print(e)
    finally:
        if remote_control is not None:
            remote_control.power_on = False
            remote_control.erase_rumble()

        if drone is not None:
            drone.land()
            drone.quit()

        print("Closing async loop..")
        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()
        print("Done..")
