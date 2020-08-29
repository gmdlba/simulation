# -*- coding: utf-8 -*-
"""
Created on Tue Aug 18 14:17:14 2020

@author: mdelabarra
"""

# DESARROLLO DE UNA SIMULACIÓN MONTE CARLO DE UN SISTEMA DE 3 COMPONENTES"
# lIBRERIAS Y DEPENDENCIAS
from random import uniform
import math
import matplotlib.pyplot as plt
import sys
sys.path.append("..")

##############
# CLASES
from src.domain.component import Component
from src.domain.system import System_Status
from src.domain.simulation_param import Simulation


def lambdas(a):
    lambda_system = []
    for states in range(len(a)):
        if states == 0:
            if a[states] == 1:
                lambda_system.append(componente_A.fail_ratio)
            else:
                lambda_system.append(componente_A.repair_ratio)
        elif states == 1:
            if a[states] == 1:
                lambda_system.append(componente_B.fail_ratio)
            else:
                lambda_system.append(componente_B.repair_ratio)
        else:
            if a[states] == 1:
                lambda_system.append(componente_C.fail_ratio)
            else:
                lambda_system.append(componente_C.repair_ratio)
    return lambda_system


########################
# LOGIC CONTROL
# BUILDING THE 3 COMPONENTS OF THE SYSTEM
componente_A = Component(0.001, 0.1, 1)
componente_B = Component(0.002, 0.15, 1)
componente_C = Component(0.005, 0.05, 1)

system = [componente_A, componente_B, componente_C]

ejecuciones = 40
mission_time = 500

# SET UP SYSTEM STATUS
system_global_state = System_Status()

# SET UP TOTAL FAILURE CONFIGURATIONS OF THE SYSTEM
total_failure = {"config#1": [2, 2, 1], "config#2": [2, 2, 2], "config#3": [2, 1, 2]}

total_states = [[1, 1, 1], [1, 1, 2], [1, 2, 1], [1, 2, 2], [2, 1, 1], [2, 1, 2], [2, 2, 1], [2, 2, 2]]

sims = 0  # Se inicializa el contador de simulaciones
exitos = 0
fracasos = 0

lifetime_acumulado = 0
max_state = 0

# SET UP SIMULATION PARAMETERS
simulation = Simulation(mission_time, ejecuciones)  # Se inicializan las variables de la simulación

final_status_list = []

while sims < simulation.executions_number:
    life_time = [0]
    lambda_system = [componente_A.fail_ratio, componente_B.fail_ratio, componente_C.fail_ratio]

    system_global_state.plant_state = [1, 1, 1]
    simulation_states = [1]

    while not (system_global_state.plant_state in total_failure.values()) and life_time[-1] < simulation.mission_time:


        aleatorio = uniform(0, 1)

        new_time = life_time[-1] - (1 / sum(lambda_system) * math.log(1 - aleatorio))
        life_time.append(new_time)

        updated = False
        # Sum the repair and fail ratio of all previous components
        repair_ratio_acum = 0
        fail_ratio_acum = 0

        for i in range(len(system)):
            if not updated:
                # Add the current fail and repair ratio to the accumulators
                repair_ratio_acum += system[i].repair_ratio
                fail_ratio_acum += system[i].fail_ratio

                if system_global_state.plant_state[i] == 1:  # The component is working
                    # Check if the component has failed
                    if fail_ratio_acum / sum(lambda_system) > aleatorio:
                        system_global_state.plant_state[i] = 2  # Update component state
                        lambda_system = lambdas(system_global_state.plant_state)  # Update system lambda
                        updated = True
                else:  # The component is not working
                    # Check if the component has been repaired
                    if repair_ratio_acum / sum(lambda_system) > aleatorio:
                        system_global_state.plant_state[i] = 1  # Update component state
                        lambda_system = lambdas(system_global_state.plant_state)  # Update system lambda
                        updated = True

        # Get the integer equivalent to the plant state
        current_state = total_states.index(system_global_state.plant_state) + 1
        simulation_states.append(current_state)
        if current_state > max_state:
            max_state = current_state

    # Collect statistics
    lifetime_final = life_time[-1]

    lifetime_acumulado = lifetime_acumulado + lifetime_final

    sims += 1
    final_status_list.append(lambda_system)
    exito = True
    if life_time[-1] < mission_time:
        fracasos += 1
        exito = False
    else:
        exitos += 1

    plt.plot(life_time, simulation_states, linewidth=1, drawstyle='steps-mid', label="sim" + str(sims))

    # plt.plot(mission_time * 1.1, list2, drawstyle='steps-mid', label="s" + str(sims))
    # print(f"Sim number: {sims} = {system_global_state.plant_state}. Time = {life_time[-1]}. Exito = {exito}")

print(f"Exitos: {exitos}")
print(f"Fracasos: {fracasos}")
print(f"Fiabilidad: {100 * exitos / ejecuciones}%")
print(f"Lifetime medio: {lifetime_acumulado / sims}")

plt.grid(axis='y')
plt.ylabel("System Status")
plt.xlabel("Life Time")
plt.yticks([1, 2, 3, 4, 5, 6, 7, 8], total_states)
plt.vlines(mission_time, 1, max_state, colors='red', linestyles='dotted', label='Mission Time')
plt.text(520, 4.5, r'mission time')
#plt.vlines(lifetime_acumulado / sims, 1, max_state, colors='blue', linestyles='dotted', label='Average MT')
plt.grid(axis='x', color='0.95')
#plt.legend(title='Sim. Number:')
plt.title('Monte Carlo Simulations')
plt.show()
