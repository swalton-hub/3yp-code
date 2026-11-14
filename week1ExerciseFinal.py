#design of simple spar flotation system to minimise steel weight
#Sam Walton oct 26
#MT week1

import math
pi = math.pi

#defining fixed variables
m_t = 1142600   #mass of turbine tower
RNA = 800000    #mass of turbine nacelle assembly
m_f = m_t + RNA #fixed mass
t = 0.1         #wall thickness of spar
thrust = 2000000#thrust on the centre of the rotor assembly
g = 9.81        #gravitational constant
t_t = 0.06      #thickness of tower
h_t = 130       #tower height

#densities
p_steel = 7850
p_sea_water = 1030
p_b = 2000

#predefining list for spar mass
w = [[float("inf") for i in range(31)] for j in range(100)]

#looping for range of spar depth and diameter
for depth in range (100):
    for D in range (30):

        D_i = D - t

        #finding the amount of balast
        m_b = depth * pi * D**2/4 * p_sea_water - m_f - pi * (D * t - t**2) * (depth + 20) * p_steel
        h_b = 4 * m_b / (pi * p_b * D_i**2)

        #spar height and mass
        h_s = depth + 20
        m_s = pi * (D*t-t**2) * (depth + 20) * p_steel

        #total mass
        m = m_f + m_s + m_b + RNA
        
        #finding distance of CoM from the bottom
        MRcm = 800000 * (150 + depth) + m_b * h_b / 2 + m_s * h_s / 2 + m_t * ((130/2) + h_s)
        r_cm = MRcm / m


        #roll angle under rated thrust
        tantheta = thrust  * (depth/2 - r_cm) / (m * g * (150 + depth - r_cm))
        theta = math.degrees(math.atan(tantheta))

        #time period of oscillation
        #mass moments of inertia
        I_b = m_b * (3/4 * D_i**2 + h_b**2) / 12
        I_s = m_s * D**2 * (1 - t + t**2 / 2) / 4
        I_t = m_t * D**2 * (1 - t_t + t_t**2 / 2) / 4

        I = I_b + I_s + I_t + m_b * h_b**2 / 4 + m_s * h_s**2 / 4 + m_t * (h_s + h_t/2)**2


        #finding the spring constant k
        k = m * g * (depth/2 - r_cm)

        #final time period calculation
        if I > 0:
            if k > 0:
                T = 2 * pi * math.sqrt(I/k)
            else:
                T = 0
        else:
            T = 0

        if h_b > 0:
            if theta <= 5:
                if T >= 10:
                    w[depth][D] = m_s


#im sure theres a better way to do this
#finding the configuation with the lowerst spar weight

best_depth = 0
best_d = 0
minw = w[0][0]
for depth in range (0,100):
    for D in range (0,30):
        if w[depth][D] < minw:
            minw = w[depth][D]
            best_depth = depth
            best_d = D



print ("best depth:")
print (best_depth)
print ("best diameter:")
print (best_d)
print ("steel weight in spar:")
print (minw)
