#Sam Walton
#MT week 2 
#find lowest displacemnet TLP design using simplified model
#Mostly based on the Bachynski
import functions
import math
import itertools


pi = math.pi
g = 9.81 

height_tower = 130
diameter_tower = 6
thickness_tower = 0.06
RNA = 800000
thrust = 2000000#thrust on the centre of the rotor assembly
water_depth = 100

#assuming tendons are made of mild steel for now.
E_tendon = 210000000000 #Young's modulus of mild steel (Pa)

#i just set this as a reasonable value for now as this script isnt about the moorings
#can be updated later
area_tendon = 0.15   #cross-sectional area of each tendon (m^2)

boyancy_ratio = 1.3 #the ratio of the total mas of the water displaced to the total mass of the platform
bt = 20            #the distance between the bottom of the tower and the water line


density_steel = 7850
density_sea_water = 1030
density_upper_central_column = 157
density_lower_central_column = 224
density_pontoon = 202

mass_tower = functions.mass_of_cylinder(height_tower,diameter_tower,thickness_tower,density_steel)

fixed_mass = RNA + mass_tower

best_platform_mass = float("inf")


#using the same notation as the Bachynski paper for most variables
for D1, D2, rp, h1, hp, wp, np in itertools.product(
    range(diameter_tower, 4 * diameter_tower),
    range(diameter_tower, 4 * diameter_tower),
    range(diameter_tower, 40),
    range(1, 70),
    range(1, 10),
    range(1, 10),
    range(3, 6)
):


    A11 = functions.a_t_d(D1) * (h1-bt) + functions.a_t_d(D2) * (hp)
    A11 += functions.added_mass_pontoon_length(np,rp,hp)

    A33 = density_sea_water * pi / 12 * D2 ** 3 + functions.added_mass_pontoon_width(np,rp,wp)
    #calculating the displacement of submerged parts:
    #an approximation considering the pontooons to be cuboids 
    #neglecting the shape of the interface with the central column
    displacement_upper_central_column = functions.volume_of_cylinder(h1-bt,D1,D1/2)
    displacement_lower_central_column = functions.volume_of_cylinder(hp,D2,D2/2)
    displacement_pontoons = np * rp * wp * hp 

    displacement = displacement_upper_central_column + displacement_lower_central_column + displacement_pontoons
    #for the mass of the platform, as with the Bachynski paper
    #the platform is assumed to have some density
    mass_upper_central_column = displacement_upper_central_column * density_upper_central_column
    mass_lower_central_column = displacement_lower_central_column * density_lower_central_column
    mass_pontoons = displacement_pontoons * density_pontoon
    mass_upper_central_above_water = functions.mass_of_cylinder(bt,D1,D1/2,density_upper_central_column)
    mass_platform = mass_upper_central_column + mass_lower_central_column + mass_pontoons + mass_upper_central_above_water

    boyancy = displacement * density_sea_water * g
    total_mass = boyancy / boyancy_ratio / g

    ballast_mass = total_mass - mass_platform - fixed_mass
    
    #moves onto the next iteration if the ballast mass is negative, as this is not a valid design
    if ballast_mass < 0:
        continue
    
    #for now assuming no length reduction due to morrings and connections
    tendon_length = water_depth - h1 - hp + bt
    total_pretension = boyancy - total_mass * g

    K11 = total_pretension / tendon_length

    nt = np # for now assume one tendon per pontoon
    K33 = nt * E_tendon * area_tendon / tendon_length

    #Awp is the cross sectional area at the waterline
    Awp = pi/4 * D1 ** 2 
    C33 = density_sea_water * g * Awp

    #i think this is the correct mass but check
    M11 = total_mass
    M33 = total_mass + A33

    #surge and sway period
    T_n1 = 2 * pi * math.sqrt((A11 + M11 )/ K11)
    #roll and pitch period
    if total_pretension <= 0 or tendon_length <= 0 or (A11 + M11) < 0:
        print(f"DEBUG ERROR: A11={A11}, M11={M11}, K11={K11}, Tendon_Len={tendon_length}, Pretension={total_pretension}")
    T_n3 = 2 * pi * math.sqrt((A33 + M33) / (K33 + C33))

    if mass_platform < best_platform_mass:
        if T_n1 > 25 and T_n3 < 3.5:
            if displacement > 2000:
                best_platform_mass = mass_platform
                best_ballast_mass = ballast_mass
                best_D1 = D1
                best_D2 = D2
                best_rp = rp
                best_h1 = h1
                best_hp = hp
                best_wp = wp
                best_np = np



print("Best platform mass: ", best_platform_mass)
print("Best ballast mass: ", best_ballast_mass)
print("Best Upper central diameter: ", best_D1)
print("Best Lower central diameter: ", best_D2)
print("Best pontoon length: ", best_rp)
print("Best upper central height: ", best_h1)
print("Best pontoon height: ", best_hp)
print("Best pontoon width: ", best_wp)
print("Best number of pontoons: ", best_np)
            