FROM python:3.10

WORKDIR TfModelTraining

RUN pip install tensorflow
RUN pip install tensorflow_hub

ENTRYPOINT ["tail", "-f", "/dev/null"]