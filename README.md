# Simulated Annealing Between Images
![alt text](https://github.com/galenseilis/image_anneal/blob/master/simulated_annealing.jpg "Logo Title Text 1")

Provides a command line interface to use simulated annealing between two images, one providing color and the other providing structure. What this program does is rearrange (but otherwise does not change) the pixels in one image to best match a second image.

## Usage
The *Original Image* in the example above would have been passed as ```--color_img```, the *Template Image* passed as ```struct_img```, and *Simulated Annealing Image* would have been the resulting image whose yet-to-exist filename would have been passed to ```--out```.
```
$ python3 image_anneal.py --color_img /path/to/color_img.jpg --struct_img /path/to/struc_image.jpg --out test.png --height 100
```
