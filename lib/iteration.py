from matplotlib import pyplot as plt

import numpy as np


def rauber_beute(x, **kwargs):
    """Iterationsfunktion für das Räuber-Beute-Modell."""
    x_elem = list(x)
    assert len(x_elem) == 2
    a = kwargs.get("a")
    b = kwargs.get("b")
    c = kwargs.get("c")
    d = kwargs.get("d")
    H = x[0]
    L = x[1]
    H_new = H + a * H - b * H * L
    L_new = L - c * L + d * H * L
    return [H_new, L_new]


def si_modell(x, **kwargs):
    """Iterationsfunktion für das SI-Modell."""
    x_elem = list(x)
    assert len(x_elem) == 2
    a = kwargs.get("a")
    b = kwargs.get("b")
    S = x[0]
    I = x[1]
    S_new = S - a * S + b * I
    I_new = I + a * S - b * I
    return [S_new, I_new]


def sir_modell(x, **kwargs):
    """Iterationsfunktion für das SIR-Modell."""
    x_elem = list(x)
    assert len(x_elem) == 3
    a = kwargs.get("a")
    b = kwargs.get("b")
    c = kwargs.get("c")
    S = x[0]
    I = x[1]
    R = x[2]
    N = S + I + R
    S_new = S - b * I * S / N
    R = R + c * I
    I_new = I + b * S * I / N - c * I
    return [S_new, I_new, R]


def cond(x_list):
    """
    Abbruchbedinnung für die Iteration.

    Diese Funktion wird überschrieben wenn eine Abbruchbedinnung gewünscht wird.
    """
    return False


def iteration(f, x0, n=10, **kwargs):
    """
    Führt eine Iteration der Funktion f durch.

    f: ist die Funktion die als Iterationsmodell verwendet wird.
    x0: ist der Startwert der Iteration.
    n: ist die Anzahl Zeitschritte der Iteration (default=10).
    kwargs: Weitere argumente die der Iterationsfunktion übergeben werden.
    """
    x_list = [x0]
    for i in range(n):
        if cond(x_list):
            print("Bedingung erfüllt für Element x" + str(i))
            return
        x_elem = f(x_list[-1], **kwargs)
        x_list.append(x_elem)
    return x_list


def plot_iteration(iter_list):
    """
    Plottet die Iterationen des Räuber-Beute-Modells.

    iter_list: ist die Rückgabe der Funktion iteration.
    """
    plt.plot(iter_list)
    plt.show()


def plot_phase_diagramm(iter_list, *args, **kwargs):
    """
    Plottet das Phasendiagramm für die Iteration mit 2 Unbekannten (z.B.
    Räuber-Beute-Modell).

    iter_list: ist die Rückgabe der Funktion iteration.
    """
    try:
        new_list = simple_remap(iter_list)

        plt.plot(new_list[0], new_list[1], *args, **kwargs)
        plt.show()
    except TypeError:
        print(
            "Kann nicht geplottet werden! Braucht eine Iterationsfolge mit 2 Variablen..."
        )


def simple_remap(bad_list):
    """
    Nimmt eine Liste mit Einträgen in der Form [[list1], [list2], ...]
    entgegen, und macht daraus eine Liste der Form [[elem1_list1, elem2_list2,
    ...], [elem1_list2, elem2_list2, ...]].
    """
    return np.reshape(bad_list, (len(bad_list), 2)).T.tolist()
