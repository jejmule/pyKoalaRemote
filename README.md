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

## New methods
Two new methods enable a dialog in the console.

 - ConnectAndLoginDialog
	 - Connect and Login to Koala within a single function.
	 - IP address and password are defined in the console
	 - If the user leave empty field, the default value is used
 - OpenConfigDialog

## Modified methods
The methods that returns dotNet Array are modified to return Numpy Array

 - Connect(hostname, quiet=True)
	 - Arguments :
		 - hostName (String): The IP of the computer where Koala is running. Use localhost if running on the same computer
		 - quiet (Boolean): Deprecated parameter, will be removed in a later version. Set either to true or false
	 - Return : true if the connection was successful
	 - Comments : the instance variable username is set with username
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
	 - Return : 1D Numpy array of np.double of profile length

    
> Written with [StackEdit](https://stackedit.io/).
<!--stackedit_data:
eyJoaXN0b3J5IjpbLTEyMTk5NjYyNTcsLTYzNjU5MjE5M119
-->