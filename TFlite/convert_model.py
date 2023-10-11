import tensorflow as tf

with open('model.tflite', 'wb') as file:
    file.write(
        tf.lite.TFLiteConverter.from_saved_model("./models/sound_analyzer_v1").convert())