import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from IPython.display import display
from ipywidgets import interactive
import importlib

class design_space:
    def __init__(self):
         return 
        
    def f(self, AA_min = 9.70, AA_max= 72.6, AG_min= 1, AG_max= 7.3):
        if AA_min > AA_max:
            print('AA_min should be smaller than AA_max!')
        if AG_min > AG_max:
            print('AG_min should be smaller than AG_max!')
        f1 = np.linspace(AA_min, AA_max, 6)                                         #Number of samples reagent 1 (x-axis)
        f2 = np.linspace(AG_min, AG_max, 8)                                         #Number of samples reagent 2 (y-axis)
        m1,m2 = np.meshgrid(f1,f2)
        fig, ax = plt.subplots(figsize = (7,5))
        for i in range(m1.shape[0]):
            for j in range(m1.shape[1]):
                plt.scatter(m1[i,j], m2[i,j], s = 200, c = 'red')
        plt.xlim([9.5,75])
        plt.ylim([0.8,8])
        plt.xlabel('Concentration of Ascorbic Acid ($M x 10^{-5}$)')
        plt.ylabel('Concentration of Silver Nitrate ($M x 10^{-5}$)')
        plt.title('Design Space')
        self.m1 = m1
        self.m2 = m2
        for i in range(self.m1.shape[1]):
            column1 = self.m1[:,i]
            column2 = self.m2[:,i]
            if i == 0:
                design_var_1 = column1.reshape(-1,1)
                design_var_2 = column2.reshape(-1,1)
            else:
                design_var_1 = np.vstack((design_var_1, column1.reshape(-1,1)))
                design_var_2 = np.vstack((design_var_2, column2.reshape(-1,1)))
        self.design_var_1 = design_var_1
        self.design_var_2 = design_var_2

    def display_graph(self):
        w = interactive(self.f, AA_min=(9.7,72.6,0.5), AA_max=(9.7,72.6,0.5), AG_min = (1,7.3,0.05), AG_max = (1,7.3,0.05))
        display(w)

    def graph_to_volumes(self):
        stock_conc_1=0.0063 #M                                                         #Stock solution concentration of reagent 1 
        stock_conc_2=0.00064 #M                                                        #Stock solution coencentration of reagent 2 
        v_sample = 1300 #uL                                                            #Total sample volume 
        return self.design_var_1*v_sample/stock_conc_1/10**5, self.design_var_2*v_sample/stock_conc_2/10**5


class experiment:
    def __init__(self):
        return 

    def create_design_space(self):
        self.d = design_space()
        self.d.display_graph()

    def to_volumes(self):
        self.design_var_1, self.design_var_2 = self.d.graph_to_volumes()

    def create_samples(self):
        CTAB = np.array([416]*self.design_var_1.shape[0]).reshape(-1,1)                         #Volume of CTAB 
        Chloroauric = np.array([256]*self.design_var_1.shape[0]).reshape(-1,1)                  #Volume of Chloroauric acid
        SEEDS = np.array([102]*self.design_var_1.shape[0]).reshape(-1,1)                        #Volume of Seeds
        array = np.hstack((CTAB, Chloroauric, self.design_var_1, self.design_var_2, SEEDS))
        water = 1300 - np.sum(array, axis=1)                                                    #Total sample volume 
        array = np.hstack((array[:,0].reshape(-1,1), water.reshape(-1,1), array[:,1:]))
        df = pd.DataFrame(array, columns = ['CTAB-stock', 'Water-stock', 'Chloroauric-stock', 'Ascorbic_Acid-stock','Silver_Nitrate-stock','Gold_Seeds-stock'])
        df.to_csv('samples.csv')
