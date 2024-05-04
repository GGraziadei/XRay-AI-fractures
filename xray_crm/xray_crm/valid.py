import tensorflow as tf
import numpy as np
from core.models import ReportFile

def predict_image(image_path, model_path="xray_crm/xray.h5"):
    # Load the model
    model = tf.keras.models.load_model(model_path)

    img = tf.keras.utils.load_img(image_path, target_size=(150, 150), color_mode='grayscale')

    # Convert the image to an array and normalize it
    img_array = tf.keras.utils.img_to_array(img)
    img_array = img_array / 255.0  # Scale the image
    img_array = np.expand_dims(img_array, axis=0)  # Add a batch dimension

    # Predict the image
    prediction = model.predict(img_array)
    print("Raw prediction output:", prediction)

    # Assuming your model uses a sigmoid output layer for binary classification
    if prediction[0][0] > 0.35:
        return ReportFile.BROKEN
    else:
        return ReportFile.NOT_BROKEN
