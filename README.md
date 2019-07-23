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
	 - Return : Array of doubles of size 4, where the data for the X, Y, Z and Theta axis respectively
 - GetHoloImage
	 - Arguments : void (nothing)
	 - Return : Array of U8 of image size

    
> Written with [StackEdit](https://stackedit.io/).
<!--stackedit_data:
eyJoaXN0b3J5IjpbLTE2MjUzOTI5NDUsLTYzNjU5MjE5M119
-->