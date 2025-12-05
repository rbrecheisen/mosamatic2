# %%
import os
import pathlib

import matplotlib.pyplot as plt
import numpy as np
import torch

from models import UNet
# from models2 import AttentionUNet
from param_loader import Params


def normalize(data: np.ndarray, lower_bound: int, upper_bound: int) -> np.ndarray:
    """Normalize input: 'data' between 'lower_bound' and 'upper_bound',
    and scale between [0, 1].

    Parameters
    ----------
    data : np.ndarray
        Input image
    lower_bound : int
        Minimum Hounsfield Unit
    upper_bound : int
        Maximum Hounsfield Unit

    Returns
    -------
    np.ndarray
        Normalized and scaled input
    """

    data = (data - lower_bound) / (upper_bound - lower_bound)
    data[data > 1] = 1
    data[data < 0] = 0
    return data


DEVICE = "cuda"

# Load params.json
param_path = pathlib.Path(os.getcwd()) / "params.json"

params = Params(param_path)

# Load Contour model
model_path = os.path.join(
    os.getcwd(),
    "assets/logs/20250325-122319contour/saved_models/highest_val.pt",
)

model_c = UNet(params, 2).to(device=DEVICE)
model_c.load_state_dict(torch.load(model_path, weights_only=False))
model_c.eval()

# Load example patient
patients = np.load(os.path.join(os.getcwd(), "img_foreign_object.npy"))
patients_labels = np.load(os.path.join(os.getcwd(), "labels_foreign_object.npy"))

image = patients[:, :, 6]
label = patients_labels[:, :, 6]

# Preprocess, normalization and bounds are now the same for contour and body composition
image = normalize(
    image,
    lower_bound=params.dict["lower_bound"],
    upper_bound=params.dict["upper_bound"],
)

# Create Contour mask
with torch.no_grad():
    # Create 4D Tensor input
    input = np.expand_dims(image, 0)
    input = np.expand_dims(input, 0)
    input = torch.Tensor(input)
    input = input.to(DEVICE, dtype=torch.float)

    # Predict
    prediction = model_c(input)
    prediction = torch.argmax(prediction, axis=1)
    prediction = prediction.squeeze()
    prediction = prediction.detach().cpu().numpy()

# Keep only torso
image *= prediction

# Remove contour model from memory if necessary
# del model

# Load body composition model
model_path = os.path.join(
    os.getcwd(),
    "assets/logs/20250401-144027-fixedMuscle/saved_models/highest_val.pt",
)
model = UNet(params, 4).to(device=DEVICE)
model.load_state_dict(torch.load(model_path, weights_only=False))
model.eval()

with torch.no_grad():
    input = np.expand_dims(image, 0)
    input = np.expand_dims(input, 0)
    input = torch.Tensor(input)

    input = input.to(DEVICE, dtype=torch.float)

    prediction = model(input)
    prediction = torch.argmax(prediction, axis=1)
    prediction = prediction.squeeze()
    prediction = prediction.detach().cpu().numpy()

plt.figure()
plt.imshow(image, cmap="gray")
plt.imshow(prediction, alpha=0.3)

plt.figure()
plt.imshow(label)
plt.title("Label")

plt.figure()
plt.imshow(prediction)
plt.title("Prediction")


# %%
