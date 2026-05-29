import tensorflow as tf
import numpy as np
from tensorflow.keras.utils import load_img, img_to_array
from ml import config



def classify_single_image(image_path):
    print(f"Modelpath: {config.MODEL_PATH}")
    model = tf.keras.models.load_model(config.MODEL_PATH)
    img = load_img(image_path, target_size=(224, 224))
    img_array = img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)

    prediction = model.predict(img_array)[0]
    predicted_class = np.argmax(prediction)
    confidence = np.max(prediction) * 100

    print(f"Image: {image_path.split('/')[-1]} | Predicted Class: {config.CLASS_LABELS[predicted_class]} | Confidence: {confidence:.2f}%")
    label = config.CLASS_LABELS[predicted_class]
    label_conf = f"{label} mit  {confidence:.2f}%"
    # return config.CLASS_LABELS[predicted_class]
    return label_conf

def evaluate_image(IMAGE_DIR):

    print(f"Modelpath: {config.MODEL_PATH}")
    model = tf.keras.models.load_model(config.MODEL_PATH)
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


# print(f"Classify images in {config.EVAL_IMAGE_DIR}")
# evaluate_image(config.EVAL_IMAGE_DIR)

