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
 
Then you can run standard methods

    remote.Connect("localhost")
    remote.Login("password")
    remote.OpenConfig(137)

## Modified methods

    
> Written with [StackEdit](https://stackedit.io/).
<!--stackedit_data:
eyJoaXN0b3J5IjpbLTYzNjU5MjE5M119
-->