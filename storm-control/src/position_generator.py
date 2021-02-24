'''
Created on Aug 22, 2020

@author: MERFISH
'''

nx = 5
ny = 5

xstep = 125.0
ystep = 125.0

xc = 12500.0
yc = 12500.0

x0 = xc - (nx-1)/2.0*xstep
y0 = yc - (ny-1)/2.0*ystep


f= open("positions1.txt","w+")

for ii in range(nx):
    for jj in range(ny):
        f.write(str(format(float(ii*xstep+x0),'.3f'))+', '+str(format(float(jj*ystep+y0),'.3f'))+'\n')
     
f.close()