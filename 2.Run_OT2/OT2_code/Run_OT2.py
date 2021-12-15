from . import CreateSamples
from . import OT2Commands as ALH
from opentrons import simulate, execute, protocol_api
import numpy as np
import pandas as pd

class run_protocol:
    def __init__(self):
        return 

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
        description = [["opentrons_96_tiprack_1000ul"],                 # Destination labware
                      '["'+ str(wellplate_pos) + '"]',          
                      ["opentrons_96_tiprack_1000ul"],                  # Stock Labware 
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
        protocol.to_csv('Samples_and_Protocol/protocol.csv', header = False, index = False)

    def stock_position(self):
        path = r"Samples_and_Protocol/protocol.csv"
        chem_path = r"OT2_code/Chemical Database.csv"
        samples =  r"Samples_and_Protocol/samples.csv"
        self.plan = CreateSamples.get_experiment_plan(path, chem_path)
        stock_volumes = CreateSamples.concentration_from_csv(samples)
        stock_volumes = stock_volumes.loc[:, ~stock_volumes.columns.str.contains('^Unnamed')]
        stock_volumes['CTAB-stock'].sum(axis=0)
        stock_volumes.astype(int)
        labware_dir_path = r"Custom Labware"
        custom_labware_dict = ALH.custom_labware_dict(labware_dir_path)
        self.protocol = simulate.get_protocol_api('2.8') #
        self.loaded_dict = ALH.loading_labware(self.protocol, self.plan)
        max_source_vol = 17000
        self.stock_position_info = ALH.stock_well_ranges(stock_volumes, self.loaded_dict, max_source_vol)
        self.stock_volumes = stock_volumes
        for k , v in self.stock_position_info.items(): # iterating freqa dictionary
            print(k+"\t", v)

    def simulate_protocol(self):
        self.START_POS = 0                                              #Start Position of wellplate 
        self.directions = ALH.create_sample_making_directions(self.stock_volumes, self.stock_position_info, self.loaded_dict, start_position=self.START_POS)
        ALH.pipette_volumes_component_wise(self.protocol, self.directions, self.loaded_dict) 


    def execute_protocol(self):
        # Executing 
        protocol = execute.get_protocol_api('2.8')
        self.loaded_dict = ALH.loading_labware(protocol, self.plan)
        max_source_vol = 17000
        stock_position_info = ALH.stock_well_ranges(self.stock_volumes, self.loaded_dict, max_source_vol) 
        directions = ALH.create_sample_making_directions(self.stock_volumes, self.stock_position_info, self.loaded_dict, start_position=self.START_POS)
        ALH.pipette_volumes_component_wise(protocol, directions, self.loaded_dict)




