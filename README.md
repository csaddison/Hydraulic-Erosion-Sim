# Hydraulic Erosion Simulation

###### Processing heightmaps for simulated droplet-based erosion.

Creating procedural terrain from heghtmaps is easily done with [classical noise generators](https://github.com/csaddison/Perlin-Noise) and fractal noise, however making that terrain look realistic is often much harder. Depending on how many octaves you use, proceduarly generated terrain is either too smooth or too jagged to look realistic. Natural terrain has a combination of these features, with rocky mountains and flatter rolling plains. A leading cause of this is the natural erosion of the terrain over time, especially due to rivers and rainfall. By simulating thousands of rain droplets we can compute the movement of the water accross the land and erode and deposit sediment as the drop travels. This leads to realistic erosion patterns, especially in hilly regions, and realisitc valleys in between them. This project is largely a pythonic implementation of the hydraulic erosion algorithm described [here](https://www.firespark.de/resources/downloads/implementation%20of%20a%20methode%20for%20hydraulic%20erosion.pdf).

### Changes

As of 6/24/2019 the code is working but not pretty. Some aspects from the paper have been neglected, such as bilinear interpolation of the gradients and bilinear interpolation on sediment distribution. Instead (mostly due to lack of patience) I've opted for the easier solution of slightly blurring the erosion map after deposition.

The biggest changes coming for this project are to:

* Fix the weights on the erosion radius
* Try and implement smoother deposition

But mainly:

* Refactor into a drop() class

Setting up a drop as its own class would make tracking drop variables (water level, sediment level, carrying capacity, speed, position, etc.) easier and more intuative; and the movement, erosion, and deposition functions could be refactored as class methods. This opens up the possibility for changing drop parameters easily which could introduce rivers and other water sources.