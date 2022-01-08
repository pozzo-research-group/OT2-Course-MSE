import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams.update({'font.size': 19})

class plot_data:
    def __init__(self):
        return 
    
    def load_data(self):
        self.df = pd.read_excel('Characterize_Samples/spectra.xlsx')
        wavelength = np.array(self.df.iloc[:, 0])
        location = np.where(wavelength == 400)[0][0]
        self.df = self.df.iloc[location:]
        
    def plot_all_spectra(self, **kwargs):
        option = kwargs['option']
        array = np.asarray(self.df)
        samples = array.shape[1]
        columns = 8
        rows = (samples + columns - 1) // columns - 1
        fig, ax = plt.subplots(figsize = (60,columns*4),ncols = columns, nrows = rows)
        for sample in range(array.shape[1]-1):
            if option == 1: # Option to fill columns by column 
                x = (sample / 6)
                y = (sample % 6)
            elif option == 2: # Option to fill row by row
                x = (sample % 8)
                y = (sample / 8)
            ax[int(y), int(x)].plot(array[:,0], array[:,sample+1])
            ax[int(y), int(x)].set_title(self.df.columns[sample+1],x = 0.07, y = 0.95, size='25', weight='bold', pad=-15)
            ax[int(y), int(x)].set_xlabel('Wavelength (nm)', size='19',)
            ax[int(y), int(x)].set_ylabel('Intensity', size='19',)
            