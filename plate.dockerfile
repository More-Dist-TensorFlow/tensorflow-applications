FROM registry.cn-hangzhou.aliyuncs.com/denverdino/tensorflow:latest

RUN mkdir -p /tf/plate
ADD plate /tf/plate
ENTRYPOINT ["python","/tf/plate/distributed/tfconfig_wrapper.py"]
