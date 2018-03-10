FROM registry.cn-hangzhou.aliyuncs.com/denverdino/tensorflow:latest

RUN mkdir -p /tf/yolo
ADD yolo /tf/yolo
COPY ./tfconfig_wrapper.py /tf/yolo/distributed/
ENTRYPOINT ["python3","/tf/yolo/distributed/tfconfig_wrapper.py"]
