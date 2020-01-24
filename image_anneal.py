#!/usr/bin/env python3
'''Image annealer combines two images by using the pixels (colors) of one image,
    and arranging them so that they closely match the pixels in a second image.'''
import numpy as np
from skimage import io
import matplotlib.pyplot as plt
import cv2

def keep_trade(old_cost, new_cost, temperature=1):
    '''
    Simulated annealing decision rule for whether to keep
    a pixel swap.
    '''
    return np.exp(-(new_cost - old_cost) / temperature) >= np.random.random()

def random_pixel(shape):
    '''
    Selects a random pixel.
    '''
    return (np.random.randint(0, shape[0]), np.random.randint(0, shape[1]))

def mean_squared_error(x_1, x_2):
    '''
    Mean squared error of two input arrays.
    '''
    return np.sum((x_1 - x_2)**2)

if __name__ == '__main__':
    # Setup argument PARSER
    import argparse
    DESC = '''Image annealer combines two images by using the pixels (colors) of one image,
            and arranging them so that they closely match the pixels in a second image.'''
    PARSER = argparse.ArgumentParser(description=DESC)
    PARSER.add_argument('--color_img', dest='COLOR_IMG', type=str, help='Image that provides colour.', required=True)
    PARSER.add_argument('--struct_img', dest='STRUCT_IMG', type=str, help='Image that provides structure.', required=True)
    PARSER.add_argument('--iter', dest='ITERS', type=int, help='Iterations.', default=100000, required=False)
    PARSER.add_argument('--out', dest='OUT', type=str, help='Output path.', required=True)
    PARSER.add_argument('--height', dest='HEIGHT', type=int, help='Height of the output image.', required=False)
    ARGS = PARSER.parse_args()

    # Load and preprocess images
    COLOR_IMG = io.imread(ARGS.COLOR_IMG)
    COLOR_IMG = COLOR_IMG / 255.0
    
    STRUCT_IMG = io.imread(ARGS.STRUCT_IMG)
    STRUCT_IMG = STRUCT_IMG / 255.0

    if ARGS.HEIGHT:
        ASPECT_RATIO = COLOR_IMG.shape[0] / COLOR_IMG.shape[1]
        NEW_WIDTH = int(ASPECT_RATIO * ARGS.HEIGHT)
        COLOR_IMG = cv2.resize(COLOR_IMG, (NEW_WIDTH, ARGS.HEIGHT))
        STRUCT_IMG = cv2.resize(STRUCT_IMG, (NEW_WIDTH, ARGS.HEIGHT))

    # Iterate
    for i in range(ARGS.ITERS):
        row1, col1 = random_pixel(COLOR_IMG.shape)
        row2, col2 = random_pixel(STRUCT_IMG.shape)
        old_cost = mean_squared_error(COLOR_IMG[row1, col1], STRUCT_IMG[row1, col1]) +\
                   mean_squared_error(COLOR_IMG[row2, col2], STRUCT_IMG[row2, col2])
        new_cost = mean_squared_error(COLOR_IMG[row1, col1], STRUCT_IMG[row2, col2]) +\
                   mean_squared_error(COLOR_IMG[row2, col2], STRUCT_IMG[row1, col1])

        if keep_trade(old_cost, new_cost, 1/(i+1)):
            COLOR_IMG[row1, col1], COLOR_IMG[row2, col2] = COLOR_IMG[row2, col2], COLOR_IMG[row1, col1]

    # Save resulting image
    plt.imsave(f'{ARGS.OUT}', COLOR_IMG)
