# pyKoalaRemote
Python wrapper for dotNet Koala Remote Client provided by LyncéeTec to control Digital Holographique Microscope using proprietary Koala software

The wrapper uses the same methods names and arguments as the dotNet library distributed by LyncéeTec SA LynceeTec.KoalaRemote.Client.dll .
The methods that return a dotNet Array are modified to return a Numpy Array, modified methods are described bellow.

## Installation using pip

    pip install pyKoalaRemote
    
## Usage
Import the class client from the pyKoalaRemote and create an instance

    from  pyKoalaRemote import client
    remote = client.pyKoalaRemoteClient()
 
Run standard methods

    remote.Connect("localhost")
    remote.Login("password")
    remote.OpenConfig(137)

## Modified methods
The methods that returns dotNet Array are modified to return Numpy Array

 - GetAxesPosMu
	 - Arguments : void (nothing)
	 - Return : 1D Numpy array of np.double of size 4, where the data for the X, Y, Z and Theta axis respectively
 - GetHoloImage
	 - Arguments : void (nothing)
	 - Return : 2D Numpy array of np.ubyte of hologram size
 - GetIntensityImage
	 - Arguments : void (nothing)
	 - Return : 2D Numpy array of np.ubyte of ROI size
 - GetIntensity32fImage
	 - Arguments : void (nothing)
	 - Return : 2D Numpy array of np.single of ROI size
 - GetPhaseImage
	 - Arguments : void (nothing)
	 - Return : 2D Numpy array of np.ubyte of ROI size
 - GetPhase32fImage
	 - Arguments : void (nothing)
	 - Return : 2D Numpy array of np.single of ROI size
 - GetPhaseProfile
	 - Arguments : void (nothing)
	 - Return : 1D Numpy array of np.double of profile l

    
> Written with [StackEdit](https://stackedit.io/).
<!--stackedit_data:
eyJoaXN0b3J5IjpbMTA3ODkzMjkwMywtNjM2NTkyMTkzXX0=
-->