'''
Created on April 15, 2021

@author: Behnam Abaie
'''

import os
from pathlib import Path
from lxml import etree as ET

def settings(listCh,listCh_final,Nch,Nz,zstep,oversampling):
    
    maindir = "C:/Users/MERFISH/Documents/GitHub/storm-control/storm_control/hal4000/"
    for ii in range(10):
        fname1 = maindir +'shutters_' + str(ii) + ".xml"
        my_file = Path(fname1)
        if my_file.is_file():
            os.remove(fname1)
        fname2 = maindir +'xml/setting_' + str(ii) + '.xml'
        my_file = Path(fname2)
        if my_file.is_file():
            os.remove(fname2)

    xmlfile = ET.parse('C:/Users/MERFISH/Documents/GitHub/storm-control/storm_control/hal4000/xml/setting_original.xml')
    settings = xmlfile.getroot()

    z0 = -(Nz-1)/2*zstep
    offset = ''
    for ii in range(Nz):
        tempstr = str(format(float(ii*zstep+z0),'.3f'))+','
        offset = offset + tempstr

    focuslock = settings.find('focuslock')
    hardware_z_scan = focuslock.find('hardware_z_scan')
    z_offsets = hardware_z_scan.find('z_offsets')
    z_offsets.text = offset[:-1]


    filter_wheel = settings.find('filter_wheel')
    current_filter = filter_wheel.find('current_filter')
    
    film = settings.find('film')
    filetype = film.find('filetype')
    filetype.text = '.tif'

    illumination = settings.find('illumination')
    default_power = illumination.find('default_power')
    on_off_state = illumination.find('on_off_state')
    power_buttons = illumination.find('power_buttons')
    
    shutters = illumination.find('shutters')

    ch_counter = 0
    for ii in range(len(listCh_final)):
        if listCh_final[ii][2]:
            current_filter.text = listCh_final[ii][0]
            shutters.text = 'C:/Users/MERFISH/Documents/GitHub/storm-control/storm_control/hal4000/shutters_' + str(ch_counter)+'.xml'
            ch_counter = ch_counter + 1
            
            default_power_text = str('1.000,'*Nch)
            default_power.text = bytes(default_power_text[:-1], 'utf-8')
            on_off_state_text = str('False,'*Nch)
            on_off_state.text = bytes(on_off_state_text[:-1], 'utf-8')
            power_buttons_text = str([[['Max', 1.0], ['Low', 0.1]]]*Nch)
            power_buttons.text = bytes(power_buttons_text, 'utf-8')
            
            tree = ET.ElementTree(settings)
            tree.write('C:/Users/MERFISH/Documents/GitHub/storm-control/storm_control/hal4000/xml/setting_' + str(ch_counter-1)+'.xml',pretty_print = True)

    shutter_counter = 0
    if listCh[0][2]:
        shutter_counter = shutter_counter + 1
        root = ET.Element("repeat")
        frames = ET.SubElement(root, "frames")
        frames.text = str(Nz)
        frames = ET.SubElement(root, "oversampling")
        frames.text = oversampling  
        for ii in range(Nz):
            event = ET.SubElement(root, "event")
            ET.SubElement(event, "channel").text = str(shutter_counter-1)
            ET.SubElement(event, "power").text = "1.0"
            ET.SubElement(event, "on").text = str(float(ii))
            ET.SubElement(event, "off").text = str(float(0.80+ii))
            ET.SubElement(event, "color").text = "0,0,139"
    
        tree = ET.ElementTree(root)
        tree.write('C:/Users/MERFISH/Documents/GitHub/storm-control/storm_control/hal4000/shutters_' + str(shutter_counter-1) + '.xml',pretty_print = True)
    
    if listCh[1][2]:
        shutter_counter = shutter_counter + 1
        root = ET.Element("repeat")
        frames = ET.SubElement(root, "frames")
        frames.text = str(Nz)
        frames = ET.SubElement(root, "oversampling")
        frames.text = oversampling  
        for ii in range(Nz):
            event = ET.SubElement(root, "event")
            ET.SubElement(event, "channel").text = str(shutter_counter-1)
            ET.SubElement(event, "power").text = "1.0"
            ET.SubElement(event, "on").text = str(float(ii))
            ET.SubElement(event, "off").text = str(float(0.95+ii))
            ET.SubElement(event, "color").text = "0,0,255"
    
        tree = ET.ElementTree(root)
        tree.write('C:/Users/MERFISH/Documents/GitHub/storm-control/storm_control/hal4000/shutters_' + str(shutter_counter-1) + '.xml',pretty_print = True)
        
    if listCh[2][2]:
        shutter_counter = shutter_counter + 1
        root = ET.Element("repeat")
        frames = ET.SubElement(root, "frames")
        frames.text = str(Nz)
        frames = ET.SubElement(root, "oversampling")
        frames.text = oversampling  
        for ii in range(Nz):
            event = ET.SubElement(root, "event")
            ET.SubElement(event, "channel").text = str(shutter_counter-1)
            ET.SubElement(event, "power").text = "1.0"
            ET.SubElement(event, "on").text = str(float(ii))
            ET.SubElement(event, "off").text = str(float(0.95+ii))
            ET.SubElement(event, "color").text = "127,255,0"
    
        tree = ET.ElementTree(root)
        tree.write('C:/Users/MERFISH/Documents/GitHub/storm-control/storm_control/hal4000/shutters_' + str(shutter_counter-1) + '.xml',pretty_print = True)
        
    if listCh[3][2]:
        shutter_counter = shutter_counter + 1
        root = ET.Element("repeat")
        frames = ET.SubElement(root, "frames")
        frames.text = str(Nz)
        frames = ET.SubElement(root, "oversampling")
        frames.text = oversampling  
        for ii in range(Nz):
            event = ET.SubElement(root, "event")
            ET.SubElement(event, "channel").text = str(shutter_counter-1)
            ET.SubElement(event, "power").text = "1.0"
            ET.SubElement(event, "on").text = str(float(ii))
            ET.SubElement(event, "off").text = str(float(0.95+ii))
            ET.SubElement(event, "color").text = "255,48,48"
        
        tree = ET.ElementTree(root)
        tree.write('C:/Users/MERFISH/Documents/GitHub/storm-control/storm_control/hal4000/shutters_' + str(shutter_counter-1) + '.xml',pretty_print = True)
        
    if listCh[4][2]:
        shutter_counter = shutter_counter + 1
        root = ET.Element("repeat")
        frames = ET.SubElement(root, "frames")
        frames.text = str(Nz)
        frames = ET.SubElement(root, "oversampling")
        frames.text = oversampling  
        for ii in range(Nz):
            event = ET.SubElement(root, "event")
            ET.SubElement(event, "channel").text = str(shutter_counter-1)
            ET.SubElement(event, "power").text = "1.0"
            ET.SubElement(event, "on").text = str(float(ii))
            ET.SubElement(event, "off").text = str(float(0.95+ii))
            ET.SubElement(event, "color").text = "139,26,26"

        tree = ET.ElementTree(root)
        tree.write('C:/Users/MERFISH/Documents/GitHub/storm-control/storm_control/hal4000/shutters_' + str(shutter_counter-1) + '.xml',pretty_print = True)

