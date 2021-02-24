'''
Created on Feb 1, 2021

@author: Behnam Abaie
'''

#import xml.etree.cElementTree as ET

from lxml import etree as ET


#################################
######## main settings ##########
#################################
listCh = [['DAPI','0.03'],['A488','1.0'],['Cy3','1.0'],['Cy5','1.0'],['A750','1.0']]
Nz = 81
zstep = 0.150
oversampling = "100"
valve_loop = False


flat_listCh = []
for sublist in listCh:
    for item in sublist:
        flat_listCh.append(item)
N_ch = int(len(flat_listCh)/2)

#################################
######## offset values ##########
#################################
z0 = -(Nz-1)/2*zstep
offset = ''
for ii in range(Nz):
    tempstr = str(format(float(ii*zstep+z0),'.3f'))+','
    offset = offset + tempstr*N_ch

#################################
######## config settings ########
#################################
root = ET.Element("config")

comment = ET.Comment(' The starting directory. ')
root.insert(1, comment)
directory = ET.SubElement(root,'directory',type='directory')
directory.text = 'C:/Data/'

comment = ET.Comment(' The setup name ')
root.insert(2, comment)
setup_name = ET.SubElement(root,'setup_name',type='string')
setup_name.text = 'MERFISH'

comment = ET.Comment(' The ui type, this is "classic" or "detached" ')
root.insert(4, comment)
ui_type = ET.SubElement(root,'ui_type',type='string')
ui_type.text = 'classic'

comment = ET.Comment(' This has two effects: (1) If this is True any exception will immediately crash HAL, which can be useful for debugging. If it is False then some exceptions will be handled by the modules.(2) If it is False we also don''t check whether messages are valid. ')
root.insert(6, comment)
strict = ET.SubElement(root,'strict',type='boolean')
strict.text = 'True'

comment = ET.Comment(' Define the modules to use for this setup. ')
root.insert(8, comment)
modules = ET.SubElement(root,'modules')

mlist = [['hal',['string','storm_control.hal4000.hal4000'],['string','HalController'],[False]],
         ['display',['string','storm_control.hal4000.display.display'],['string','Display'],[[True,'colortable','string','idl5.ctbl','','']]],
         ['feeds',['string','storm_control.hal4000.feeds.feeds'],['string','Feeds'],[False]],
         ['film',['string','storm_control.hal4000.film.film'],['string','Film'],[[True,'extension','string','',',Red,Green,Blue','Movie file name extension']]],
         ['mosaic',['string','storm_control.hal4000.mosaic.mosaic'],['string','Mosaic'],[[True,'flip_horizontal','boolean','False','','Flip image horizontal (mosaic)'],[True,'flip_vertical','boolean','False','','Flip image vertical (mosaic)'],[True,'transpose','boolean','False','','Transpose image vertical (mosaic)'],[True,'objective','string','obj1','obj1,obj2,obj3','Current objective'],[True,'obj1','custom','100x,0.06,0.0,0.0','','Objective 1']]],
         ['settings',['string','storm_control.hal4000.settings.settings'],['string','Settings'],[False]],
         ['timing',['string','storm_control.hal4000.timing.timing'],['string','Timing'],[[True,'time_base','string','camera1','','']]],
         ['none_irlaser',['string','storm_control.sc_hardware.none.noneIRLaserModule'],['string','NoneIRLaserModule'],[False]]
         ]

for ii in range(len(mlist)):
    tempM = ET.SubElement(modules,mlist[ii][0])
    
    tempM_name = ET.SubElement(tempM,'module_name',type=mlist[ii][1][0])
    tempM_name.text = mlist[ii][1][1]
    tempC_name = ET.SubElement(tempM,'class_name',type=mlist[ii][2][0])
    tempC_name.text = mlist[ii][2][1]
    for jj in range(len(mlist[ii][3])):
        if mlist[ii][3][jj]:
            if jj == 0:
                parameters = ET.SubElement(tempM,'parameters')
            tempP = ET.SubElement(parameters,mlist[ii][3][jj][1],type=mlist[ii][3][jj][2],values=mlist[ii][3][jj][4],desc=mlist[ii][3][jj][5])
            tempP.text = mlist[ii][3][jj][3]

