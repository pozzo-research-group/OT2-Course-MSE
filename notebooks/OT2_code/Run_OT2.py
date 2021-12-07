import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from IPython.display import display
from ipywidgets import interactive
from . import CreateSamples
from . import OT2Commands as ALH
from opentrons import simulate, execute, protocol_api
import importlib
import pandas as pd

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

    def create_protocol(self):
        wellplate_pos = input('Enter position of the falcon 48 wellplate (1-11): ')
        stock_pos = input('Enter position of the stock solution (1-11): ')
        large_tiprack_pos = input('Enter position of the 1000uL tiprack (1-11): ')
        small_tiprack_pos = input('Enter position of the 300uL tiprack (1-11): ')
        labels = ['OT2 Destination Labwares',
                  'OT2 Destination Labware Slots',
                  'OT2 Stock Labwares',
                  'OT2 Stock Labware Slots',
                  'OT2 Right Pipette',
                  'OT2 Right Pipette Aspiration Rate (uL/sec)',
                  'OT2 Right Pipette Dispense Rate (uL/sec)',
                  'OT2 Right Tipracks',
                  'OT2 Right Tiprack Slots',
                  'OT2 Left Pipette',
                  'OT2 Left Pipette Aspiration Rate (uL/sec)',
                  'OT2 Left Pipette Dispense Rate (uL/sec)',
                  'OT2 Left Tipracks',
                  'OT2 Left Tiprack Slots',
                  'OT2 Bottom Dispensing Clearance (mm)']
        description = [["opentrons_96_tiprack_1000ul"],
                      '["'+ str(wellplate_pos) + '"]',
                      ["opentrons_96_tiprack_1000ul"],
                      '["'+ str(stock_pos) + '"]',
                      '"' + 'p1000_single' + '"',
                      500,
                      700,
                      ["opentrons_96_tiprack_1000ul"],
                      '["'+ str(large_tiprack_pos) + '"]',
                      '"' + 'p300_single_gen2' + '"',
                      500,
                      700,
                      ["opentrons_96_tiprack_300ul"],
                      '["'+ str(small_tiprack_pos) + '"]',
                      25]
        labels = np.array(labels).reshape(-1,1)
        description = np.array(description, dtype=object).reshape(-1,1)
        protocol = np.hstack((labels, description))
        protocol = pd.DataFrame(protocol)
        protocol.to_csv('OT2_code/protocol.csv', header = False, index = False)

    def create_samples(self):
        CTAB = np.array([416]*self.design_var_1.shape[0]).reshape(-1,1)                         #Volume of CTAB 
        Chloroauric = np.array([256]*self.design_var_1.shape[0]).reshape(-1,1)                  #Volume of Chloroauric acid
        SEEDS = np.array([102]*self.design_var_1.shape[0]).reshape(-1,1)                        #Volume of Seeds
        array = np.hstack((CTAB, Chloroauric, self.design_var_1, self.design_var_2, SEEDS))
        water = 1300 - np.sum(array, axis=1)                                                    #Total sample volume 
        array = np.hstack((array[:,0].reshape(-1,1), water.reshape(-1,1), array[:,1:]))
        df = pd.DataFrame(array, columns = ['CTAB-stock', 'Water-stock', 'Chloroauric-stock', 'Ascorbic_Acid-stock','Silver_Nitrate-stock','Gold_Seeds-stock'])
        df.to_csv('OT2_code/samples.csv')

    def stock_position(self):
        path = r"OT2_code/protocol.csv"
        chem_path = r"OT2_code/Chemical Database.csv"
        plan = CreateSamples.get_experiment_plan(path, chem_path)
        stock_volumes = CreateSamples.concentration_from_csv('OT2_code/samples.csv')
        stock_volumes = stock_volumes.loc[:, ~stock_volumes.columns.str.contains('^Unnamed')]
        stock_volumes['CTAB-stock'].sum(axis=0)
        stock_volumes.astype(int)
        labware_dir_path = r"Custom Labware"
        custom_labware_dict = ALH.custom_labware_dict(labware_dir_path)
        self.protocol = simulate.get_protocol_api('2.8') #
        self.loaded_dict = ALH.loading_labware(self.protocol, plan)
        max_source_vol = 17000
        self.stock_position_info = ALH.stock_well_ranges(stock_volumes, self.loaded_dict, max_source_vol)
        self.stock_volumes = stock_volumes
        for k , v in self.stock_position_info.items(): # iterating freqa dictionary
            print(k+"\t", v)

    def simulate_protocol(self):
        START_POS = 0                                                                             #Start Position of wellplate 
        self.directions = ALH.create_sample_making_directions(self.stock_volumes, self.stock_position_info, self.loaded_dict, start_position=START_POS)
        ALH.pipette_volumes_component_wise(self.protocol, self.directions, self.loaded_dict) 


    def execute_protocol(self):
        # Executing 
        protocol = execute.get_protocol_api('2.8')
        loaded_dict = ALH.loading_labware(protocol, plan)
        max_source_vol = 17000
        stock_position_info = ALH.stock_well_ranges(stock_volumes, loaded_dict, max_source_vol) 
        directions = ALH.create_sample_making_directions(stock_volumes, stock_position_info, loaded_dict, start_position=START_POS)
        ALH.pipette_volumes_component_wise(protocol, directions, loaded_dict)




