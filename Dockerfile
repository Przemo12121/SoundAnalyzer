FROM python:3.10

WORKDIR TfModelTraining

ARG MODEL_NAME
ENV MODEL_NAME ${MODEL_NAME} 

COPY TFlite .

RUN pip install tensorflow
RUN pip install tensorflow_hub
RUN pip install scikit-learn

ENTRYPOINT python3 train_model.py ${MODEL_NAME} 