#################################
####### camera settings #########
#################################            
camera1 = ET.SubElement(modules,'camera1')      
module_name = ET.SubElement(camera1,'module_name',type='string')
module_name.text = 'storm_control.hal4000.camera.camera'
class_name = ET.SubElement(camera1,'class_name',type='string')
class_name.text = 'Camera'  
camera = ET.SubElement(camera1,'camera')
master = ET.SubElement(camera,'master',type='boolean')
master.text = 'True'  
module_name = ET.SubElement(camera,'module_name',type='string')
module_name.text = 'storm_control.hal4000.camera.photometricsCameraControl'
class_name = ET.SubElement(camera,'class_name',type='string')
class_name.text = 'PhotometricsCameraControl'   
parameters = ET.SubElement(camera,'parameters')
pvcam_sdk = ET.SubElement(parameters,'pvcam_sdk',type='string')
pvcam_sdk.text = 'C:/Windows/System32/pvcam64.dll'
camera_name = ET.SubElement(parameters,'camera_name',type='string')
camera_name.text = 'PMPCIECam00'
default_max = ET.SubElement(parameters,'default_max',type='int')
default_max.text = '150'
default_min  = ET.SubElement(parameters,'default_min',type='int')
default_min .text = '100'
flip_horizontal  = ET.SubElement(parameters,'flip_horizontal',type='boolean')
flip_horizontal.text = 'False'
flip_vertical  = ET.SubElement(parameters,'flip_vertical',type='boolean')
flip_vertical.text = 'False'
transpose = ET.SubElement(parameters,'transpose',type='boolean')
transpose.text = 'False'
extension = ET.SubElement(parameters,'extension',type='string')
saved = ET.SubElement(parameters,'saved',type='boolean')
saved.text = 'True'

#################################
####### DAQ settings #########
#################################            
daq = ET.SubElement(modules,'daq')      
module_name = ET.SubElement(daq,'module_name',type='string')
module_name.text = 'storm_control.sc_hardware.nationalInstruments.nidaqModule'
class_name = ET.SubElement(daq,'class_name',type='string')
class_name.text = 'NidaqModule'  
configuration = ET.SubElement(daq,'configuration')  
timing = ET.SubElement(configuration,'timing')
camera_fire_pin = ET.SubElement(timing,'camera_fire_pin',type='string')
camera_fire_pin.text = '/Dev1/PFI8'
counter = ET.SubElement(timing,'counter',type='string')
counter.text = '/Dev1/ctr0'
counter_out = ET.SubElement(timing,'counter_out',type='string')
counter_out.text = '/Dev1/PFI12'

listI = [['ilm400','/Dev1/ao0','/Dev1/port0/line0'],['ilm470','/Dev1/ao1','/Dev1/port0/line1'],['ilm545','/Dev1/ao2','/Dev1/port0/line8'],['ilm630','/Dev2/ao0','/Dev2/port0/line0'],['ilm730','/Dev2/ao1','/Dev2/port0/line1']]
 
for ii in range(N_ch):
    illumination = ET.SubElement(configuration,listI[ii][0])
    ao_task = ET.SubElement(illumination,'ao_task')
    source = ET.SubElement(ao_task,'source',type='string')
    source.text = listI[ii][1]
    do_task = ET.SubElement(illumination,'do_task')
    source = ET.SubElement(do_task,'source',type='string')
    source.text = listI[ii][2]

mcl = ET.SubElement(configuration,'mcl')
ao_task = ET.SubElement(mcl,'ao_task')
source = ET.SubElement(ao_task,'source',type='string')
source.text = '/Dev1/ao3'

#################################
##### Focus lock settings #######
#################################
focuslock = ET.SubElement(modules,'focuslock')      
module_name = ET.SubElement(focuslock,'module_name',type='string')
module_name.text = 'storm_control.hal4000.focusLock.focusLock'
class_name = ET.SubElement(focuslock,'class_name',type='string')
class_name.text = 'FocusLock'  
configuration = ET.SubElement(focuslock,'configuration')
ir_laser  = ET.SubElement(configuration,'ir_laser',type='string')
ir_laser.text = 'none_irlaser'
ir_power  = ET.SubElement(configuration,'ir_power',type='int')
ir_power.text = '10'
lock_modes  = ET.SubElement(configuration,'lock_modes',type='string')
lock_modes.text = 'NoLockMode,AutoLockMode,AlwaysOnLockMode,OptimalLockMode,CalibrationLockMode,HardwareZScanLockMode'
qpd  = ET.SubElement(configuration,'qpd',type='string')
qpd.text = 'none_qpd'
z_stage  = ET.SubElement(configuration,'z_stage',type='string')
z_stage.text = 'mcl_zstage'

