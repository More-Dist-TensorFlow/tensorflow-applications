FROM registry.cn-hangzhou.aliyuncs.com/denverdino/tensorflow:latest

RUN mkdir -p /tf/audio
ADD audio-classification /tf/audio
COPY ./tfconfig_wrapper.py /tf/audio/distributed/
ENTRYPOINT ["python3","/tf/audio/distributed/tfconfig_wrapper.py"]
