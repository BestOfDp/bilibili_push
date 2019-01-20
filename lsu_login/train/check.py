import keras
import numpy as np
import string
from keras import backend as K

model_file_path = 'train/ok.h5'
model = keras.models.load_model(model_file_path)
CHRS = string.ascii_lowercase + string.digits
img_rows, img_cols = 12, 22
if K.image_data_format() == 'channels_first':
    input_shape = (1, img_rows, img_cols)
else:
    input_shape = (img_rows, img_cols, 1)


def handle_split_image(image):
    im = image.point(lambda i: i != 43, mode='1')
    y_min, y_max = 0, 22  # im.height - 1 # 26
    split_lines = [5, 17, 29, 41, 53]
    ims = [im.crop([u, y_min, v, y_max]) for u, v in zip(split_lines[:-1], split_lines[1:])]
    return ims


def predict_image(images):
    Y = []
    for i in range(4):
        im = images[i]
        test_input = np.array(im)
        test_input = test_input.reshape(1, *input_shape)
        y_probs = model.predict(test_input)
        y = CHRS[y_probs[0].argmax(-1)]
        Y.append(y)
    return ''.join(Y)


def check(image):
    veri_code = predict_image(handle_split_image(image))
    return veri_code
