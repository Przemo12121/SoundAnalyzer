MODEL_NAME="$1"

if ! [ -e "./output/$1" ]; then
    echo "Training model"
    bash train_model.sh $1
else
    echo "Model already exists"
fi