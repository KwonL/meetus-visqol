import argparse
import logging
import os
import wave
from threading import Thread, Semaphore

import pyaudio
from flask import Flask

from delay import get_delay_for_inout
from visqol import run_visqol

app = Flask(__name__)
CHUNK = 1024
FORMAT = pyaudio.paInt16
RATE = 48000
RECORD_SECONDS = 10
os.putenv("WAVE_INPUT_FILENAME", "input.wav")
os.putenv("IN_DEVICE_NAME", "")
os.putenv("OUT_DEVICE_NAME", "")
WAVE_OUTPUT_FILENAME = "output.wav"
semaphore = Semaphore(0)
logging.basicConfig(
    filename="logs/meetus-audio-testing.log",
    format="%(asctime)s %(levelname)s [%(name)s] [%(filename)s:%(lineno)d] - %(message)s",
    level=logging.DEBUG,
)
logger = logging.getLogger(__name__)


def stream_file_to_dev(pyaud: pyaudio.PyAudio, dev: dict):
    input_file = wave.open(os.getenv("WAVE_INPUT_FILENAME", "input.wav"), "rb")
    output_stream = pyaud.open(
        format=pyaudio.get_format_from_width(input_file.getsampwidth()),
        channels=input_file.getnchannels(),
        output_device_index=dev.get("index"),
        rate=int(dev.get("defaultSampleRate")),
        output=True,
    )
    input_file.close()
    file = open(os.getenv("WAVE_INPUT_FILENAME", "input.wav"), "rb")
    semaphore.release()
    output_stream.write(file.read())
    file.close()


def record_testing():
    pyaud = pyaudio.PyAudio()

    global RECORD_SECONDS
    global RATE
    with wave.open(os.getenv("WAVE_INPUT_FILENAME", "input.wav"), "rb") as f:
        RECORD_SECONDS = f.getnframes() / float(f.getframerate()) + 1
        RATE = f.getframerate()
    logger.info(f"duration is {RECORD_SECONDS}")

    # Find device
    in_dev = dict()
    out_dev = dict()
    for i in range(pyaud.get_device_count()):
        dev = pyaud.get_device_info_by_index(i)
        if (
            os.getenv("IN_DEVICE_NAME") in dev.get("name")
            and dev["maxInputChannels"] > 0
        ):
            in_dev = dev
        elif (
            os.getenv("OUT_DEVICE_NAME") in dev.get("name")
            and dev["maxOutputChannels"] > 0
        ):
            out_dev = dev

    input_stream = pyaud.open(
        format=FORMAT,
        channels=in_dev.get("maxInputChannels"),
        input_device_index=in_dev.get("index"),
        rate=int(in_dev.get("defaultSampleRate")),
        input=True,
        frames_per_buffer=CHUNK,
    )
    streaming_thread = Thread(target=stream_file_to_dev, args=(pyaud, out_dev))
    streaming_thread.start()

    logger.info("* start recording")
    semaphore.acquire()
    frames = []
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = input_stream.read(CHUNK)
        frames.append(data)
    logger.info("* done recording")

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
    parser.add_argument(
        "--input-file", "-i", type=str, help="테스트용 입력 파일", default="input.wav"
    )
    parser.add_argument(
        "--input-device",
        "-r",
        type=str,
        help="PC의 마이크 포트로 오디오를 입력받을 디바이스 이름의 일부",
        default="마이크",
    )
    parser.add_argument(
        "--output-device",
        "-p",
        type=str,
        help="PC의 스피커 포트 오디오를 출력할 디바이스 이름의 일부",
        default="스피커",
    )
    parser.add_argument("--serve-mode", "-s", action="store_true", help="서버 모드로 실행")
    args = parser.parse_args()

    os.environ["WAVE_INPUT_FILENAME"] = args.input_file
    os.environ["IN_DEVICE_NAME"] = args.input_device
    os.environ["OUT_DEVICE_NAME"] = args.output_device

    if args.serve_mode:
        from route import main_bp

        app.register_blueprint(main_bp)
        app.run(debug=True, port=5000, host="0.0.0.0")
    else:
        record_testing()
        run_visqol(os.getenv("WAVE_INPUT_FILENAME", "input.wav"), WAVE_OUTPUT_FILENAME)
        logger.info("=============================================")
        logger.info(
            "delay for this audio is: "
            f"{get_delay_for_inout(os.getenv('WAVE_INPUT_FILENAME', 'input.wav'), WAVE_OUTPUT_FILENAME)}"
        )
