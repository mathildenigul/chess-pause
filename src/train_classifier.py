import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.applications import MobileNetV2
from pathlib import  Path
import keras

DIRECTORY = Path("data")
MODEL_OUTP = Path("models/piece_classifier.keras")

def build_ds():
    train_ds = tf.keras.utils.image_dataset_from_directory(
        DIRECTORY / "train",
        image_size = (160, 160),
        batch_size = 32,
    )
    val_ds = tf.keras.utils.image_dataset_from_directory(
        DIRECTORY / "val",
        image_size = (160, 160),
        batch_size = 32,
    )
    class_names = train_ds.class_names
    print(f"Classes found: {class_names}")

    return train_ds, val_ds, class_names

def build_model(num_classes): #takes the number of classes
    #loading MobileNetV2 pretrained on ImageNet(without its original classifier)
    base_model = MobileNetV2(
        input_shape = (160, 160) + (3,),#3, for color channels
        include_top = False,
        weights = "imagenet",
    )
    base_model.trainable = False #freezing it on the pretrained base because retraining is not the focus of this project
    inputs = tf.keras.Input(shape = (160, 160) + (3,))
    x = tf.keras.applications.mobilenet_v2.preprocess_input(inputs)
    x = base_model(x, training = False) #need to actaully run the inputs through the frozen layer
    x = layers.GlobalAveragePooling2D()(x) #feature map needs to be turned into a flat vector per img
    x = layers.Dropout(0.2)(x)
    outputs = layers.Dense(num_classes, activation = "softmax")(x) #softmax cause best for iamge classification and specific to multi-class, single-label problems
    model = models.Model(inputs, outputs)

    model.compile(
        optimizer = "adam",
        loss = "sparse_categorical_crossentropy",
        metrics = ["accuracy"],
    )
    return model
    
def main():
    train_ds, val_ds, class_names = build_ds()
    model = build_model(num_classes = len(class_names))
    model.summary()

    training = model.fit(train_ds, validation_data = val_ds, epochs = 10)

    MODEL_OUTP.parent.mkdir(exist_ok = True)
    model.save(MODEL_OUTP)
    print(f"Model saved to {MODEL_OUTP}")
    final_val_acc = training.history["val_accuracy"][-1]
    print(f"Final validation accracy: {final_val_acc:.4f}")

if __name__ == "__main__":
    main()