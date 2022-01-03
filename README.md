# OT2-Course-MSE
Course documents and code for introduction to high-throughput experimentation module for MSE

## Description 

<p align="center">
<img src= "images/summary.jpg" width = "700"/>
</p>

The purpose of this module is to introduce high-throughput experimentation for the synthesis of gold nanoparticles. Students will explore the design space used to create gold nanoparticles and then autonomously synthesize them using an OT2 liquid handling robot. Depending on the chosen regent concentrations, nanospheres or nanorods may form, which can sometimes be identified by the sample's color, or more accurately, by characterizing them using Uv-vis Spectroscopy. All the modules can be easily run using jupyter notebooks, without any coding experience.  


## Installation
Each of the folders contain jupyter notebooks that must be used to perform the module. The first folder, "1.Design_Space", creates the samples that will be made with the OT2. The second folder, "2.Run_OT2", is used to command the OT2 to create the samples made previously. The thrid folder, "3.Characterize_Samples", is used to plot the Uv-vis data of each sample.    

The notebooks from the folders, "1.Design_Space" and "3.Characterize_Samples" must be opened through jupyter notebook from anaconda, while the folder "2.Run_OT2" must be opened from the jupyter notebook from the OT2.  


### For "2.Run_OT2": ###

1. To install this library, first download the zip file from github.

<p align="center">
<img src= "images/download_zip.jpg" width = "300"/>
</p>

2. Open the jupyter notebook from the OT2 app.

<p align="center">
<img src= "images/jupyter notebook OT2.jpg" width = "400"/>
</p>

3. Upload the zip file to the OT2 jupyter notebook.

<p align="center">
<img src= "images/upload_file.jpg" width = "700"/>
</p>

4. Open the terminal.

<p align="center">
<img src= "images/terminal.jpg" width = "700"/>   
</p>

5. Run the following lines of code to unzip the file: 
```
	cd var/lib/jupyter/notebooks 
	unzip OT2-Course-MSE-main
```