parameters = ET.SubElement(configuration,'parameters')
find_sum = ET.SubElement(parameters,'find_sum')
step_size  = ET.SubElement(find_sum,'step_size',type='float')
step_size.text = '1.0'

locked = ET.SubElement(parameters,'locked')
buffer_length  = ET.SubElement(locked,'buffer_length',type='int')
buffer_length.text = '5'
offset_threshold  = ET.SubElement(locked,'offset_threshold',type='float')
offset_threshold.text = '50.0'

scan = ET.SubElement(parameters,'scan')
scan_step = ET.SubElement(scan,'scan_step',type='float')
scan_step.text = '1.0'
offset_threshold = ET.SubElement(scan,'offset_threshold',type='float')
offset_threshold.text = '10000.0'

hardware_z_scan = ET.SubElement(parameters,'hardware_z_scan')
z_offsets = ET.SubElement(hardware_z_scan,'z_offsets')
z_offsets.text = offset[:-1]

jump_size = ET.SubElement(parameters,'jump_size',type='float')
jump_size.text = '0.1'

#################################
#### Illumination settings ######
#################################
illumination = ET.SubElement(modules,'illumination')      
module_name = ET.SubElement(illumination,'module_name',type='string')
module_name.text = 'storm_control.hal4000.illumination.illumination'
class_name = ET.SubElement(illumination,'class_name',type='string')
class_name.text = 'Illumination'  
configuration = ET.SubElement(illumination,'configuration')

listCh_config = [['400','0,0,139','daq.ilm400.ao_task','4.9','0.0','daq.ilm400.do_task'],
                 ['470','0,0,255','daq.ilm470.ao_task','4.9','0.0','daq.ilm470.do_task'],
                 ['545','127,255,0','daq.ilm545.ao_task','4.9','0.0','daq.ilm545.do_task'],
                 ['630','255,48,48','daq.ilm630.ao_task','4.9','0.0','daq.ilm630.do_task'],
                 ['730','139,26,26','daq.ilm730.ao_task','4.9','0.0','daq.ilm730.do_task']]
for ii in range(N_ch):
    ch = ET.SubElement(configuration,'ch'+str(ii+1))
    gui_name = ET.SubElement(ch,'gui_name',type='string')
    gui_name.text = listCh_config[ii][0]
    color = ET.SubElement(ch,'color',type='string')
    color.text = listCh_config[ii][1]
    analog_modulation = ET.SubElement(ch,'analog_modulation')
    hw_fn_name = ET.SubElement(analog_modulation,'hw_fn_name',type='string')
    hw_fn_name.text = listCh_config[ii][2]
    max_voltage = ET.SubElement(analog_modulation,'max_voltage',type='float')
    max_voltage.text = listCh_config[ii][3]
    min_voltage = ET.SubElement(analog_modulation,'min_voltage',type='float')
    min_voltage.text = listCh_config[ii][4]
    
    digital_modulation = ET.SubElement(ch,'digital_modulation')
    hw_fn_name = ET.SubElement(digital_modulation,'hw_fn_name',type='string')
    hw_fn_name.text = listCh_config[ii][5]


#################################
###### none qpd settings ########
#################################
none_qpd = ET.SubElement(modules,'none_qpd')      
module_name = ET.SubElement(none_qpd,'module_name',type='string')
module_name.text = 'storm_control.sc_hardware.none.noneQPDModule'
class_name = ET.SubElement(none_qpd,'class_name',type='string')
class_name.text = 'NoneQPDModule'  
configuration = ET.SubElement(none_qpd,'configuration')

parameters = ET.SubElement(configuration,'parameters')
max_voltage = ET.SubElement(parameters,'max_voltage',type='float')
max_voltage.text = '10.0'
min_voltage = ET.SubElement(parameters,'min_voltage',type='float')
min_voltage.text = '-10.0'
offset_has_center_bar = ET.SubElement(parameters,'offset_has_center_bar',type='boolean')
offset_has_center_bar.text = 'True'
offset_maximum = ET.SubElement(parameters,'offset_maximum',type='float')
offset_maximum.text = '0.6'
offset_minimum = ET.SubElement(parameters,'offset_minimum',type='float')
offset_minimum.text = '-0.6'
offset_warning_high = ET.SubElement(parameters,'offset_warning_high',type='float')
offset_warning_high.text = '0.5'
offset_warning_low = ET.SubElement(parameters,'offset_warning_low',type='float')
offset_warning_low.text = '-0.5'
sum_maximum = ET.SubElement(parameters,'sum_maximum',type='float')
sum_maximum.text = '1000.0'
sum_minimum = ET.SubElement(parameters,'sum_minimum',type='float')
sum_minimum.text = '0.0'
sum_warning_low = ET.SubElement(parameters,'sum_warning_low',type='float')
sum_warning_low.text = '100.0'

