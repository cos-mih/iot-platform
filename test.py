from json import dumps, load
from numpy import arange
from random import choice
from sys import stdin
from time import sleep

import paho.mqtt.client as mqtt

class SensorData:
    def __init__(self, bat, tmp, hmd, co2=None, pm25=None, light=None, noise=None):
        self.bat = bat
        self.tmp = tmp
        self.hmd = hmd
        self.co2 = co2
        self.pm25 = pm25
        self.light = light
        self.noise = noise

    def to_dict(self):
        return {
            'BAT': self.bat,
            'TMP': self.tmp,
            'HMD': self.hmd,
            'CO2': self.co2,
            'PM25': self.pm25,
            'LIGHT': self.light,
            'NOISE': self.noise
        }

def main():
    client = mqtt.Client()
    client.connect("172.18.128.1")
    client.loop_start()

    bat_range = range(25, 101)
    tmp_range = range(20, 31)
    hmd_range = range(30, 41)
    co2_range = range(400, 501)
    pm25_range = range(0, 31)
    light_range = range(0, 1001)
    noise_range = range(30, 81)

    stations = {
        "UPB": ["Precis", "EG", "EC"],
        "UBB": ["city_center", "city_park", "city_suburb"],
        "MIT": ["park_north", "park_south", "park_center"],
        "Oxford": ["campus_gate", "campus_library", "campus_labs"],
    }

    while True:
        station_type = choice(list(stations.keys()))
        location = choice(stations[station_type])

        data = SensorData(
            bat=choice(bat_range),
            tmp=choice(tmp_range),
            hmd=choice(hmd_range),
            co2=choice(co2_range),
            pm25=choice(pm25_range),
            light=choice(light_range),
            noise=choice(noise_range)
        )

        client.publish(f"{station_type}/{location}", dumps(data.to_dict()))

        sleep(choice([0.5, 1.5]))
main()