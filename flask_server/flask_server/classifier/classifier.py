import time
import cv2
import numpy as np

from pathlib import Path
from io import BytesIO, StringIO
from base64 import b64decode

from torchvision.transforms import Compose, ToTensor, Normalize
from .model import device, model

MEAN = np.array([0.48826352, 0.45509255, 0.4174077])
STD = np.array([0.22981022, 0.22478424, 0.22537524])

transforms = Compose([
    ToTensor(),
    Normalize(MEAN, STD)
])



def to_tensor(image):
    return transforms(image)


def response_to_image(data):
    data_uri = str(data).split(",")[1]
    decoded = b64decode(data_uri)
    buffer = np.fromstring(decoded, np.uint8)
    return cv2.imdecode(buffer, cv2.IMREAD_COLOR)[:, :, ::-1].copy()


def classify(data):
    image = response_to_image(data)
    tensor = to_tensor(image)
    print(tensor.shape)
    return 'okay'
