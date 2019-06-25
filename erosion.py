#
# 4/9/19
# ---------------------------------------- Erosion Simulation ----------------------------------------
"""
Simulating erosion on procedularly generated terrain.
"""
# To-do:
#   6/3/19 -- Need to speed up distance-weighted erosion, currently utilizes nested for loop
#   --> want to add gaussian blur to final image (scipy.ndimage.filters.gaussian_filter)
#
# ----------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------


# ---------------------------------------- IMPORTS ----------------------------------------

import noise
import numpy as np
import math
from mayavi import mlab
from itertools import product
from scipy import ndimage


# ---------------------------------------- PARAMETERS ----------------------------------------

# Noise parameters
grid = 2
res = 256 #ends up being (res-2), removing edge artifacts
oct = 4
lanc = 2
pers = .5
map_seed = 1

# Rain parameters
p_num_drops = 2000
p_move_cap = 100
p_drop_size = 1
p_drop_seed = 874923
p_initial_vel = [0, 0]
p_grav = 20

# Erosion parameters
k_momentum = .4
k_erosion_rate = .9
k_capacity = 10
k_deposition_rate =  .02
k_erode_radius = 4
k_min_slope_capacity = .01
k_water_cuttoff = .001

# Board parameters
colormap = 'YlGn'
z_scale = 5
board_scale = 10
offset = 0.05
blur = 1




# ---------------------------------------- LOADING MAP ----------------------------------------

# Noise map
noise_raw = noise.Octave(res, oct, lanc, pers, map_seed)
mapp = noise_raw[1:-2,1:-2] #removing edge artifacts

# Simulating generation
ermap = mapp

# Generating drops
np.random.seed(p_drop_seed)
drops = np.random.rand(p_num_drops, 2)




# ---------------------------------------- EROSION PROCESS ----------------------------------------

# Initializing drop
for drop in drops:
    uy, ux = np.gradient(ermap)
    pos_t = [(res - 3) * drop[0], (res - 3) * drop[1]] #updated to (res-3) due to rounding errors
    index_0 = tuple(np.rint(pos_t).astype(int))
    vel = np.array(p_initial_vel)
    speed = np.linalg.norm(vel)
    water_cap = p_drop_size
    carry_cap = 0
    sed_carry = 0

    # Drop sequence
    for t in range(p_move_cap):
        pos_0 = pos_t
        index_0 = tuple(np.rint(pos_t).astype(int))

        # Calculating movement
        grad = np.array([uy[index_0], ux[index_0]])
        vel = vel * k_momentum - grad * (1 - k_momentum)
        norm_vel = np.linalg.norm(vel)

        # Moving drop
        pos_t = pos_0 + vel / norm_vel
        index_t = tuple(np.rint(pos_t).astype(int))
        
        # Checking if drop exists
        if min(index_t) >= 0 and max(index_t) < (res - 2) and water_cap > k_water_cuttoff:

            # Determining erosion
            h1 = ermap[index_0]
            h2 = ermap[index_t]
            del_h = h2 - h1
            carry_cap = max(k_min_slope_capacity, -del_h) * speed * water_cap * k_capacity

            # Depositing sediment
            if sed_carry > carry_cap:
                deposit = (sed_carry - carry_cap) * k_deposition_rate
                sed_carry -= deposit
                ermap[index_0] += deposit
                speed = 0

            # Eroding sediment
            else:
                erode = min((carry_cap - sed_carry) * k_erosion_rate, -del_h)
                sed_carry += erode
                speed = math.sqrt(abs(speed ** 2 - del_h * p_grav))
                weight_norm = 4 * (math.pi * k_erode_radius ** 2) / 3

                # Radius weighted erosion
                for x, y in product(range(1, k_erode_radius + 1), range(1, k_erode_radius + 1)):
                    # Equivalent of nested for loop
                    if np.linalg.norm(np.array([x, y])) <= k_erode_radius:
                        print(np.linalg.norm(np.array([x, y])))
                        index_i = tuple([index_0[0] + x, index_0[1] + y])
                        index_j = tuple([index_0[0] - x, index_0[1] - y])
                        wi = k_erode_radius - abs(np.linalg.norm(np.array([index_i[0] - index_0[0], index_i[1] - index_0[1]])))
                        wj = k_erode_radius - abs(np.linalg.norm(np.array([index_j[0] - index_0[0], index_j[1] - index_0[1]])))
                        try:
                            ermap[index_i] -= wi * erode / weight_norm
                            ermap[index_j] -= wj * erode / weight_norm
                        except:
                            continue

            # Evaporating water
            water_cap -= p_drop_size / p_move_cap

        # Dead drops
        else:
            break

"""
Apply erosion radius normalization as volume of cone with fixed height 1 and variable radius R
V = 1/3 h * pi R^2
"""



# ---------------------------------------- PLOTTING MAP ----------------------------------------

# Blurring
ermap = ndimage.filters.gaussian_filter(ermap, blur)

# Mayavi surface (GEN 0)
e = mlab.surf(ermap, colormap = colormap, extent = [0, board_scale, 0, board_scale, 0, z_scale])
e.module_manager.scalar_lut_manager.reverse_lut = True
mlab.show()