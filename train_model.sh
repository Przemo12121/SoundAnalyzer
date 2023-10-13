MODEL_NAME=$1
CONAINER_NAME="tf_model_training"

# create container if not exits
if ! [ "$(docker ps -a | grep $CONAINER_NAME)" ]; then
    # build image if not exists
    if ! [ "$(docker images | grep $CONAINER_NAME)" ]; then
        docker build -t $CONAINER_NAME --build-arg MODEL_NAME=$MODEL_NAME .
    fi

    # run container
    docker run -d --name $CONAINER_NAME -v ./TFlite:/TfModelTraining $CONAINER_NAME
else
    # start container
    docker start $CONAINER_NAME
fi

# attach for output
docker attach $CONAINER_NAME