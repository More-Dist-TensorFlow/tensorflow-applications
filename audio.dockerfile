FROM registry.cn-hangzhou.aliyuncs.com/denverdino/tensorflow:latest

RUN mkdir -p /tf/audio
ADD audio-classification /tf/audio
ENTRYPOINT ["python","/tf/audio/distributed/tfconfig_wrapper.py"]
