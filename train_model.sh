MODEL_NAME = "$1"

docker build -t tf_model_training .

docker run -d --name tf_model_training -v ./TFlite:/TfModelTraining tf_model_training -e MODEL_NAME=$MODEL_NAME