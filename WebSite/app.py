from flask import Flask, render_template, request

import tensorflow as tf
import tensorflow_text

import os
from pathlib import Path


app = Flask(__name__)

path_model = {
    '0': 'RUS-OSS',
    '1': 'RUS-ENG-MINI',
}

list_model = {}

@app.before_first_request
def load_model():
    global list_model
    for index, type_model in path_model.items():
        list_model[index] = tf.saved_model.load(Path('static', 'model', type_model).__str__())


@app.route('/', methods=['POST', 'GET'])
def index():
    input_seq = ""
    output_seq = None
    if request.method == 'POST' and request.form['input_sequence']:
        output_seq = translation(request.form['input_sequence'], request.form['temp_model'])
        input_seq = request.form['input_sequence']
    return render_template('index.html', output_seq=output_seq, input_seq=input_seq, path_model=path_model)


def translation(input_sequence, model_type):
    input_text = tf.constant([input_sequence])
    result = list_model[model_type].tf_translate(input_text)

    return result['text'][0].numpy().decode().capitalize()


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
