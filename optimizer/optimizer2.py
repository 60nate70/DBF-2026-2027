# Optimization of a simple electric aircraft design for maximum range.
# Author(s): Aryan Patil
# Last Updated: 9/16/26

import aerosandbox as asb
import aerosandbox.numpy as np

opti = asb.Opti()

# 1. Geometry & Power Variables

# Vary the wing span between 3ft to 6ft, converted to meters. 
span = opti.variable(init_guess=1.5, lower_bound=0.914, upper_bound=1.828) 

# Vary the wing chord between 0.33ft to 2ft, converted to meters.
chord = opti.variable(init_guess=0.3, lower_bound=0.101, upper_bound=0.609)

# Vary the motor power between 1000W to 3000W
motor_power = opti.variable(init_guess=2000, lower_bound=1000, upper_bound=3000)

# Vary the battery capacity between 1000Wh to 100000Wh (1kWh - 100kWh)
battery_wh = opti.variable(init_guess=30000, lower_bound=1000, upper_bound=100000)

# Fixed angles of attack for different flight states
alpha_cruise = 0.0
alpha_turn = 10.0
alpha_climb = 15.0

S = span * chord
AR = span / chord

# 2. Physics & Mass Constants
rho, g, e = 1.225, 9.81, 0.85
Cd0 = 0.007
CL0 = 0.20        
CL_slope = 0.10   

m_wing = (0.5 * S) + (0.02 * (AR**1.5))
m_batt = battery_wh / 150.0  

# 1000W motor weighs 4 oz (0.113 kg)
m_motor = motor_power * (0.113 / 1000.0)
W = (1.0 + m_wing + m_batt + m_motor) * g 

# ====================================================================
# 3. OPTIMIZED CRUISE STATE (Straight Flight)
# ====================================================================

CL_cruise = CL0 + (CL_slope * alpha_cruise)
Cd_cruise = Cd0 + ((CL_cruise**2) / (np.pi * e * AR))

# Speed required to hold altitude at this specific angle
V_cruise = np.sqrt((2 * W) / (rho * S * CL_cruise))

Drag_cruise = 0.5 * rho * (V_cruise**2) * S * Cd_cruise
Power_cruise = Drag_cruise * V_cruise

# ====================================================================
# 4. TURN CONSTRAINT
# ====================================================================
CL_turn = CL0 + (CL_slope * alpha_turn)
Cd_turn = Cd0 + ((CL_turn**2) / (np.pi * e * AR))
V_turn = np.sqrt((2 * W) / (rho * S * CL_turn))

Drag_turn = 0.5 * rho * (V_turn**2) * S * Cd_turn
Power_turn = Drag_turn * V_turn

opti.subject_to(Power_turn < motor_power) 

# ====================================================================
# 5. CLIMB CONSTRAINT
# ====================================================================
CL_climb = CL0 + (CL_slope * alpha_climb)
Cd_climb = Cd0 + ((CL_climb**2) / (np.pi * e * AR))
V_climb = np.sqrt((2 * W) / (rho * S * CL_climb))
Drag_climb = 0.5 * rho * (V_climb**2) * S * Cd_climb

Climb_Rate = V_climb * np.sin(alpha_climb * (np.pi/180)) 
Power_climb = (Drag_climb * V_climb) + (W * Climb_Rate)

opti.subject_to(Power_climb < motor_power) 

# ====================================================================
# 6. OBJECTIVE: Maximize Range
# ====================================================================
# Using 100% ideal power transfer for calculations
Flight_time_seconds = (battery_wh * 3600) / Power_cruise
Range_km = (V_cruise * Flight_time_seconds) / 1000.0

opti.minimize(-Range_km)

# 7. Solve and Output
sol = opti.solve()

print("\n--- OPTIMAL PLANE DESIGN ---")
print(f"Wingspan:     {sol.value(span) / 0.3048:.2f} ft")
print(f"Wing Chord:   {sol.value(chord) / 0.3048:.2f} ft")
print(f"Motor Power:  {sol.value(motor_power):.0f} Watts")
print(f"Battery:      {sol.value(battery_wh):.0f} Wh")
print(f"Weight:       {sol.value(W) / 9.81:.2f} kg")

print("\n--- OPTIMAL FLIGHT DYNAMICS ---")
print(f"Cruise Angle:      {alpha_cruise:.1f} degrees")
print(f"Cruise Speed:      {sol.value(V_cruise):.1f} m/s")
print(f"Cruise Power:      {sol.value(Power_cruise):.0f} W")
print(f"Max Range:         {sol.value(Range_km):.1f} km")