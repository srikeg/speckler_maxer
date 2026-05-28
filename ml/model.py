import numpy as np
import matplotlib.pyplot as plt
from IPython import embed
import tensorflow as tf
import keras
from tensorflow.keras import layers
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
import os
from datetime import datetime
import config

# timestamp = datetime.now().strftime("%m%d-%H%M%S")
# output_dir = f"output_data2/{timestamp}"
output_dir = "output"
os.makedirs(output_dir, exist_ok=True)
print(f"Saving outputs to: {output_dir}")


pretrained_model = keras.applications.ResNet50(
    include_top=False,
    weights="imagenet",
    input_tensor=None,
    input_shape=None,
    pooling=None,
    classes=4,
    classifier_activation="softmax",
    name="resnet50",
)

pretrained_model.trainable = False

inputs = keras.Input(shape=(224, 224, 3))

x = tf.keras.applications.resnet50.preprocess_input(inputs)
x = pretrained_model(x, training=False)
x = layers.GlobalAveragePooling2D()(x)
x = layers.Dropout(0.2)(x)
outputs = layers.Dense(4, activation='softmax')(x)
model = keras.Model(inputs, outputs)

model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

ds = tf.keras.utils.image_dataset_from_directory(
    config.TRAININGS_DATA_DIR,
    image_size=(224,224),
    batch_size=32,
    shuffle=True,
    seed=42
)


def plot_samples(ds):
    plt.figure(figsize=(10, 10))
    for images, labels in ds.take(1):
        for i in range(9):
            ax = plt.subplot(3, 3, i + 1)
            plt.imshow(images[i].numpy().astype("uint8"))
            plt.title(ds.class_names[labels[i]])
            plt.axis("off")
    plt.savefig(os.path.join(output_dir,"samples.png"))
    print("Plottig sampels done.")

def plot_confusion(ds,model):
    y_true = []
    y_pred = []
    for images, labels in test_ds:
        preds = model.predict(images)
        y_true.extend(labels.numpy())
        y_pred.extend(np.argmax(preds, axis=1))

    cm = confusion_matrix(y_true, y_pred)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=ds.class_names)
    # disp.plot(cmap=plt.cm.Blues)
    disp.plot()
    plt.title("Confusion Matrix")
    plt.savefig(os.path.join(output_dir,"confusion.png"))


def plot_misclassified_samples(test_ds, model, class_names, max_samples=9):

    misclassified_images = []
    misclassified_true = []
    misclassified_pred = []

    for images, labels in test_ds:
        preds = model.predict(images)
        pred_labels = np.argmax(preds, axis=1)
        for img, true, pred in zip(images, labels.numpy(), pred_labels):
            if true != pred:
                misclassified_images.append(img.numpy().astype("uint8"))
                misclassified_true.append(true)
                misclassified_pred.append(pred)
            if len(misclassified_images) >= max_samples:
                break
        if len(misclassified_images) >= max_samples:
            break

    plt.figure(figsize=(10, 10))
    for i in range(len(misclassified_images)):
        ax = plt.subplot(3, 3, i + 1)
        plt.imshow(misclassified_images[i])
        plt.title(f"True: {class_names[misclassified_true[i]]}\nPred: {class_names[misclassified_pred[i]]}")
        plt.axis("off")
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir,"misclassified_samples.png"))
    print("Plotted misclassified samples.")

def save_model(model, output_dir):
    model_path = os.path.join(output_dir, "model.keras")
    model.save(model_path)
    print(f"Model saved to {model_path}")

def plot_accuracy():

    plt.figure()
    plt.plot(history.history['loss'], label='Training Loss')
    plt.plot(history.history['val_loss'], label='Validation Loss')
    plt.title('Model Loss')
    plt.ylabel('Loss')
    plt.xlabel('Epoch')
    plt.legend(loc='upper right')
    plt.savefig(os.path.join(output_dir, "loss_curve.png"))


total_batches = len(ds)
train_size = int(0.7 * total_batches)
val_size = int(0.15 * total_batches)

train_ds = ds.take(train_size)
val_ds = ds.skip(train_size).take(val_size)
test_ds = ds.skip(train_size + val_size)

AUTOTUNE = tf.data.AUTOTUNE
train_ds = train_ds.cache().prefetch(buffer_size=AUTOTUNE)
val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)
test_ds = test_ds.cache().prefetch(buffer_size=AUTOTUNE)

EPOCHS = 30

print("\nStarting Training...")
history = model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=EPOCHS
)

print("\nEvaluating on Test Dataset:")
test_loss, test_acc = model.evaluate(test_ds)
print(f"Test Loss: {test_loss:.4f}")
print(f"Test Accuracy: {test_acc:.4f}")
print(model.summary())

save_model(model, output_dir)
plot_samples(ds)
plot_confusion(ds,model)
plot_misclassified_samples(test_ds, model, ds.class_names)
plot_accuracy()