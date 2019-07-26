# -*- coding: utf-8 -*-
"""
This class enables easy access to Koala TCP/IP remote interface
Prompt dialog for connection and login
Get functions return numpy Array
"""
#import python package
from pyKoalaRemote import remote_utils as ru
import numpy as np
import sys
import clr



#Add required dotNet reference
clr.AddReference("System")
import System
from System import Array

#Class pyRemote to manage dotNet dll in Python
class pyKoalaRemoteClient:
    
    def __init__(self, koala_8 = True):
        self.koala_8 = koala_8
        #create an instance to Koala remote Client. Version 8 and above has a new dll location
        if koala_8 :
            #Add Koala remote librairies to Path
            sys.path.append(r'C:\Program Files\LynceeTec\Koala\Remote\Remote Libraries\x64') #load x86 for 32 bits applications
            #Import KoalaRemoteClient
            clr.AddReference("LynceeTec.KoalaRemote.Client")
            from LynceeTec.KoalaRemote.Client import KoalaRemoteClient
            #Define KoalaRemoteClient host
            self.host=KoalaRemoteClient()
        
        else :
            #Add Koala remote librairies to Path
            sys.path.append(r'C:\Program Files\Koala\Remote Libraries\x64') #load x86 for 32 bits applications
            #Import KoalaRemoteClient
            clr.AddReference("TCPCLient")
            import KoalaClient
            #Define KoalaRemoteClient host
            self.host=KoalaClient.KoalaTCPClient()
        
        #check if host is properly initialized
        try :
            self.host
        except :
            print("class not initialized")
            return
    
    def ConnectAndLoginDialog(self) :
        #Ask for IP adress
        IP = ru.get_input('Enter host IP adress','localhost')
        #Connect to Koala
        if self.Connect(IP):
            print('connected to Koala as',self.username,'on ',IP)
        else:
            print('connection to Koala failed on :',IP)
            print('Check if Koala is started or if the production window is open or if the previous session was closed')
            return False
        
        #ask for username password
        password = ru.get_input('Enter password for '+self.username+' account', self.username)
        #Login with username password
        if self.Login(password) :
            print('Log as ',self.username,)
        else :
            print('Login failed for',self.username,)
            return False
        return True
    
    def Connect(self,hostName,quiet=True):
        self.username = ''
        ret,self.username = self.host.Connect(hostName,self.username,quiet)
        return ret  
            
    def Login(self,password):
        return self.host.Login(password)
    
    def Logout(self) :
        try : self.host.Logout()
        except : 
            print("Logout failed")
            return
        print("Logout succesfull")        
        
    def __del__(self):
        self.Logout()
    
    #Open a configuration using config id
    def OpenConfigDialog(self) :
        #☻get config Id
        config = ru.get_input('Enter configuration number', default='137')
        #open config
        return self.OpenConfig(config)
   
    def OpenConfig(self, configNumber) :
        try : self.host.OpenConfig(configNumber)
        except: 
            print("configuration",configNumber,'do not exists')
            return
        print("Configuration",configNumber,"open")
        #wait for older koala version
        if not self.koala_8 :
            import time
            time.sleep(2) # 2 seconds to wait for OPL to move if DHM was re-init
   
    def updateROI(self) :
        self.roiWidth = self.host.GetPhaseWidth();
        self.roiHeight = self.host.GetPhaseHeight();
        if self.roiWidth % 4 == 0:
            self.roiStride = self.roiWidth
        else : 
            self.roiStride = (int(self.roiWidth / 4) * 4) + 4;
        return int(self.roiStride * self.roiHeight)
    
    def GetAxesPosMu(self) :
        #Define a dotNet (C#) Double Array
        buffer = Array.CreateInstance(System.Double,4)
        self.host.GetAxesPosMu(buffer)
        #copy and return buffer
        return ru.dn2np(buffer)
    
    def GetHoloImage(self) :
        #Define a dotNet (C#) Byte Array
        self.width = self.host.GetHoloWidth();
        self.height = self.host.GetHoloHeight();
        buffer = Array.CreateInstance(System.Byte,self.height*self.width)
        #Get holo from Koala
        self.host.GetHoloImage(buffer)
        #copy, reshape and return buffer
        return np.reshape(ru.dn2np(buffer),(self.height,self.width))
    
    def GetIntensity32fImage(self) :
        self.updateROI()
        #Define a dotNet (C#) Single Array
        buffer = Array.CreateInstance(System.Single,self.roiHeight*self.roiWidth)
        self.host.GetIntensity32fImage(buffer)
        #copy, reshape and return buffer
        return np.reshape(ru.dn2np(buffer),(self.roiHeight,self.roiWidth))
    
    def GetIntensityImage(self) :
        #Define a dotNet (C#) Byte Array
        buffer = Array.CreateInstance(System.Byte,self.updateROI())
        self.host.GetIntensityImage(buffer)
        #copy, reshape and return buffer
        return np.reshape(ru.dn2np(buffer),(self.roiHeight,self.roiStride))[:,0:self.roiWidth]
    
    def GetPhase32fImage(self) :
        self.updateROI()
        #Define a dotNet (C#) Single Array
        buffer = Array.CreateInstance(System.Single,self.roiHeight*self.roiWidth)
        self.host.GetPhase32fImage(buffer)
        #copy, reshape and return buffer
        return np.reshape(ru.dn2np(buffer),(self.roiHeight,self.roiWidth))
    
    def GetPhaseImage(self) :
        #Define a dotNet (C#) Byte Array
        buffer = Array.CreateInstance(System.Byte,self.updateROI())
        self.host.GetPhaseImage(buffer)
        #copy, reshape and return buffer
        return np.reshape(ru.dn2np(buffer),(self.roiHeight,self.roiStride))[:,0:self.roiWidth]
    
    def GetPhaseProfile(self) :
        #Define a dotNet (C#) Double Array
        buffer = Array.CreateInstance(System.Double,self.GetPhaseProfileLength())
        self.host.GetPhaseProfile(buffer)
        #copy and return buffer
        return ru.dn2np(buffer)
    
    def GetPhaseProfileAxis(self):
        return np.arange(self.GetPhaseProfileLength()) * self.GetPxSizeUm()
    
    #wrapper for remote function, direct call
    def AccWDSearch(self,distUM,stepUM):
        return self.host.AccWDSearch(distUM,stepUM)
    
    def Acquisition2L(self):
        return self.host.Acquisition2L()
    
    def AddCorrSegment(self,top,left,length,orientation):
        return self.host.AddCorrSegment(top,left,length,orientation)
    
    def AlgoResetPhaseMask(self):
        return self.host.AlgoResetPhaseMask()
    
    def AxisInstalled(self,axisId):
        return self.host.AxisInstalled(axisId)
    
    def ComputePhaseCorrection(self,fitMethod,degree):
        return self.host.ComputePhaseCorrection(fitMethod,degree)
    
    def DigitizerAcquiring(self):
        return self.host.DigitizerAcquiring()
    
    def ExtractPhaseProfile(self,startX,startY,endX,endY):
        return self.host.ExtractPhaseProfile(startX,startY,endX,endY)
    
    def FastWDSearch(self):
        return self.host.FastWDSearch()
    
    def GetCameraShutterUs(self):
        return self.host.GetCameraShutterUs()
    
    def GetDHMSerial(self):
        return self.host.GetDHMSerial()
    
    def GetHoloContrast(self):
        return self.host.GetHoloContrast()
    
    def GetHoloHeight(self):
        return self.host.GetHoloHeight()
    
    def GetHoloWidth(self):
        return self.host.GetHoloWidth()
    
    def GetLambdaNm(self,srcId,useLogicalId=True):
        return self.host.GetLambdaNm(srcId,useLogicalId)
    
    def GetOPLPos(self):
        return self.host.GetOPLPos()
    
    def GetPhaseHeight(self):
        return self.host.GetPhaseHeight()
    
    def GetPhaseWidth(self):
        return self.host.GetPhaseWidth()
    
    def GetPhaseProfileLength(self):
        return self.host.GetPhaseProfileLength()
    
    def GetPxSizeUm(self):
        return self.host.GetPxSizeUm()
    
    def GetRecDistCM(self):
        return self.host.GetRecDistCM()
    
    def GetUnwrap2DState(self):
        return self.host.GetUnwrap2DState()
    
    def InitXYZStage(self,withProgressBar=False,moveToCenter=False):
        return self.host.InitXYZStage(withProgressBar,moveToCenter)
    
    def KoalaShutDown(self,confirm=False):
        return self.host.KoalaShutDown(confirm)
    
    def LoadHolo(self,path,numLambda):
        return self.host.LoadHolo(path,numLambda)
    
    def MoveAxes(self, absMove, mvX, mvY, mvZ, mvTh, distX, distY, distZ, distTh, accX, accY, accZ, accTh, waitEnd=True):
        return self.host.MoveAxes(absMove, mvX, mvY, mvZ, mvTh, distX, distY, distZ, distTh, accX, accY, accZ, accTh, waitEnd)
    
    def MoveAxesArr(self,axes,absMove,dist,acc,waitEnd=True):
        return self.host.MoveAxesArr(axes,absMove,dist,acc,waitEnd)
    
    def MoveAxis(self, axisId, absMove, distUm, accuracyUM, waitEnd=True):
        return self.host.MoveAxis(axisId, absMove, distUm, accuracyUM, waitEnd)
    
    def MoveOPL(self, position):
        return self.host.MoveOPL(position)
        
    def OnDistanceChange(self):
        return self.host.OnDistanceChange()
    
    def OpenFrmTopography(self):
        return self.host.OpenFrmTopography()
        
    def OpenHoloWin(self):
        return self.host.OpenHoloWin()
    
    def OpenIntensityWin(self, updateXYScale=True):
        return self.host.OpenIntensityWin(updateXYScale)
    
    def OpenPhaseWin(self,withoutColorbar=False,doReconstruction=True,updateXYScale=True):
        return self.host.OpenPhaseWin(withoutColorbar,doReconstruction,updateXYScale)
    
    def OpenStroboFixFrequency(self,numberOfPeriods):
        return self.host.OpenStroboFixFrequency(self,numberOfPeriods)
    
    def RecordStroboFrequencyScan(self):
        return self.host.RecordStroboFrequencyScan(self)
    
    def ResetCorrSegment(self,dimension=1):
        return self.host.ResetCorrSegment(dimension)
    
    def ResetGrab(self):
        return self.host.ResetGrab()
    
    def SaveImageFloatToFile(self, winId, fileName, useBinFormat=False):
        return self.host.SaveImageFloatToFile(winId,fileName,useBinFormat)
    
    def SaveImageToFile(self, winId, fileName):
        return self.host.SaveImageToFile(winId, fileName)
    
    def SelectDisplayWL(self, winId):
        return self.host.SelectDisplayWL(winId)
    
    def SelectTopoZone(self, top, left, width, height):
        return self.host.SelectTopoZone(top, left, width, height)
    
    def SetCameraShutterUs(self, shutterUs):
        return self.host.SetCameraShutterUs(shutterUs)
    
    def SetPhaseProfileState(self, state=False):
        return self.host.SetPhaseProfileState(state)
    
    def SetRecDistCM(self,distCM):
        return self.host.SetRecDistCM(distCM)
    
    def SetSourceState(self, srcId, state, useLogicalId=True):
        return self.host.SetSourceState(srcId, state, useLogicalId)
    
    def SetUnwrap2DMethod(self, method):
        return self.host.SetUnwrap2DMethod(method)
    
    def SetUnwrap2DState(self,state=False):
        return self.host.SetUnwrap2DState(state)
    
    def SingleReconstruction(self):
        return self.host.SingleReconstruction()

#test the class when running this file directly
if __name__ == '__main__' :
    remote = pyKoalaRemoteClient()
    remote.ConnectAndLoginDialog()
    remote.OpenConfigDialog()
    remote.OpenHoloWin()
    remote.OpenIntensityWin()
    remote.OpenPhaseWin()
    remote.Logout()