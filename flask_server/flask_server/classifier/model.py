import torch

from pathlib import Path
from torchvision import models


def load_model():
    has_gpu = torch.cuda.is_available()
    device = torch.device("cuda" if has_gpu else "cpu")

    root = Path(".")
    weights = root/"flask_server/classifier/weights/resnet50_state_dict.pt"
    state_dict = torch.load(weights, device)

    model = models.resnet50()
    status = model.load_state_dict(state_dict)
    # print(status)
    return model, device


model, device = load_model()
