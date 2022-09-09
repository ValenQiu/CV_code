# Thermal Camera

## Flirpy
Check the `Flirpy` library for details: https://github.com/LJMUAstroecology/flirpy

### Grab image
The following program will grab the raw data from the camera, 
··· python
from flirpy.camera.lepton import Lepton

camera = Lepton()
image = camera.grab()
image = image.astype(int)
print(camera.frame_count)
print(camera.frame_mean)
print(camera.ffc_temp_k)
print(camera.fpa_temp_k)
camera.close()
···

### Show the image
First convery the raw

#### Center axis 骨架提取
About how to get the center axis of image, check the `morphology` module in the library `skimage`: https://blog.csdn.net/qq_36756866/article/details/115485629
See the pip webpage for installing: https://pypi.org/project/scikit-image/


