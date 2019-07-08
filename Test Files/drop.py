#
# 7/1/19
# ---------------------------------------- Droplet Class ----------------------------------------
"""
The droplet class & methods for simulating hydraulic erosion.
"""
# ----------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------

class drop:

    def __init__(self, terrain, water_level, initial_velocity):
        self.water_level = water_level
        self.initial_velocity = initial_velocity
    
    def move(self, gravity, momentum):
        self.gravity = gravity
        self.momentum = momentum
    
    def set_capacity(self, capacity, min_slope):
        self.capacity = capacity
        self.min_slope = min_slope

    def erode(self, rate, radius):
        self.erode_rate = rate
        self.erode_radius = radius
    
    def deposit(self, rate):
        self.deposit_rate = rate

    def evaporate(self, rate, cutoff):
        self.evaporate_rate = rate
        self.cutoff = cutoff