units_to_microns = ET.SubElement(configuration,'units_to_microns',type='float')
units_to_microns.text = '1.0'

noise = ET.SubElement(configuration,'noise',type='float')
noise.text = '0e-2'

tilt = ET.SubElement(configuration,'tilt',type='float')
tilt.text = '0e-3'

z_stage_fn = ET.SubElement(configuration,'z_stage_fn',type='string')
z_stage_fn.text = 'mcl_zstage'

#################################
#### Thorlabs UC480 camera ######
#################################
uc480_camera = ET.SubElement(modules,'uc480_camera')      
module_name = ET.SubElement(uc480_camera,'module_name',type='string')
module_name.text = 'storm_control.sc_hardware.thorlabs.uc480CameraModule'
class_name = ET.SubElement(uc480_camera,'class_name',type='string')
class_name.text = 'UC480Camera'  
configuration = ET.SubElement(uc480_camera,'configuration')

parameters = ET.SubElement(configuration,'parameters')
offset_has_center_bar = ET.SubElement(parameters,'offset_has_center_bar',type='boolean')
offset_has_center_bar.text = 'True'
offset_maximum = ET.SubElement(parameters,'offset_maximum',type='float')
offset_maximum.text = '100.0'
offset_minimum = ET.SubElement(parameters,'offset_minimum',type='float')
offset_minimum.text = '-100.0'
offset_warning_high = ET.SubElement(parameters,'offset_warning_high',type='float')
offset_warning_high.text = '80.0'
offset_warning_low = ET.SubElement(parameters,'offset_warning_low',type='float')
offset_warning_low.text = '-80.0'
sum_maximum = ET.SubElement(parameters,'sum_maximum',type='float')
sum_maximum.text = '230000.0'
sum_minimum = ET.SubElement(parameters,'sum_minimum',type='float')
sum_minimum.text = '50.0'
sum_warning_low = ET.SubElement(parameters,'sum_warning_low',type='float')
sum_warning_low.text = '125000.0'

units_to_microns = ET.SubElement(configuration,'units_to_microns',type='float')
units_to_microns.text = '0.025'

background = ET.SubElement(configuration,'background',type='int')
background.text = '100000'

camera_id = ET.SubElement(configuration,'camera_id',type='int')
camera_id.text = '1'

ini_file = ET.SubElement(configuration,'ini_file',type='string')
ini_file.text = 'uc480_settings.ini'

offset_file = ET.SubElement(configuration,'offset_file',type='string')
offset_file.text = "C:/Users/MERFISH/Documents/GitHub/storm-control/storm_control/hal4000/cam_offsets_storm5.txt"

sigma = ET.SubElement(configuration,'sigma',type='float')
sigma.text = '2.0'

uc480_dll = ET.SubElement(configuration,'uc480_dll',type='string')
uc480_dll.text = 'c:/windows/system32/uc480_64.dll'

use_correlation = ET.SubElement(configuration,'use_correlation',type='boolean')
use_correlation.text = 'True'

allow_single_fits = ET.SubElement(configuration,'allow_single_fits',type='boolean')
allow_single_fits.text = 'False'

x_width = ET.SubElement(configuration,'x_width',type='int')
x_width.text = '700'

y_width = ET.SubElement(configuration,'y_width',type='int')
y_width.text = '100'


#################################
########## PI Stage #############
#################################
pi_stage = ET.SubElement(modules,'pi_stage')      
module_name = ET.SubElement(pi_stage,'module_name',type='string')
module_name.text = 'storm_control.sc_hardware.physikInstrumente.piC867Module2'
class_name = ET.SubElement(pi_stage,'class_name',type='string')
class_name.text = 'PiStageModule'  
configuration = ET.SubElement(pi_stage,'configuration')
serialnum1 = ET.SubElement(configuration,'serialnum1',type='int')
serialnum1.text = '0109029920'
serialnum2 = ET.SubElement(configuration,'serialnum2',type='int')
serialnum2.text = '0109029922'
devices = ET.SubElement(configuration,'devices')
xy_stage = ET.SubElement(devices,'xy_stage')
velocity = ET.SubElement(xy_stage,'velocity',type='float')
velocity.text = '400.0'


