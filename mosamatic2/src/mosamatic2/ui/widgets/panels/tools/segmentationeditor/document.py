import numpy as np
from dataclasses import dataclass


@dataclass
class Document:    
    img: np.ndarray
    disp8: np.ndarray
    mask: np.ndarray
    meta: dict