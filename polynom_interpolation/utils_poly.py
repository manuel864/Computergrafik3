import numpy as np
from fractions import Fraction
from math import sqrt

def vander(a):
    n = len(a)
    ergb = []
    for x in a:
        row = []
        for i in range(n):
            row.append(pow(x,i))
        ergb.append(row)
    return np.array(ergb)

def map_range(value, old_min, old_max, new_min, new_max):
        old_range = old_max - old_min
        new_range = new_max - new_min
        scaled_value = (value - old_min) / old_range
        mapped_value = new_min + (scaled_value * new_range)
        return mapped_value

def convert_to_numpy_polynomial(string):
    # Extrahiere die Koeffizienten aus dem String
    coefficients = []
    for coeff in string.split(','):
        coeff = coeff.strip()
        if '/' in coeff:
            coeff = Fraction(coeff)
        elif 'sqrt' in coeff:
            coeff = float(coeff[5:-1])  # Entferne "sqrt(" und ")"
            coeff = sqrt(coeff)
        else:
            coeff = float(coeff)
        coefficients.append(coeff)

    # Erstelle das Numpy-Polynom
    polynomial = np.poly1d(coefficients)

    return polynomial


def check_target_hits(targets,poly):
    threshold = 0.01
    for t in targets:
        x = t.x 
        y = t.y 
        poly_y = np.polyval(poly,x)
        if abs(poly_y-y) <= threshold:
            t.is_hit = True



