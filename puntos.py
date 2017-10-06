import numpy as np
import cv2
import matplotlib.pyplot as plt
import matplotlib.image as mimg
import easygui

path2 = easygui.fileopenbox(msg="Introduzca el path de la imagen", title="ABRIR ARCHIVO")
img=mimg.imread(path2)
f=open("archivo1.txt","w")
imgplot=plt.imshow(img)
ax = plt.gca()
fig = plt.gcf()
implot = ax.imshow(img, extent=[0,10,0,10])

k = 0
coords = []

def onclick(event):
    global ix, iy
    ix, iy = event.xdata, event.ydata
    print(ix,iy)
    global coords
    global k
    k = k+1
    coords.append((ix, iy))
    return coords

cid = fig.canvas.mpl_connect('button_press_event', onclick)

plt.show()
x1,y1=zip(*coords)
f.write(("%d\n")%(k))
for i in range(0,len(x1)):
    f.write(("%.1f\n")%(x1[i]))
    f.write(("%.1f\n")%(y1[i]))
