#mt week 4
#Sam Walton

import math
from week_2_tpl_basic_calcs import functions

g = 9.81

real_thrust = 4000000

turbine_radius = 230
tower_height = turbine_radius + 30
thickness = 0.1    
density_steel = 7850
phi = 5
real_yield_strss = 240000000

#chosen fairly randomly
RNA = 1600000

###################find actual factors for thrust and weight
thrust_load_factor = 1.5
weight_load_factor = 1.2
yield_load_factor = 1.2

thrust = real_thrust * thrust_load_factor
yield_stress = real_yield_strss / yield_load_factor

dx = 0.01

mass_best = float("inf")
#looping through to find optimal tower diameters
#for now we are assuming a linear taper from the bottom to the top 
#of the tower
#and we assume constant thickness of the tower wall
for i in range (300,1000,10):
    for j in range (i,1200,10):

        #convert to radius in m
        R_upper = i / 200     #top tower radius
        R_lower = j / 200     #bottom tower radius

        #looping through the height of the tower to check
        #the stress at each point along the tower is within
        #the limits of the material
        works = 0

        for n in range (0, int(tower_height/dx)):

            #check to see if stress is too high elsewhere
            if works > 0:
                continue


            #where x is the distance from the top of the tower
            x = n * dx

            #calculating the radius at this height
            R = R_upper + (R_lower - R_upper) * (x / tower_height)

            #calculating the self weight of the tower above this point
            tower_selfweight_above = functions.mass_of_tapered_cylinder(x, 2*R_upper, 2*R, thickness, density_steel) * 9.81
            weight_above_real = RNA + tower_selfweight_above
            weight_above = weight_above_real * weight_load_factor

            #calculating the axial force along the tower
            force_axial = (thrust * math.sin(math.radians(phi))
                + math.cos(math.radians(phi)) * weight_above
                )       

            #calculating the intergral of the intergral
            #of the weight per unit length
            intint_weight_per_length = density_steel * g * math.pi * (
                (2 * thickness * R_upper - thickness ** 2) * x ** 2 / 2
                + (R_lower - R_upper) * thickness * x ** 3 / (3 * tower_height)
                )

            #calculating the moment at this point in the tower
            moment_at_x = (x * thrust * math.cos(math.radians(phi))
                 - x * RNA * math.sin(math.radians(phi))
                - math.sin(math.radians(phi)) * intint_weight_per_length
                )

            #finding the stresses in the tower

            #stress due to axial forces
            area = math.pi * (2 * R * thickness - thickness**2)
            stress_axial = force_axial / area

            #stress due to bending moments
            R_inner = R - thickness
            I = math.pi * (R ** 4 - R_inner ** 4) / 2
            stress_moment = moment_at_x * R / I

            total_stress = stress_axial + stress_moment

            if total_stress > yield_stress:
                works = works + 1

        if works == 0:

            mass = functions.mass_of_tapered_cylinder(tower_height, 2*R_upper, 2*R_lower,thickness,density_steel)

            if mass < mass_best:
                best_R_upper = R_upper
                best_R_lower = R_lower
                mass_best = mass


print("in kg mass is:")
print(mass_best)
print ("in m")
print("upper radius:")
print(best_R_upper)
print("lower radius: ")
print(best_R_lower)