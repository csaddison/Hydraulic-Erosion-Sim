#
# 4/8/19
# ---------------------------------------- Terrain Generation: Noise ----------------------------------------
"""
Generating perlin and fractal noise.
"""
# Change Log:
#
# 4/9:
# Finished interpolation issues. want to add to class
# fixed grid x-y issues but still have resolution x-y issues
# temp fix is having grid, res only one number (square)
# Also added octave fractal noise
#
# 4/13:
# Vectorized all components, runs abou ~25x faster than before
#
# ----------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------


# ---------------------------------------- Imports ----------------------------------------

import math
import numpy as np
from itertools import product



# ----------------------------------------------------------------------------------------------------
# ---------------------------------------- Perlin Noise ----------------------------------------

def Perlin(grid, resolution, seed = 1, burn = .5):
    """
    Takes argument for grid node scale and overall resolution. Resolution has to be evenly divisible by grid.
    """
    # ---------------------------------------- Initializing variables ----------------------------------------
    # Bookeeping variables
    np.random.seed(seed)
    grid_size = (grid, grid)
    resolution = (resolution, resolution) 
    delta = resolution[0] // grid_size[0]

    # Cordinate grids
    nodes = (grid_size[0] + 1, grid_size[1] + 1)
    samples = (resolution[0] + 1, resolution[1] + 1)
    x_int = [i for i in range(nodes[0])]
    y_int = [i for i in range(nodes[1] - 1, -1, -1)]
    x = np.linspace(0, grid_size[0], samples[0])
    y = np.linspace(grid_size[1], 0, samples[1])
    # Want y = 0 at bottom of grid
    xx, yy = np.meshgrid(x, y)
    XX, YY = np.meshgrid(x_int, y_int)

    # Generating random gradients
    angs = 2 * math.pi * np.random.rand(nodes[0], nodes[1])


    # ---------------------------------------- Nodal Matricies ----------------------------------------
    # Calculates which grid node a pixel belongs to

    # Nodal matrix - X
    x_tl = XX[:-1, :-1].repeat(delta, 0).repeat(delta, 1)
    row = x_tl[resolution[0] - 1]
    x_tl = np.insert(x_tl, resolution[0], row, axis = 0)
    col = x_tl[:, resolution[1] - 1]
    x_tl = np.insert(x_tl, resolution[1], col, axis = 1)

    x_tr = XX[:-1, 1:].repeat(delta, 0).repeat(delta, 1)
    row = x_tr[resolution[0] - 1]
    x_tr = np.insert(x_tr, resolution[0], row, axis = 0)
    col = x_tr[:, 0]
    x_tr = np.insert(x_tr, 0, col, axis = 1)

    x_bl = XX[1:, :-1].repeat(delta, 0).repeat(delta, 1)
    row = x_bl[0]
    x_bl = np.insert(x_bl, 0, row, axis = 0)
    col = x_bl[:, resolution[1] - 1]
    x_bl = np.insert(x_bl, resolution[1], col, axis = 1)

    x_br = XX[1:, 1:].repeat(delta, 0).repeat(delta, 1)
    row = x_br[0]
    x_br = np.insert(x_br, 0, row, axis = 0)
    col = x_br[:, 0]
    x_br = np.insert(x_br, 0, col, axis = 1)


    # Nodal matrix - Y
    y_tl = YY[:-1, :-1].repeat(delta, 0).repeat(delta, 1)
    row = y_tl[resolution[0] - 1]
    y_tl = np.insert(y_tl, resolution[0], row, axis = 0)
    col = y_tl[:, resolution[1] - 1]
    y_tl = np.insert(y_tl, resolution[1], col, axis = 1)

    y_tr = YY[:-1, 1:].repeat(delta, 0).repeat(delta, 1)
    row = y_tr[resolution[0] - 1]
    y_tr = np.insert(y_tr, resolution[0], row, axis = 0)
    col = y_tr[:, 0]
    y_tr = np.insert(y_tr, 0, col, axis = 1)

    y_bl = YY[1:, :-1].repeat(delta, 0).repeat(delta, 1)
    row = y_bl[0]
    y_bl = np.insert(y_bl, 0, row, axis = 0)
    col = y_bl[:, resolution[1] - 1]
    y_bl = np.insert(y_bl, resolution[1], col, axis = 1)

    y_br = YY[1:, 1:].repeat(delta, 0).repeat(delta, 1)
    row = y_br[0]
    y_br = np.insert(y_br, 0, row, axis = 0)
    col = y_br[:, 0]
    y_br = np.insert(y_br, 0, col, axis = 1)


    # ---------------------------------------- Gradient Matricies ----------------------------------------
    grad_tl = angs[:-1, :-1].repeat(delta, 0).repeat(delta, 1)
    row = grad_tl[resolution[0] - 1]
    grad_tl = np.insert(grad_tl, resolution[0], row, axis = 0)
    col = grad_tl[:, resolution[1] - 1]
    grad_tl = np.insert(grad_tl, resolution[1], col, axis = 1)

    grad_tr = angs[:-1, 1:].repeat(delta, 0).repeat(delta, 1)
    row = grad_tr[resolution[0] - 1]
    grad_tr = np.insert(grad_tr, resolution[0], row, axis = 0)
    col = grad_tr[:, 0]
    grad_tr = np.insert(grad_tr, 0, col, axis = 1)

    grad_bl = angs[1:, :-1].repeat(delta, 0).repeat(delta, 1)
    row = grad_bl[0]
    grad_bl = np.insert(grad_bl, 0, row, axis = 0)
    col = grad_bl[:, resolution[1] - 1]
    grad_bl = np.insert(grad_bl, resolution[1], col, axis = 1)

    grad_br = angs[1:, 1:].repeat(delta, 0).repeat(delta, 1)
    row = grad_br[0]
    grad_br = np.insert(grad_br, 0, row, axis = 0)
    col = grad_br[:, 0]
    grad_br = np.insert(grad_br, 0, col, axis = 1)


    # ---------------------------------------- Calculating distance ----------------------------------------
    d_tlx, d_tly = (xx - x_tl), (yy - y_tl)
    d_trx, d_try = (xx - x_tr), (yy - y_tr)
    d_blx, d_bly = (xx - x_bl), (yy - y_bl)
    d_brx, d_bry = (xx - x_br), (yy - y_br)

    # ---------------------------------------- Calculating dot product ----------------------------------------
    dot_tl = d_tlx * np.cos(grad_tl) + d_tly * np.sin(grad_tl)
    dot_tr = d_trx * np.cos(grad_tr) + d_try * np.sin(grad_tr)
    dot_bl = d_blx * np.cos(grad_bl) + d_bly * np.sin(grad_bl)
    dot_br = d_brx * np.cos(grad_br) + d_bry * np.sin(grad_br)

    # ---------------------------------------- Interpolation & Normalization ----------------------------------------
    def interpolate(t):
        f = 6*t**5 - 15*t**4 + 10*t**3
        return f

    ones = np.ones((samples[0], samples[1]))

    influence_tl = interpolate(ones - abs(d_tlx)) * interpolate(ones - abs(d_tly))
    influence_tr = interpolate(ones - abs(d_trx)) * interpolate(ones - abs(d_try))
    influence_bl = interpolate(ones - abs(d_blx)) * interpolate(ones - abs(d_bly))
    influence_br = interpolate(ones - abs(d_brx)) * interpolate(ones - abs(d_bry))

    # Final noise & normalization
    noise_raw = influence_tl * dot_tl + influence_tr * dot_tr + influence_bl * dot_bl + influence_br * dot_br
    burn_mat = np.ones((samples[0], samples[1]))
    indicies = [[np.array([*product(range(0, samples[0], delta), range(0, samples[1], delta))])]]
    burn_mat[indicies,:] = burn
    burn_mat[:, indicies] = burn
    noise_raw *= burn_mat
    noise_norm = 255 * (noise_raw - np.amin(noise_raw)) / (np.amax(noise_raw) - np.amin(noise_raw))
    return noise_norm

# ----------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------




# ---------------------------------------- Fractal Noise ----------------------------------------
# ----------------------------------------------------------------------------------------------------
def Octave(resolution, octaves = 3, lacunarity = 2, persistance = 0.5, seed = 1):
    """
    Lacunarity equates to first octave node scale. Resolution should be divisible by every lancunarity^octave permutation.
    """
    zraw = np.zeros((resolution + 1, resolution + 1))
    for i in range(octaves):
        freq = lacunarity ** i
        weight = persistance ** i
        oct = Perlin(freq, resolution, seed)
        zraw += weight * oct
    znorm = 255 * (zraw - np.amin(zraw)) / (np.amax(zraw) - np.amin(zraw))
    return znorm

# ----------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------
