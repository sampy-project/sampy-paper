import numpy as np
from scipy.ndimage import gaussian_filter
import matplotlib.pyplot as plt
import glob
import os

# parameters
path_output = "C:/post_doc/data/data_paper_sampy/k_maps_arrays"

# k uniform of 10.
map_10 = np.full((100, 100), 10.)

# 55 rows on top at k=50, bottom at 5.
map_halves = np.full((100, 100), 10.)
for i in range(100):
    for j in range(100):
        if i >= 45:
            map_halves[i, j] = 50.


# random noise map
map_gauss = np.random.uniform(0., 1., (100, 100))
map_gauss = gaussian_filter(map_gauss, 10.)
map_gauss = (map_gauss - map_gauss.min())
map_gauss = 20. * map_gauss / map_gauss.max()


plt.imshow(map_gauss, vmin=0., vmax=20.)
plt.show()

# for path in glob.glob(path_output + '/*'):
#     os.remove(path)

# np.save(path_output + '/map_k10.npy', map_10)
np.save(path_output + '/map_halves.npy', map_halves)
# np.save(path_output + '/map_noise.npy', map_gauss)
