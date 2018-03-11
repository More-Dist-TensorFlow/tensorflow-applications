FROM registry.cn-hangzhou.aliyuncs.com/denverdino/tensorflow:latest

RUN apt update && apt install python-pip && echo y | pip install paho-mqtt

RUN mkdir -p /tf/scale
ADD scale /tf/scale
COPY ./tfconfig_wrapper.py /tf/scale/distributed/
#ENTRYPOINT ["python3","/tf/scale/distributed/tfconfig_wrapper.py"]
