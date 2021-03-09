# Audio quality testing tool
VISQOL, PESQ 등을 이용한 통화 서비스의 오디오 품질 측정을 위한 툴입니다.

## Dependencies
다음 command를 통해 python dependency 추가

```shell
# Before install dependencies, enable virtual environment
pip install -r reqruiements.txt
```

추후에 Docker로 migration할 예정, 현재는 audio device를 연결해서 사용해야 하기 때문에 Docker가 큰 의미가 없

## Usage

```shell
python main.py \
  -i [sample file] \
  -r [오디오를 입력받을 포트 디바이스의 일부] \
  -p [샘플 오디오를 재생할 포트 디바이스의 일부]
```

현재 연결된 audio device 목록을 출력하기 위해서는 다음 command 실행

```shell
python print_audio_device.py
```

```
# Example output

{'defaultHighInputLatency': 0.053875,
 'defaultHighOutputLatency': 0.1,
 'defaultLowInputLatency': 0.04454166666666667,
 'defaultLowOutputLatency': 0.01,
 'defaultSampleRate': 48000.0,
 'hostApi': 0,
 'index': 2,
 'maxInputChannels': 1,
 'maxOutputChannels': 0,
 'name': 'MacBook Pro 마이크',
 'structVersion': 2}
{'defaultHighInputLatency': 0.1,
 'defaultHighOutputLatency': 0.018395833333333333,
 'defaultLowInputLatency': 0.01,
 'defaultLowOutputLatency': 0.0090625,
 'defaultSampleRate': 48000.0,
 'hostApi': 0,
 'index': 3,
 'maxInputChannels': 0,
 'maxOutputChannels': 2,
 'name': 'MacBook Pro 스피커',
 'structVersion': 2}
```

원하는 device의 name을 argument로 입력
