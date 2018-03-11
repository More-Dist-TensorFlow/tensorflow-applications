FROM registry.cn-hangzhou.aliyuncs.com/denverdino/tensorflow:latest

RUN apt update && apt -y install python-pip && echo y | pip install librosa

RUN mkdir -p /tf/audio
ADD audio-classification /tf/audio
COPY ./tfconfig_wrapper.py /tf/audio/distributed/
#ENTRYPOINT ["python3","/tf/audio/distributed/tfconfig_wrapper.py"]
