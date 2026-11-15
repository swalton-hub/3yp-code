#mt week 4
#Sam Walton

import math
from week_2_tpl_basic_calcs import functions
import sympy as sp

g = 9.81

real_thrust = 4000000

turbine_radius = 230
tower_height_loop = turbine_radius + 30
#thickness = 0.1    
density_steel = 7850
phi = 5
real_yield_strss = 240000000


###################find actual factors for thrust and weight
thrust_load_factor = 1.5
weight_load_factor = 1.2
yield_load_factor = 1.2

#chosen fairly randomly
RNA_real = 1600000 #mass in kg
RNA = RNA_real * weight_load_factor * g

thrust = real_thrust * thrust_load_factor
yield_stress = real_yield_strss / yield_load_factor

#defining the sympy var
x, R_upper, R_lower, t_upper, t_lower, tower_height = sp.symbols('x R_upper R_lower t_upper t_lower tower_height', positive=True)


#defining a funciton for the radius
radius = R_upper + (R_lower - R_upper) * (x / tower_height)

#defining function for thickness
thickness = t_upper + (t_lower - t_upper) * (x / tower_height)

#defining function for weight per unit length
weight_per_length = density_steel * g * math.pi * (2* radius * thickness - thickness ** 2) * weight_load_factor

#intergrating weight per unit length
int_weight = sp.integrate(weight_per_length,x)

#finding tower weight
tower_weight = int_weight.subs(x,tower_height) - int_weight.subs(x,0)

#shear in beam
shear = thrust * math.cos(math.radians(phi)) - RNA * math.sin(math.radians(phi)) - math.sin(math.radians(phi)) * (int_weight-int_weight.subs(x,0))

#moment
moment_integral = sp.integrate(shear,x)
moment = moment_integral - moment_integral.subs(x,0)
#max moment will be at the base
moment_max = moment.subs(x,tower_height)

#defining fuctions with lamdafy to speed up computations
weight_func = sp.lambdify((R_upper, R_lower, t_upper, t_lower, tower_height), tower_weight, 'math')
moment_func = sp.lambdify((R_upper, R_lower, t_upper, t_lower, tower_height), moment_max, 'math')


mass_best = float("inf")
best_R_upper = None
best_R_lower = None
best_t_upper = None
best_t_lower = None
#looping through to find optimal tower diameters
#for now we are assuming a linear taper from the bottom to the top 
#of the tower
#and we assume constant thickness of the tower wall
for i in range (300,1000,10):
    for j in range (i,1200,10):
        for t1 in range (10,100,10):
            for t2 in range (t1,100,10):

                #convert thickness to m
                t_upper_loop = t1/1000
                t_lower_loop = t2/1000


                #convert to radius in m
                R_upper_loop = i / 200     #top tower radius
                R_lower_loop = j / 200     #bottom tower radius


                #calc of tower weight and the moment at the base usning the sympy stuff
                tower_weight_loop = weight_func(R_upper_loop, R_lower_loop, t_upper_loop, t_lower_loop, tower_height_loop)
                moment_max_loop  =moment_func(R_upper_loop, R_lower_loop, t_upper_loop, t_lower_loop, tower_height_loop)
                mass = tower_weight_loop / g / weight_load_factor


                #finding axial stress, also at the base
                force_axial = thrust * math.sin(math.radians(phi)) + RNA * math.cos(math.radians(phi)) + math.cos(math.radians(phi)) * tower_weight_loop

                area = math.pi * (2 * R_lower_loop * t_lower_loop - t_lower_loop**2)
                stress_axial = force_axial / area

                #finding stress due to moments
                R_inner = R_lower_loop - t_lower_loop
                I = math.pi * (R_lower_loop ** 4 - R_inner ** 4) / 4
                stress_moment = moment_max_loop * R_lower_loop / I
                
                total_stress = stress_axial + stress_moment

                if total_stress < yield_stress:

                    if mass < mass_best:
                        best_R_upper = R_upper_loop
                        best_R_lower = R_lower_loop
                        best_t_upper = t_upper_loop
                        best_t_lower = t_lower_loop
                        mass_best = mass
                    


print("in kg mass is:")
print(mass_best)
print ("in m")
print("upper radius:")
print(best_R_upper)
print("lower radius: ")
print(best_R_lower)
print("upper thickness:")
print(best_t_upper)
print("lower thickness: ")
print(best_t_lower)