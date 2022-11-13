from flask import Flask, render_template, request, jsonify
from tensorflow.keras.models import load_model
import numpy as np
from tensorflow.keras.preprocessing.image import load_img
from tensorflow.keras.applications.vgg19 import preprocess_input
import os
from tensorflow.keras.preprocessing import image
import random

app = Flask(__name__)


@app.route('/')
def index_view():
    return 'Hello, World!'


# Allow files with extension png, jpg and jpeg
ALLOWED_EXT = set(['jpg', 'jpeg', 'png'])


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXT

# Function to load and prepare the image in right shape


def read_image(filename):
    img = load_img(filename, target_size=(224, 224))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    return x


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        file = request.files.get('file', None)
        if file and allowed_file(file.filename):  # Checking file format
            # filename = file.filename
            # file_path = os.path.join('static/images', filename)
            # file.save(file_path)
            # img = read_image(file_path)  # prepressing method
            # class_prediction = model.predict(img)
            # classes_x = np.argmax(class_prediction, axis=1)
            classes_x = random.randint(0, 4)
            genus = "Not found"
            treatment = "Lorem ipsum"

            if classes_x == 0:
                genus = "Cattelya"
            elif classes_x == 1:
                genus = "Dendrobium"
            elif classes_x == 2:
                genus = "Oncidium"
            elif classes_x == 3:
                genus == "Phalaenopsis"
            elif classes_x == 4:
                genus = "Vanda"
            else:
                genus = "What is that"

            return jsonify(
                genus=genus,
                treatment=treatment
            )
        else:
            return jsonify(
                error="Unable to read the file or no file uploaded"
            )


if __name__ == '__main__':
    app.run(debug=True, use_reloader=False, port=5580)
