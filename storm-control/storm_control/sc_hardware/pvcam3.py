import sys
sys.path.append(r'C:\Users\MERFISH\Documents\GitHub\PyVCAM\pyvcam_wrapper\src\pyvcam')


#!/usr/bin/env python
"""
A ctypes based interface to the Photometrics PVCAM library.

Hazen 10/17
"""
import ctypes
import numpy
import sys

import storm_control.sc_library.halExceptions as halExceptions
from pyvcam import pvc
from pyvcam.camera import Camera as PYVcam

pvcam = None

def check(value, fn_name = "??"):
    """
    Wrap all calls to pvcam with this to get any error messages.
    """
    if (value == 0):

        # Get the error message from the PVCAM library.
        error_msg = ctypes.c_char_p((' ' * pvc.ERROR_MSG_LEN).encode())
        pvcam.pl_error_message(pvcam.pl_error_code(), error_msg)

        # Compose error message.
        error_message = fn_name + " failed with message: " + error_msg.value.decode()

        # Raise exception.
        raise PVCAMException(error_message)
        
        return False
    else:
        return True

def getCameraNames():
    """
    Return a list of all the available cameras.
    """
    # Query to get the total number of cameras.
    n_cams = pvc.get_cam_total()

    ## Query the camera names.
    camera_names = []
    for i in range(n_cams):
        camera_names.append(pvc.get_cam_name(i))

    return camera_names

def initPVCAM():
    """
    Initialize the library.
    """
    pvc.init_pvcam()
    
def loadPVCAMDLL(pvcam_library_name):
    """
    Load the pvcam DLL.
    """
    global pvcam
    if pvcam is None:
        pvcam = ctypes.WinDLL(pvcam_library_name)
        
def uninitPVCAM():
    """
    Closes the library.
    """
    pvc.uninit_pvcam()
    
class PVCAMException(halExceptions.HardwareException):
    pass

class PVCAMCamera(object):
    """
    Python interface to a PVCAM camera.

    The basic idea is that we are going to keep track of how many frames the
    camera has acquired using an EOF callback. Then when HAL polls with getFrames()
    we'll return all the frames that have been acquired since the last polling.
    """
    def __init__(self, camera_name = None, **kwds):
        super().__init__(**kwds)

        self.buffer_len = None
        self.data_buffer = None
        self.frame_bytes = None
        self.frame_x = None
        self.frame_y = None
        #self.n_captured = pvc.uns32(0) # No more than 4 billion frames in a single capture..
        self.n_processed = 0

        # Open camera.
        c_name = getCameraNames()[0]
        self.hcam = pvc.get_cam_total()
        print(c_name)
        pvc.open_camera(c_name)

        # Register our EOF callback. This callback is supposed to increment
        # self.n_captured every time the camera acquires a new frame.
        #

















#initPVCAM()
test = loadPVCAMDLL('C:/Windows/System32/pvcam64.dll')
initPVCAM()
print(getCameraNames())
PVCAMCamera()


