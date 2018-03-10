FROM registry.cn-hangzhou.aliyuncs.com/denverdino/tensorflow:latest
ARG appname=audio-classification

RUN mkdir -p /tf/$appname
COPY audio-data-extraction audio-min-samples distributed model-ckpt single /tf/$appname/
ENTRYPOINT ["python","/tf/$appname/distributed/tfconfig_wrapper.py"]
