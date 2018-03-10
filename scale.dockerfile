FROM registry.cn-hangzhou.aliyuncs.com/denverdino/tensorflow:latest

RUN mkdir -p /tf/scale
ADD scale /tf/scale
ENTRYPOINT ["python","/tf/scale/distributed/tfconfig_wrapper.py"]
