'''
Created on Aug 22, 2020

@author: MERFISH
'''

nn = 81
zstep = 0.150

z0 = -(nn-1)/2*zstep


f= open("offset.txt","w+")

for ii in range(nn):
    f.write(str(format(float(ii*zstep+z0),'.3f'))+','+str(format(float(ii*zstep+z0),'.3f'))+','+str(format(float(ii*zstep+z0),'.3f'))+',')
     
f.close()