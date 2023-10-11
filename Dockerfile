FROM python:3.10

WORKDIR TfModelTraining

RUN pip install tensorflow
RUN pip install tensorflow_hub
RUN pip install scikit-learn
RUN pip install sklearn

ENTRYPOINT ["tail", "-f", "/dev/null"]