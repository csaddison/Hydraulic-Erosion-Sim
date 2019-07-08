#
# 7/1/19
# ---------------------------------------- Parameter File ----------------------------------------
"""
An easily editable parameter file for the erosion simulation.
"""
# ----------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------

# Map parameters
noise_scale = 2
terrain_reolution = 256
    # Ends up being (res-2) units after removing edge artifacts.
    # Remember noise.py instructions for res/scale/lanc relations.
noise_octaves = 4
noise_lacunarity = 2
noise_persistance = .8
map_seed = 5

# Rain parameters
drop_iterations = 50000
drop_move_cap = 250
drop_initial_water = 1
rain_seed = 874923
rain_initial_vel = [0, 0]

# Movement parameters
world_gravity = 20
drop_momentum = .2
water_cuttoff = .001

# Erosion parameters
erosion_rate = .9
sediment_capacity_multiplier = 10
deposition_rate =  .02
erosion_radius = 4
min_slope_capacity = .01

# Render parameters
map_colormap = 'YlGn'
map_z_scale = 5
map_board_scale = 10
processing_blur = 1