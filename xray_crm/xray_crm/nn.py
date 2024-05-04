import pandas as pd
import tensorflow as tf
from keras import layers, models
import matplotlib.pyplot as plt
import os
from PIL import ImageFile, Image

ImageFile.LOAD_TRUNCATED_IMAGES = True


def check_images(directory, extensions=['.jpg', '.jpeg', '.png']):
    broken_images = []
    for filename in os.listdir(directory):
        if any(filename.lower().endswith(ext) for ext in extensions):
            try:
                img = Image.open(os.path.join(directory, filename))  # Open the image file
                img.verify()  # Verify that it is, in fact, an image
            except (IOError, SyntaxError) as e:
                print('Bad file:', filename)  # Print out the names of corrupt files
                broken_images.append(filename)
    return broken_images


# Replace '/path/to/images' with the path to your directory containing the images
broken_images = check_images('xray_crm/images')
print("Broken images:", broken_images)

# Load the dataset
data_path = 'xray_crm/dataset.csv'  # Update with the correct path to your CSV file
data = pd.read_csv(data_path)

# Convert 'fractured' column to string to satisfy Keras requirements
data['fractured'] = data['fractured'].astype(str)

# Path to your image directory
image_directory = 'xray_crm/images'  # Update this with the actual path to your images

# Initialize the ImageDataGenerator for grayscale images
datagen = tf.keras.preprocessing.image.ImageDataGenerator(
    rescale=1. / 255,
    validation_split=0.2
)
# Create generators for training and validation
train_generator = datagen.flow_from_dataframe(
    dataframe=data,
    directory=image_directory,
    x_col='image_id',
    y_col='fractured',
    target_size=(150, 150),
    batch_size=32,
    class_mode='binary',
    color_mode='grayscale',
    subset='training')

validation_generator = datagen.flow_from_dataframe(
    dataframe=data,
    directory=image_directory,
    x_col='image_id',
    y_col='fractured',
    target_size=(150, 150),
    batch_size=32,
    class_mode='binary',
    color_mode='grayscale',
    subset='validation')

# Build the CNN model for grayscale image input
model = models.Sequential([
    layers.Conv2D(32, (3, 3), activation='relu', input_shape=(150, 150, 1)),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(128, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Flatten(),
    layers.Dense(512, activation='relu'),
    layers.Dense(1, activation='sigmoid')
])

model.compile(optimizer='adam',
              loss='binary_crossentropy',
              metrics=['accuracy'])

# Train the model
history = model.fit(
    train_generator,
    steps_per_epoch=train_generator.n // train_generator.batch_size,
    epochs=10,  # Adjust number of epochs based on your needs
    validation_data=validation_generator,
    validation_steps=validation_generator.n // validation_generator.batch_size)

model.save('xray_crm/xray.h5')

# # Plot training and validation accuracy
# plt.plot(history.history['accuracy'], label='Training Accuracy')
# plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
# plt.title('Model Accuracy')
# plt.xlabel('Epoch')
# plt.ylabel('Accuracy')
# plt.legend()
# plt.show()
#
# # Evaluate on the validation set
# val_loss, val_acc = model.evaluate(validation_generator)
# print(f"Validation Accuracy: {val_acc}")


