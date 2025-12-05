# %%
import os
import pathlib

import h5py
import matplotlib.pyplot as plt
import numpy as np
import torch

from models import UNet
# from models2 import AttentionUNet

# from models_ import AttentionUNet, UNet
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


# DEVICE = "cuda"
DEVICE = "cpu"

# Load params.json
param_path = pathlib.Path(os.getcwd()) / "params.json"

params = Params(param_path)

# Load Contour model
# model_path = os.path.join(
#     os.getcwd(),
#     "assets/logs/20250325-122319Contour/saved_models/highest_val.pt",
# )
model_path = "D:\\Mosamatic\\PyTorchModelFiles\\leroyvolmer\\T4_VAT_and_remote_VAT_script\\T4\\contour_model-1.0.pt"

model_c = UNet(params, 2).to(device=DEVICE)
model_c.load_state_dict(torch.load(model_path, weights_only=False, map_location=torch.device(DEVICE)))
model_c.eval()

# Data path
# test_path = os.path.join(
#     os.getcwd(),
#     "assets/data/T4-val/KU_Leuven.h5",
# )
test_path = "D:\\Mosamatic\\T4\\Test\\h5\\KU_Leuven.h5"

# Load data
with h5py.File(test_path, "r") as f:
    a_group_key2 = list(f.keys())
    pad_width = 0
    images = np.zeros(
        [len(a_group_key2), 512 + pad_width, 512 + pad_width], dtype=np.float32
    )
    labels = np.zeros(
        [len(a_group_key2), 512 + pad_width, 512 + pad_width], dtype=np.int16
    )

    # List to store keys of skipped patients
    skipped_keys = []
    for i, name in enumerate(a_group_key2):
        if i % 500 == 0:
            print(f"Loading patients: {i} out of {len(a_group_key2)}")
        image = f[str(name)]["images"][()]
        label = f[str(name)]["labels"][()]

        image = normalize(
            image,
            lower_bound=params.dict["lower_bound"],
            upper_bound=params.dict["upper_bound"],
        )
        label[label == 5] = 2
        label[label == 7] = 3
        label[label > 3] = 0
        images[i, :, :] = image
        labels[i, :, :] = np.uint8(label)

    print(">>> Unique labels in {}: {}".format(test_path, np.unique(labels)))

# Take example patient
layer = 0
image = images[layer, :, :]
label = labels[layer, :, :]

# Predict contour
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
# del model_c

# Load body composition model
# model_path = os.path.join(
#     os.getcwd(),
#     "assets/logs/20250422-102951_lungVAT-lung1-lung3/saved_models/highest_val.pt",
# )
model_path = "D:\\Mosamatic\\PyTorchModelFiles\\leroyvolmer\\T4_VAT_and_remote_VAT_script\\T4\\model-1.0.pt"
model = UNet(params, 4).to(device=DEVICE)
model.load_state_dict(torch.load(model_path, weights_only=False, map_location=torch.device(DEVICE)))
model.eval()

# Predict body composition
with torch.no_grad():
    input = np.expand_dims(image, 0)
    input = np.expand_dims(input, 0)
    input = torch.Tensor(input)

    input = input.to(DEVICE, dtype=torch.float)

    prediction = model(input)
    prediction = torch.argmax(prediction, axis=1)
    prediction = prediction.squeeze()
    prediction = prediction.detach().cpu().numpy()

# # Remove VAT prediction by setting label 2 to 0.
# prediction_no_vat = np.copy(prediction)
# prediction_no_vat[prediction_no_vat == 2] = 0

# Plt example
fig, ax = plt.subplots(1, 4, figsize=(20, 20))
ax[0].imshow(image, cmap="gray")
ax[1].imshow(label)
ax[1].title.set_text("Label")
ax[2].imshow(prediction)
ax[2].title.set_text("Prediction")
# ax[3].imshow(prediction_no_vat)
# ax[3].title.set_text("Prediction VAT removed")

plt.show()

# %%
