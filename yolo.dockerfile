FROM registry.cn-hangzhou.aliyuncs.com/denverdino/tensorflow:latest

RUN mkdir -p /tf/yolo
ADD yolo /tf/yolo
ENTRYPOINT ["python","/tf/yolo/distributed/tfconfig_wrapper.py"]
