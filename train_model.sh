MODEL_NAME="$1"

# build image
docker build -t tf_model_training --build-arg MODEL_NAME=$1 .

# run container
docker run -d --name tf_model_training -v ./TFlite:/TfModelTraining tf_model_training