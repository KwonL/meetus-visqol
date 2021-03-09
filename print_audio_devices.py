from pprint import pprint

from pyaudio import PyAudio

pyaud = PyAudio()

for i in range(pyaud.get_device_count()):
    dev = pyaud.get_device_info_by_index(i)
    pprint(dev)
