MODEL_NAME="sound_analyzer_v1"
CLASSES_FILE_NAME="${MODEL_NAME}_classes.csv"

# Train model if not exits
if ! [ -e "./TFlite/output/${MODEL_NAME}.tflite" ]; then
    echo "Training model"
    mkdir -p ./TFlite/output
    bash train_model.sh $MODEL_NAME
else
    echo "Model already exists"
fi

cp "./TFlite/output/${MODEL_NAME}.tflite" "./OrangePi/SoundAnalyzer/models/${MODEL_NAME}.tflite"
cp "./TFlite/output/$CLASSES_FILE_NAME" "./OrangePi/SoundAnalyzer/models/$CLASSES_FILE_NAME"

# TODO: ssh, Mount orange pi