import serial
from flask import Flask
import threading
import json
import signal
import sys
import time
import random

import pandas as pd

app = Flask(__name__)

def read_forces_from_serial():
    ser = serial.Serial(port="COM4", baudrate=9600, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)
    num_measurements = 0
    while True:
        if ser.in_waiting > 0:
            line = ser.readline()
            with open("force_data.csv", "a") as out:
                try:
                    line = line.decode("Ascii")
                    line = line.strip()
                    if line.strip() != "":
                        print("line: {}".format(line))
                        num_measurements += 1
                        if num_measurements % 10 == 0 and num_measurements != 0:
                            out.write(line)
                        else:
                            out.write(line + ",")
                except:
                    pass
            if num_measurements % 10 == 0 and num_measurements != 0:
                with open("force_data.csv", "a") as out:
                    out.write("\n")

def simulate_data_from_serial():
    num_measurements = 0
    while True:
        with open("sim_force_data.csv", "a") as out:
            if num_measurements < 100:
                num = random.randrange(0, 2)
                print(num)
                if num_measurements % 10 == 0 and num_measurements != 0:
                    out.write(str(num))
                else:
                    out.write(str(num) + ",")
            elif num_measurements >= 100 and num_measurements < 200:
                num = random.randrange(50, 120)
                print(num)
                if num_measurements % 10 == 0 and num_measurements != 0 :
                    out.write(str(num))
                else:
                    out.write(str(num) + ",")
            else:
                num = random.randrange(0, 2)
                print(num)
                if num_measurements % 10 == 0 and num_measurements != 0:
                    out.write(str(num))
                else:
                    out.write(str(num) + ",")

            if num_measurements % 10 == 0 and num_measurements != 0:
                out.write("\n")
        time.sleep(0.1)
        num_measurements += 1

@app.route("/", methods=['GET'])
def get_data():
    data = pd.read_csv("sim_force_data.csv")
    target_data = data.tail(3).values.tolist()
    headers = ["first_data", "second_data", "third_data"]
    return_data = {
        "first_data": [str(data) for data in target_data[0]],
        "second_data": [str(data) for data in target_data[1]],
        "third_data": [str(data) for data in target_data[2]]
    }
    print(json.dumps(return_data))
    return json.dumps(return_data)

if __name__ == '__main__':
    flask_thread = threading.Thread(target=lambda: app.run(host="143.215.84.249", port="5000", debug=True, use_reloader=False))
    flask_thread.start()
    simulate_data_from_serial()
    # read_forces_from_serial()