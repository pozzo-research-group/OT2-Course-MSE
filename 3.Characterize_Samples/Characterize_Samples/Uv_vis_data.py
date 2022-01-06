import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class plot_data:
    def __init__(self):
        return 
    
    def load_data(self):
        self.df = pd.read_excel('Characterize_Samples/spectra.xlsx')
        
    def plot_all_spectra(self):
        array = np.asarray(self.df)
        samples = array.shape[1]
        columns = 8
        rows= (samples + columns - 1) // columns - 1
        fig, ax = plt.subplots(figsize = (35,columns*1.2),ncols = columns, nrows = rows)
        for sample in range(array.shape[1]-1):
            x = sample % columns
            y = sample / columns
            ax[int(y), x].plot(array[:,0], array[:,sample+1])
            ax[int(y), x].set_title(self.df.columns[sample+1])
            ax[int(y), x].set_xlabel('Wavelength (nm)')
            ax[int(y), x].set_ylabel('Intensity')