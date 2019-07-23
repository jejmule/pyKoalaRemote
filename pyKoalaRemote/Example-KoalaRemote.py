from pyKoalaRemote import client
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

#create instance to class pyRemote
remote = client.pyKoalaRemoteClient()
#Connect and Login
remote.ConnectAndLoginDialog()

#Open a 2 wavelenghts configuration.
remote.OpenConfigDialog()

#Open main display windows
remote.OpenPhaseWin();
remote.OpenIntensityWin();
remote.OpenHoloWin();

#This block records an hologram so that you can later work offline with the rest of the script. 
#Set logical source 0 (the 1st source of the current configuration) to ON
remote.SetSourceState(0, True, True)
#Set logical source 1 (the 2nd source of the current configuration) to ON
remote.SetSourceState(1, True, True)
#Acquire on hologram
remote.Acquisition2L()
remote.ResetGrab()
#Save holo to file
#path = Path(r'c:\tmp')
path = Path.cwd()/'data'
remote.SaveImageToFile(1, str(path/'holo.tiff'))

#Load previously recorded hologram
remote.LoadHolo(str(path/'holo.tiff'), 2);

#Display lambda 1 image in phase window
remote.SelectDisplayWL(8192);

#Save hologram image
remote.SaveImageToFile(1, str(path/'holo.tiff'));
#Save intensity image
remote.SaveImageToFile(2, str(path/'intensity.tiff'));
#Save phase image (as displayed, which means phase lamabda 1)
remote.SaveImageToFile(4, str(path/'phase.tif'));
#//Save intensity float in bin
remote.SaveImageFloatToFile(2, str(path/'intensity.bin'), True);
#//Save phase float in bin
remote.SaveImageFloatToFile(4, str(path/'phase.bin'), True);
print('files saved in',str(path))

#//This block only works for 2 wavelengths configurations
#//Display lambda 2 image in intensity window
remote.SelectDisplayWL(4096);
#//Display lambda 2 image in phase window
remote.SelectDisplayWL(16384);
#//Save intensity image (as displayed, which means intensity lambda 2)
remote.SaveImageToFile(2, str(path/'intensity2.tiff'));
#//Save phase image (as displayed, which means phase lambda 2)
remote.SaveImageToFile(4, str(path/'phase2.tif'));
remote.SaveImageFloatToFile(2, str(path/'intensity2.bin'), True);
remote.SaveImageFloatToFile(4, str(path/'phase2.bin'), True);

#//Gets the current reconstruction distance
recDist = remote.GetRecDistCM();
#//Set a new reconstruction distance
remote.SetRecDistCM(recDist * 1.1);
#Do a reconstruction with this new distance
remote.OnDistanceChange();

#//Get phase image for computation
phase = remote.GetPhase32fImage();
#plot phase numpy 
plt.imshow(phase,cmap="gray")

#//Extract a profile
remote.SetPhaseProfileState(True)
remote.ExtractPhaseProfile(100, 100, 200, 200)
#Get a profile
profile = remote.GetPhaseProfile()
#Get xy values to plot calibrated profile
distance = np.arange(remote.GetPhaseProfileLength()) * remote.GetPxSizeUm()
plt.figure()
plt.plot(distance,profile)
plt.xlabel('dist [um]')
plt.ylabel('OPL [nm]')
plt.show()

#//Reset phase correction segemnts
remote.ResetCorrSegment();
#Add new phase profile correction
remote.AddCorrSegment(100, 100, 500, 1);
remote.AddCorrSegment(200, 200, 600, 0);
#//Compute 1D phase correction using tilt method
remote.ComputePhaseCorrection(0, 1);

#Logout
remote.Logout()