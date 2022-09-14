import pandas as pd
import numpy as np
import time
from datetime import datetime
from pynput import keyboard
import PureThermal

# create class objects
thermal = PureThermal.PureThermal()

expData = []
q_current = [1, 2, 3, 4, 5]

START_DATA_FLOW = {keyboard.KeyCode.from_char('q')}
STOP_AND_SAVE = {keyboard.KeyCode.from_char('s')}
# The currently active modifiers
current_keys = set()


def update_data():
    timeStamp = datetime.now().strftime("%H:%M:%S")
    expData.append([timeStamp, 0, 0, 0, 0])
    # print(expData)


def on_press(key):
    global current_keys
    flag = True
    if key in START_DATA_FLOW:
        current_keys.add(key)
        if all(k in current_keys for k in START_DATA_FLOW):
            print('Start recording')
            flag = False
            update_data()

    if key in STOP_AND_SAVE:
        current_keys.add(key)
        if all(k in current_keys for k in STOP_AND_SAVE):
            print('Stop and save')
            flag = False
            record_data()


def on_release(key):
    global current_keys
    try:
        current_keys.remove(key)
        # controller.moveRobotM(np.aqrray([0, 0, 0, 0]), s_current, False, False)
    except KeyError:
        pass


def record_data():
    columnNames = ["time", "temperature", "ka*", "kb*", "ka", "kb"]
    df = pd.DataFrame(expData, columns=columnNames)
    print("save")
    df.to_csv('WubbaLubbaDubDub.csv', index=False)
    # controller.closeConnection()


if __name__ == "__main__":
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()
