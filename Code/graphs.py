import numpy as np
import matplotlib.pyplot as plt
from IPython.display import display
from ipywidgets import interactive

def f(AA_min = 5, AA_max= 45, AG_min= 5, AG_max= 45):
    if AA_min > AA_max:
        print('AA_min should be smaller than AA_max!')
    if AG_min > AG_max:
        print('AG_min should be smaller than AG_max!')
    f1 = np.linspace(AA_min, AA_max, 5)
    f2 = np.linspace(AG_min, AG_max, 5)
    m1,m2 = np.meshgrid(f1,f2)
    fig, ax = plt.subplots(figsize = (7,5))
    for i in range(m1.shape[0]):
        for j in range(m1.shape[1]):
            plt.scatter(m1[i,j], m2[i,j], s = 200, c = 'red')
    plt.xlim([0,50])
    plt.ylim([0,50])
    plt.xlabel('Volume of AA')
    plt.ylabel('Volume of AG')
    plt.title('Design Space')

def display_graph():
    w = interactive(f, AA_min=(0,50,1), AA_max=(0,50,1), AG_min = (0,50,1), AG_max = (0,50,1))
    display(w)