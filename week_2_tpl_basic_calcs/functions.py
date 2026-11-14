#Sam Walton
#MT week 2 
#Function for TLP
import math

pi = math.pi


def volume_of_cylinder(height,diameter,thickness):
    radius = diameter / 2
    area = pi * (2 * radius * thickness - thickness ** 2)
    volume = area * height
    return volume


def mass_of_cylinder(height,diameter,thickness,density):
    volume = volume_of_cylinder(height,diameter,thickness)
    mass = volume * density
    return mass

def volume_of_tapered_cylinder(height,top_diameter,bottom_diameter,thickness):
    top_radius = top_diameter / 2
    bottom_radius = bottom_diameter / 2
    area = pi * ((top_radius + bottom_radius) * thickness - thickness ** 2)
    volume = area * height
    return volume

def mass_of_tapered_cylinder(height,top_diameter,bottom_diameter,thickness,density):
    volume = volume_of_tapered_cylinder(height,top_diameter,bottom_diameter,thickness)
    mass = volume * density
    return mass


#functions for added mass due to interacting with the water
#1030 is the density of sea water in kg/m^3
#square section
def a_t_h (h):
    a_t = 4.754/4 * 1030 * h ** 2 
    return a_t

#cylindrical section
def a_t_d (d):
    a_t = 1030 * pi * d ** 2 / 4
    return a_t

#functions for the added mass due to waves for pontoons
def added_mass_pontoon_length (np,rp,hp):
    theta_diff = 360/np
    added_mass = 0

    for i in range (np):
        theta = i * theta_diff
        added_mass += rp * a_t_h(hp) * math.cos(math.radians(theta)) ** 2
    return added_mass

def added_mass_pontoon_width (np,rp,wp):
    added_mass = 0

    for i in range (np):
        added_mass += rp * a_t_h(wp)
    return added_mass