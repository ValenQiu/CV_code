# Thermal Camera

## Flirpy
Check the `Flirpy` library for details: https://github.com/LJMUAstroecology/flirpy

#### Grab image
The following program will grab the raw data from the camera, 
```Python
from flirpy.camera.lepton import Lepton

camera = Lepton()
image = camera.grab()
image = image.astype(int)
print(camera.frame_count)
print(camera.frame_mean)
print(camera.ffc_temp_k)
print(camera.fpa_temp_k)
camera.close()
```
> the relationship between N (one of the raw data in image) and temperature:
>   Kelvin temperature = N/100，
>   Celsius = N/100 - 273

#### Show the image
First convery the raw into 8-bit array, and then show the image by `OpenCV`
```Python
# need to use the raw data "image" grabed from camera
img = np.asarray(image)
img = 255 * (img - img.min()) / (img.max - img.min())
# apply colormap
img_col = cv2.applyColorMap(img.astype(np.uint8), cv2.COLORMAP_INFERNO)
# show image
cv2.namedWindow("Thermal", 0)
cv2.resizeWindow("Thermal", 300, 300)
cv2.imshow("Thermal", img_col)
```

#### Center axis 骨架提取
About how to get the center axis of image, check the `morphology` module in the library `skimage`: https://blog.csdn.net/qq_36756866/article/details/115485629
See the pip webpage for installing: https://pypi.org/project/scikit-image/


