# -*- coding: utf-8 -*-
import ctypes
import clr
import numpy as np

clr.AddReference("System.Runtime")
clr.AddReference("System.Runtime.InteropServices")
from System.Runtime.InteropServices import GCHandle, GCHandleType

#get input form console, if input is empty us default value
def get_input(question,default) :
    answer = input(question+'['+default+'] :')
    return answer or default

#fonction dn2cp : copy dotNet array to Numpy array directly from memory
def dn2np(src) :
    #Arg src : the source dotNEt source Array
    #Retrun dest : the copy of src into a numpy array
    
    #Get GCHandle to handle managed memory with non-managed code
    src_hndl = GCHandle.Alloc(src, GCHandleType.Pinned)
    
    #Get numpy type from dotNet Array
    array_type = src.GetType()
    if array_type.ToString() == "System.Byte[]" :
        ctype = ctypes.c_ubyte
    elif array_type.ToString() == "System.Single[]" :
        ctype = ctypes.c_float
    elif array_type.ToString() == "System.Double[]" :
        ctype = ctypes.c_double
    else:
        print("Array type",array_type.ToString(),"does not match with numpy type")
        return
    
    try:
        #Get pointer to source
        src_ptr = src_hndl.AddrOfPinnedObject().ToInt64()
        bufType = ctype*len(src)
        #Copy src to dst
        cbuf = bufType.from_address(src_ptr)
        dest = np.frombuffer(cbuf, dtype=cbuf._type_)
    finally:
        #Allow the garbage collector to free managed memory
        if src_hndl.IsAllocated: src_hndl.Free()
    return dest