#################################
########## mcl z Stage ##########
#################################
mcl_zstage = ET.SubElement(modules,'mcl_zstage')      
module_name = ET.SubElement(mcl_zstage,'module_name',type='string')
module_name.text = 'storm_control.sc_hardware.ludl.ludlVoltageZModule'
class_name = ET.SubElement(mcl_zstage,'class_name',type='string')
class_name.text = 'LudlVoltageZ'  
configuration = ET.SubElement(mcl_zstage,'configuration')

parameters = ET.SubElement(configuration,'parameters')
center = ET.SubElement(parameters,'center',type='float')
center.text = '150.0' 
has_center_bar = ET.SubElement(parameters,'has_center_bar',type='boolean')
has_center_bar.text = 'True' 
maximum = ET.SubElement(parameters,'maximum',type='float')
maximum.text = '300.0'
minimum = ET.SubElement(parameters,'minimum',type='float')
minimum.text = '0.0'
warning_high = ET.SubElement(parameters,'warning_high',type='float')
warning_high.text = '280.0'
warning_low = ET.SubElement(parameters,'warning_low',type='float')
warning_low.text = '20.0'

ao_fn_name = ET.SubElement(configuration,'ao_fn_name',type='string')
ao_fn_name.text = 'daq.mcl.ao_task'

microns_to_volts = ET.SubElement(configuration,'microns_to_volts',type='float')
microns_to_volts.text = '0.0333333'

invert_signal = ET.SubElement(configuration,'invert_signal',type='boolean')
invert_signal.text = 'False'

#################################
########## progressions #########
#################################
progressions = ET.SubElement(modules,'progressions')      
module_name = ET.SubElement(progressions,'module_name',type='string')
module_name.text = 'storm_control.hal4000.progressions.progressions'
class_name = ET.SubElement(progressions,'class_name',type='string')
class_name.text = 'Progressions'  
configuration = ET.SubElement(progressions,'configuration')

illumination_functionality = ET.SubElement(configuration,'illumination_functionality',type='string')
illumination_functionality.text = 'illumination'

frames = ET.SubElement(configuration,'frames',type='int')
frames.text = '100'

increment = ET.SubElement(configuration,'increment',type='float')
increment.text = '0.01'

starting_value = ET.SubElement(configuration,'starting_value',type='float')
starting_value.text = '0.1'

#################################
########## spotcounter ##########
#################################
spotcounter = ET.SubElement(modules,'spotcounter')      
module_name = ET.SubElement(spotcounter,'module_name',type='string')
module_name.text = 'storm_control.hal4000.spotCounter.spotCounter'
class_name = ET.SubElement(spotcounter,'class_name',type='string')
class_name.text = 'SpotCounter'  

configuration = ET.SubElement(spotcounter,'configuration')

max_threads = ET.SubElement(configuration,'max_threads',type='int')
max_threads.text = '4'

max_size = ET.SubElement(configuration,'max_size',type='int')
max_size.text = '263000'

#################################
############# stage #############
#################################
stage = ET.SubElement(modules,'stage')      
module_name = ET.SubElement(stage,'module_name',type='string')
module_name.text = 'storm_control.hal4000.stage.stage'
class_name = ET.SubElement(stage,'class_name',type='string')
class_name.text = 'Stage'  

configuration = ET.SubElement(stage,'configuration')

stage_functionality = ET.SubElement(configuration,'stage_functionality',type='string')
stage_functionality.text = 'pi_stage'

#################################
############# TCP/IP ############
#################################
tcp_control = ET.SubElement(modules,'tcp_control')      
module_name = ET.SubElement(tcp_control,'module_name',type='string')
module_name.text = 'storm_control.hal4000.tcpControl.tcpControl'
class_name = ET.SubElement(tcp_control,'class_name',type='string')
class_name.text = 'TCPControl'  

configuration = ET.SubElement(tcp_control,'configuration')

parallel_mode = ET.SubElement(configuration,'parallel_mode',type='boolean')
parallel_mode.text = 'True'

tcp_port = ET.SubElement(configuration,'tcp_port',type='int')
tcp_port.text = '9000'

