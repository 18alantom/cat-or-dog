import sys
import time
import cv2
import numpy as np

from pathlib import Path
from io import BytesIO, StringIO
from base64 import b64decode

import torch
from .model import inference
from .what_is_it import what_is_it

MEAN = np.array([0.48826352, 0.45509255, 0.4174077]).reshape(3, 1, 1)
STD = np.array([0.22981022, 0.22478424, 0.22537524]).reshape(3, 1, 1)


def normalize(image):
    image = (image - MEAN) / STD
    return image


def to_tensor(image):
    image = image.transpose(2, 0, 1)/255
    image = np.float32(normalize(image))
    image = torch.from_numpy(image)
    return image


def fprint(*args, **kwargs):
    print(*args, **kwargs)
    sys.stdout.flush()


def response_to_image(data):
    data_uri = str(data).split(",")[1]
    decoded = b64decode(data_uri)
    buffer = np.fromstring(decoded, dtype=np.uint8)
    return cv2.imdecode(buffer, cv2.IMREAD_COLOR)[:, :, ::-1].copy()


def grad_times(t):
    t = t*1000
    return f"{t:0.3f} ms".rjust(10)


def classify(data):
    image = response_to_image(data)
    tensor = to_tensor(image)

    t1 = time.time()
    probabilites = inference(tensor)
    t2 = time.time()
    print(f"infr time: {grad_times(t2-t1)} | ", end="")
    response = what_is_it(*probabilites.numpy().squeeze())
    fprint(f"resp: {response} ")
    return response


# Loads the network when flask runs
# else lazy loading?
_ = inference(torch.rand(3, 224, 224))
fprint("model loaded ")
