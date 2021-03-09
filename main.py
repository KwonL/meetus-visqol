import argparse
import wave
from threading import Thread, Semaphore

import pyaudio

from delay import get_delay_for_inout
from visqol import run_visqol

CHUNK = 1024
FORMAT = pyaudio.paInt16
RATE = 48000
RECORD_SECONDS = 10
WAVE_INPUT_FILENAME = "input.wav"
WAVE_OUTPUT_FILENAME = "output.wav"
IN_DEVICE_NAME = "BY Hi-Res"
OUT_DEVICE_NAME = "외장"
semaphore = Semaphore(0)


def stream_file_to_dev(pyaud: pyaudio.PyAudio, dev: dict):
    input_file = wave.open(WAVE_INPUT_FILENAME, "rb")
    output_stream = pyaud.open(
        format=pyaudio.get_format_from_width(input_file.getsampwidth()),
        channels=input_file.getnchannels(),
        output_device_index=dev.get("index"),
        rate=input_file.getframerate(),
        output=True,
    )
    input_file.close()
    file = open(WAVE_INPUT_FILENAME, "rb")
    semaphore.release()
    output_stream.write(file.read())
    file.close()


def record_testing():
    pyaud = pyaudio.PyAudio()

    global RECORD_SECONDS
    global RATE
    with wave.open(WAVE_INPUT_FILENAME, "rb") as f:
        RECORD_SECONDS = f.getnframes() / float(f.getframerate()) + 1
        RATE = f.getframerate()
    print(f"duration is {RECORD_SECONDS}")

    # Find device
    in_dev = dict()
    out_dev = dict()
    for i in range(pyaud.get_device_count()):
        dev = pyaud.get_device_info_by_index(i)
        print(dev)
        if IN_DEVICE_NAME in dev.get("name") and dev["maxInputChannels"] > 0:
            in_dev = dev
        elif OUT_DEVICE_NAME in dev.get("name") and dev["maxOutputChannels"] > 0:
            out_dev = dev

    input_stream = pyaud.open(
        format=FORMAT,
        channels=in_dev.get("maxInputChannels"),
        input_device_index=in_dev.get("index"),
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK,
    )
    streaming_thread = Thread(target=stream_file_to_dev, args=(pyaud, out_dev))
    streaming_thread.start()

    print("* start recording")
    semaphore.acquire()
    frames = []
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = input_stream.read(CHUNK)
        frames.append(data)
    print("* done recording")

    input_stream.stop_stream()
    input_stream.close()
    pyaud.terminate()

    wf = wave.open(WAVE_OUTPUT_FILENAME, "wb")
    wf.setnchannels(in_dev.get("maxInputChannels"))
    wf.setsampwidth(pyaud.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b"".join(frames))
    wf.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-file", "-i", type=str, help="테스트용 입력 파일")
    args = parser.parse_args()

    WAVE_INPUT_FILENAME = args.input_file

    record_testing()
    run_visqol(WAVE_INPUT_FILENAME, WAVE_OUTPUT_FILENAME)
    print("=============================================")
    print(
        f"delay for this audio is: {get_delay_for_inout(WAVE_INPUT_FILENAME, WAVE_OUTPUT_FILENAME)}"
    )
