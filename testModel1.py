# -*- coding:utf-8 -*-
"""
Project: MathematicsModeling-2023.5
Written by: Evan Wong
DATE: 2023/5/9
TIME: 17:09
"""

import matplotlib.pyplot as plt

monthdays = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
temperatures = [-1, 2, 6, 12, 22, 28, 31, 32, 26, 23, 15, 2]

COP = 3.5
EER = 2.7

length = 4
width = 3
height = 3

roof_thickness = 0.3
roof_thermal = 0.2
roof_square = length * width
windowAndDoor_thickness = 0.1
windowAndDoor_thermal = 1.6
windowAndDoor_square = 5
wall_thickness = 0.3
wall_thermal = 0.3
wall_square = (length + width) * height * 2 - windowAndDoor_square
ground_thickness = 1.0
ground_thermal = 0.25
ground_square = length * width


def get_delta_t(tout):
    if tout < 18:
        return 18 - tout
    elif tout > 26:
        return 26 - tout
    else:
        return 0


def get_qmake(k, a, t, d):
    return (k * a * t) / d


def get_day_qmake(dt):
    if dt == 0:
        return 0.0

    day_qmake = \
        get_qmake(wall_thermal, wall_square, dt, wall_thickness) + \
        get_qmake(windowAndDoor_thermal, windowAndDoor_square, dt, windowAndDoor_thickness) + \
        get_qmake(roof_thermal, roof_square, dt, roof_thickness) + \
        get_qmake(ground_thermal, ground_square, dt, ground_thickness)
    return day_qmake * 86400


def get_month_qmake(month):
    return get_day_qmake(abs(get_delta_t(temperatures[month]))) * monthdays[month]


def get_qelec(qmake, dt):
    if dt < 0:
        return qmake / EER
    elif dt == 0:
        return 0
    else:
        return qmake / COP


def get_carbon_emission(qelec):
    return (qelec / 3600000) * 0.28


carbonEmissions = []
for i in range(0, 12):
    qelec = get_qelec(get_month_qmake(i), get_delta_t(temperatures[i]))
    carbonEmissions.append(get_carbon_emission(qelec))

print("Sum of carbon emissions: " + str(sum(carbonEmissions)) + "kg")

plt.figure(figsize=(10, 6))
plt.bar(range(1, len(carbonEmissions) + 1), carbonEmissions, fc='g')
plt.title("Carbon Emissions")
plt.xlabel("Month")
plt.ylabel("kg")

plt.show()
