from PIL import Image
import numpy as np

im = Image.open("map.png")
height = np.array(im)