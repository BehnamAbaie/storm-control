'''
Created on May 16, 2020

@author: Behnam Abaie
'''

import xml.etree.cElementTree as ET

Nz = 81

root = ET.Element("repeat")
frames = ET.SubElement(root, "frames")
frames.text = str(3*81)
frames = ET.SubElement(root, "oversampling")
frames.text = "100"

for ii in range(Nz):
    event = ET.SubElement(root, "event")
    ET.SubElement(event, "channel").text = "0"
    ET.SubElement(event, "power").text = "1.0"
    ET.SubElement(event, "on").text = str(float(0+ii*3))
    ET.SubElement(event, "off").text = str(float(0.95+ii*3))
    ET.SubElement(event, "color").text = "255,0,255"
    
    event = ET.SubElement(root, "event")
    ET.SubElement(event, "channel").text = "1"
    ET.SubElement(event, "power").text = "1.0"
    ET.SubElement(event, "on").text = str(float(1+ii*3))
    ET.SubElement(event, "off").text = str(float(1.95+ii*3))
    ET.SubElement(event, "color").text = "0,255,255"
    
    event = ET.SubElement(root, "event")
    ET.SubElement(event, "channel").text = "2"
    ET.SubElement(event, "power").text = "1.0"
    ET.SubElement(event, "on").text = str(float(2+ii*3))
    ET.SubElement(event, "off").text = str(float(2.95+ii*3))
    ET.SubElement(event, "color").text = "255,255,0"
    
    #event = ET.SubElement(root, "event")
    #ET.SubElement(event, "channel").text = "3"
    #ET.SubElement(event, "power").text = "1.0"
    #ET.SubElement(event, "on").text = str(float(3+ii*4))
    #ET.SubElement(event, "off").text = str(float(4+ii*4))
    #ET.SubElement(event, "color").text = "255,255,0"

tree = ET.ElementTree(root)
tree.write('shutters_default.xml')