#################################
########## output config ########
#################################
tree = ET.ElementTree(root)
tree.write('C:/Users/MERFISH/Documents/GitHub/storm-control/storm_control/hal4000/xml/HZScan_config.xml',pretty_print = True)


#################################
############ shutter ############
#################################
root = ET.Element("repeat")
frames = ET.SubElement(root, "frames")
frames.text = str(N_ch*Nz)
frames = ET.SubElement(root, "oversampling")
frames.text = oversampling

for ii in range(Nz):
    if 'DAPI' in flat_listCh:
        event = ET.SubElement(root, "event")
        ET.SubElement(event, "channel").text = "0"
        ET.SubElement(event, "power").text = listCh[0][1]
        ET.SubElement(event, "on").text = str(float(0+ii*N_ch))
        ET.SubElement(event, "off").text = str(float(0.95+ii*N_ch))
        ET.SubElement(event, "color").text = "0,0,139"
    
    if 'A488' in flat_listCh:
        event = ET.SubElement(root, "event")
        ET.SubElement(event, "channel").text = "1"
        ET.SubElement(event, "power").text = listCh[1][1]
        ET.SubElement(event, "on").text = str(float(1+ii*N_ch))
        ET.SubElement(event, "off").text = str(float(1.95+ii*N_ch))
        ET.SubElement(event, "color").text = "0,0,255"
    
    if 'Cy3' in flat_listCh:
        event = ET.SubElement(root, "event")
        ET.SubElement(event, "channel").text = "2"
        ET.SubElement(event, "power").text = listCh[2][1]
        ET.SubElement(event, "on").text = str(float(2+ii*N_ch))
        ET.SubElement(event, "off").text = str(float(2.95+ii*N_ch))
        ET.SubElement(event, "color").text = "127,255,0"
    
    if 'Cy5' in flat_listCh:
        event = ET.SubElement(root, "event")
        ET.SubElement(event, "channel").text = "3"
        ET.SubElement(event, "power").text = listCh[3][1]
        ET.SubElement(event, "on").text = str(float(3+ii*N_ch))
        ET.SubElement(event, "off").text = str(float(3.95+ii*N_ch))
        ET.SubElement(event, "color").text = "255,48,48"
        
    if 'A750' in flat_listCh:
        event = ET.SubElement(root, "event")
        ET.SubElement(event, "channel").text = "4"
        ET.SubElement(event, "power").text = listCh[4][1]
        ET.SubElement(event, "on").text = str(float(4+ii*N_ch))
        ET.SubElement(event, "off").text = str(float(4.95+ii*N_ch))
        ET.SubElement(event, "color").text = "139,26,26"

#################################
######### output shutter ########
#################################

tree = ET.ElementTree(root)
tree.write('C:/Users/MERFISH/Documents/GitHub/storm-control/storm_control/hal4000/shutters_default.xml',pretty_print = True)


#################################
########### dave XML ############
#################################
root = ET.Element("recipe")
command_sequence = ET.SubElement(root,'command_sequence')      
loop = ET.SubElement(command_sequence,'loop',name='Valve Loop')

if valve_loop:
    variable_entry = ET.SubElement(loop,'variable_entry',name='Valve Loop')
    
loop = ET.SubElement(loop,'loop',name='Movie Loop',increment="name")
item = ET.SubElement(loop,'item',name='Movie 1')

item = ET.SubElement(root,'item',name='Movie 1')
movie = ET.SubElement(item,'movie')
name = ET.SubElement(movie,'name',increment='Yes')
name.text = 'Tile'
length = ET.SubElement(movie,'length')
length.text = str(N_ch*Nz)
variable_entry = ET.SubElement(movie,'variable_entry',name='Movie Loop')
 
loop_variable = ET.SubElement(root,'loop_variable',name='Valve Loop')
valve = ET.SubElement(loop_variable,'valve')
valve_protocol = ET.SubElement(valve,'valve_protocol')
valve_protocol.text = 'Hybridize 12'

loop_variable = ET.SubElement(root,'loop_variable',name='Movie Loop')
file_path = ET.SubElement(loop_variable,'file_path')

#################################
######## output dave XML ########
#################################

tree = ET.ElementTree(root)
tree.write('C:/Users/MERFISH/Documents/GitHub/storm-control/storm_control/dave/xml_generators/example_recipe_request_positions_MyVersion.xml',pretty_print = True)





