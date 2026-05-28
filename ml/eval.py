import tensorflow as tf
import numpy as np
import config

model = tf.keras.models.load_model(config.MODEL_PATH)


def evaluate_image(IMAGE_DIR):

    ds = tf.keras.utils.image_dataset_from_directory(
        IMAGE_DIR,
        labels = None,
        image_size=(224, 224),
        batch_size=32,
        shuffle=False 
    )

    predictions = model.predict(ds)
    file_paths = ds.file_paths

    for path, prediction in zip(file_paths, predictions):
        predicted_class = np.argmax(prediction)
        confidence = np.max(prediction) * 100

        filename = path.split('/')[-1]

        print(f"Image: {filename} | Predicted Class: {config.CLASS_LABELS[predicted_class]} | Confidence: {confidence:.2f}%")


print(f"Classify images in {config.EVAL_IMAGE_DIR}")
evaluate_image(config.EVAL_IMAGE_DIR)

