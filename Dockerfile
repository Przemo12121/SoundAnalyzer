FROM python:3.10

ARG MODEL_NAME
ENV MODEL_NAME MODEL_NAME

WORKDIR TfModelTraining

RUN pip install tensorflow
RUN pip install tensorflow_hub
RUN pip install scikit-learn
# RUN pip install sklearn

ENTRYPOINT ["tail", "-f", "/dev/null"]
# ENTRYPOINT ["python3", "train_model.py", MODEL_NAME]