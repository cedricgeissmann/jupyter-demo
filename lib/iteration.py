# -*- coding: utf-8 -*-
from matplotlib import pyplot as plt
from random import uniform

import numpy as np


def sir_modell(x, **kwargs):
    """Iterationsfunktion für das SIR-Modell."""
    x_elem = list(x)
    assert len(x_elem) == 7
    a = kwargs.get("a")
    b = kwargs.get("b")
    c = kwargs.get("c")
    d = kwargs.get('d', 0)
    e = kwargs.get('e', 0)
    f = kwargs.get('f', 0)
    k = kwargs.get('k', 0)
    g = kwargs.get('g', 0)
    h = kwargs.get('h', 0)
    i = kwargs.get('i', 0)
    j = kwargs.get('j', 0)
    daily_fluctuations = kwargs.get('daily_fluctuations', 0.1)

    a = a * uniform(1-daily_fluctuations, 1+daily_fluctuations)
    b = b * uniform(1-daily_fluctuations, 1+daily_fluctuations)
    c = c * uniform(1-daily_fluctuations, 1+daily_fluctuations)
    d = d * uniform(1-daily_fluctuations, 1+daily_fluctuations)

    S = x[0]
    I = x[1]
    R = x[2]
    D = x[3]
    V = x[4]
    VI = x[5]
    T = x[6]

    N = sum(x)

    a = a / N
    h = h / N
    j = j / N
    g = g / N

    S_new = S - a * S * I + b * I - d * S + e * R + f * V - h * VI * S - j * T * S
    I_new = I + a * S * I - b * I - c * I - k * I - g * V * I + h * VI * S + j * T * S
    R_new = R + c * I - e * R + b * VI
    D_new = D + k * I
    V_new = V + d * S - f * V
    VI_new = VI + g * V * I - b * VI
    T_new = T + i * I - b * T

    return [S_new, I_new, R_new, D_new, V_new, VI_new, T_new]


def iteration(func, x0, n=10, cond=lambda x: False, **kwargs):
    """
    Führt eine Iteration der Funktion f durch.

    f: ist die Funktion die als Iterationsmodell verwendet wird.
    x0: ist der Startwert der Iteration.
    cond: ist eine callback-Funktion welche die Iteration abbricht wenn sie
    erfüllt ist.
    n: ist die Anzahl Zeitschritte der Iteration (default=10).
    kwargs: Weitere argumente die der Iterationsfunktion übergeben werden.
    """
    x_list = [x0]
    for i in range(n):
        if cond(x_list):
            print("Bedingung erfüllt für Element x" + str(i))
            return

        events = kwargs.get('events', None)
        if events:
            if i in events.keys():
                obj = events.get(i)
                for (k, v) in obj.items():
                    kwargs[k] = v

        x_elem = func(x_list[-1], **kwargs)
        x_list.append(x_elem)
    return simple_remap(x_list)


def plot_iteration(iter_list, **kwargs):
    """
    Plottet die Iterationen des Räuber-Beute-Modells.

    iter_list: ist die Rückgabe der Funktion iteration.
    """
    highlight = kwargs.get('highlight', None)
    to_print = kwargs.get('to_plot', {})
    labels = ['Suseptible', 'Infected', 'Removed', 'Dead', 'Vaccinated', 'VI', 'FN-Tested']
    plot=plt.subplot(211)
    for (li, lab) in zip(iter_list, labels):
        if to_print[lab]:
            if highlight and lab in highlight.keys():
                plt.plot(li, label=lab, **highlight.get(lab))
            else:
                plt.plot(li, label=lab)
    plt.legend(bbox_to_anchor=(0, 1, 1, 0), loc="lower left", mode="expand", ncol=3)
    plt.show()


def simple_remap(bad_list):
    """
    Nimmt eine Liste mit Einträgen in der Form [[list1], [list2], ...]
    entgegen, und macht daraus eine Liste der Form [[elem1_list1, elem2_list2,
    ...], [elem1_list2, elem2_list2, ...]].
    """
    return np.reshape(bad_list, (len(bad_list), len(bad_list[0]))).T.tolist()


def mean(iter_list, index):
    """
    Berechnet das arithmetische Mittel von iter_list[0][index],
    iter_list[1][index], ...
    """
    return np.mean(simple_remap(iter_list)[index])
