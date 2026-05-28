import tensorflow as tf
import numpy as np
import config
from tensorflow.keras.utils import load_img, img_to_array

model = tf.keras.models.load_model(config.MODEL_PATH)

def classify_single_image(image_path):
    img = load_img(image_path, target_size=(224, 224))
    img_array = img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)

    prediction = model.predict(img_array)[0]
    predicted_class = np.argmax(prediction)
    confidence = np.max(prediction) * 100

    print(f"Image: {image_path.split('/')[-1]} | Predicted Class: {config.CLASS_LABELS[predicted_class]} | Confidence: {confidence:.2f}%")
    return config.CLASS_LABELS[predicted_class]

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

