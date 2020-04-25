import torch
from torch import nn

from pathlib import Path
from torchvision import models


def load_model():
    has_gpu = torch.cuda.is_available()
    device = torch.device("cuda" if has_gpu else "cpu")

    root = Path(".")
    weights = root/"flask_server/classifier/weights/resnet50_state_dict.pt"
    state_dict = torch.load(weights, device)

    model = models.resnet50()

    # Replace the last layer
    in_features = model.fc.in_features
    out_features = 2
    model.fc = nn.Sequential(
        nn.Linear(in_features, out_features),
        nn.Softmax(dim=1)
    )

    # TODO: Load state dict
    status = model.load_state_dict(state_dict)
    print(status)

    model = model.to(device)

    def inference(X):
        model.eval()
        X = X.to(device).reshape(1, *X.shape)
        with torch.no_grad():
            return model(X)
    return inference


inference = load_model()
