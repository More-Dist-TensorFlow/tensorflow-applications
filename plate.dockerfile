FROM registry.cn-hangzhou.aliyuncs.com/denverdino/tensorflow:latest

RUN apt update && apt -y install python-opencv

RUN mkdir -p /tf/plate
ADD plate /tf/plate
COPY ./tfconfig_wrapper.py /tf/plate/distributed/
#ENTRYPOINT ["python3","/tf/plate/distributed/tfconfig_wrapper.py"]
