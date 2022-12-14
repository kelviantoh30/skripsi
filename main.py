from flask import Flask, render_template, request, jsonify
from tensorflow.keras.models import load_model
import numpy as np
from tensorflow.keras.preprocessing.image import load_img
from tensorflow.keras.applications.vgg19 import preprocess_input
import os
from tensorflow.keras.preprocessing import image
import random


app = Flask(__name__)

# model = load_model('Model_Anggrek_VGG19.h5')


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
            filename = file.filename
            THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
            print(THIS_FOLDER)
            file_path = os.path.join(THIS_FOLDER, 'static/images')
            print(file_path)
            file_path = os.path.join(file_path, filename)
            file.save(file_path)

            # img = read_image(file_path)
            # class_prediction = model.predict(img)
            # classes_x = np.argmax(class_prediction, axis=1)

            # delete file to save storage
            os.remove(file_path)

            classes_x = random.randint(0, 4)
            genus = "Not found"
            treatment = "Lorem ipsum"
            link1, link2, link3 = "", "", ""

            treatments = [
                "Media Tanam: Arang Kayu atau Pakis\nIntensitas Cahaya:  20 - 30%\nSuhu: 13 - 16°C (suhu malam) 20 - 24°C (suhu siang)\nPenyiraman: ",
                "Media Tanam: Arang Kayu atau Sabut Kelapa\nIntensitas Cahaya:  55 - 65%\nSuhu: 15 - 16°C (suhu malam) 26 - 27°C (suhu siang)\nPenyiraman: ",
                "Media Tanam: Pakis atau Pecahan Batu Bata\nIntensitas Cahaya:  55 - 65%\nSuhu: 15 - 18°C (suhu malam) 27°C (suhu siang)\nPenyiraman: ",
                "Media Tanam: Moss\nIntensitas Cahaya:  10 - 30%\nSuhu: 19°C (suhu malam) 27°C (suhu siang)\nPenyiraman: ",
                "Media Tanam: Sekam\nIntensitas Cahaya:  100%\nSuhu: 21°C (suhu malam) 28°C (suhu siang)\nPenyiraman: "]

            if classes_x == 0:
                genus = "Cattelya"
                link1 = "https://cdn.pixabay.com/photo/2017/11/03/08/54/orchid-2913755__480.jpg"
                link2 = "https://media.istockphoto.com/id/639004662/id/foto/anggrek-milik-genus-cattleya.jpg?b=1&s=170667a&w=0&k=20&c=vgKOyFogvC29psB9RkkguaVWGaqKg_l-XBhn6J8s4Qc="
                link3 = "https://cdn.pixabay.com/photo/2018/04/01/17/46/flower-3281568__480.jpg"
                treatment = treatments[0]
            elif classes_x == 1:
                genus = "Dendrobium"
                link1 = "https://cdn.pixabay.com/photo/2022/10/31/22/37/dendrobium-7560863__480.jpg"
                link2 = "https://cdn.pixabay.com/photo/2021/08/21/13/35/dendrobium-6562799__480.jpg"
                link3 = "https://cdn.pixabay.com/photo/2022/09/15/15/10/flower-7456633__480.jpg"
                treatment = treatments[1]
            elif classes_x == 2:
                genus = "Oncidium"
                link1 = "https://cdn.pixabay.com/photo/2021/12/26/05/23/flower-6894253__480.jpg"
                link2 = "https://cdn.pixabay.com/photo/2019/11/05/17/09/orchid-4603975__480.jpg"
                link3 = "https://thumbs.dreamstime.com/b/purple-green-maroon-oncidium-orchid-bloom-greenhouse-87482282.jpg"
                treatment = treatments[2]
            elif classes_x == 3:
                genus = "Phalaenopsis"
                link1 = "https://cdn.pixabay.com/photo/2020/02/24/13/26/orchid-4876192__480.jpg"
                link2 = "https://cdn.pixabay.com/photo/2013/05/05/09/36/orchid-108914__480.jpg"
                link3 = "https://cdn.pixabay.com/photo/2018/05/29/05/54/orchid-3437984__480.jpg"
                treatment = treatments[3]
            elif classes_x == 4:
                genus = "Vanda"
                link1 = "https://cdn.pixabay.com/photo/2012/07/27/13/27/blue-vanda-orchid-53084__480.jpg"
                link2 = "https://cdn.pixabay.com/photo/2021/12/26/05/25/flower-6894255__480.jpg"
                link3 = "https://cdn.pixabay.com/photo/2018/12/15/06/42/orchid-3876403__480.jpg"
                treatment = treatments[4]
            else:
                genus = "Server Error"
                treatment = "Please contact administrator for more info."

            if classes_x >= 0 and classes_x <= 4:
                treatment += " Disiram 2x perhari yaitu yaitu pagi hari ( 06.00- 08.00 ) dansore hari ( 16.00 - 18.00 ). Penyiraman terbaik dengan. cara spray, ditujukan ke media, batang dan daun. Hindari menyiram bunga karena akan menyebabkan cepat rontok."

            plant = {
                "genus": genus,
                "treatment": treatment,
                "link1": link1,
                "link2": link2,
                "link3": link3
            }

            return jsonify(
                plant=plant,
                error=False,
                message="success"
            )
        else:
            return jsonify(
                error=True,
                message="Unable to read the file or no file uploaded"
            )


if __name__ == '__main__':
    app.run(debug=True, use_reloader=False, port=5580)
