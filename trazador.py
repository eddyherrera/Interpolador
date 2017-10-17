#Librerias importadas
import tkinter as tk2
import matplotlib.pyplot as plt # Para graficar y mostrar la grilla
import matplotlib.image as mimg
import scipy.interpolate as interpolate # Importación de librerias para Interpolar
import numpy as np # Importación librerias para obtener tamaño de eje x e interpolación
import easygui
#Función para mostrar la mano original y permitir que el usuarios obtenga los puntos
k = 0
coords = []
def mostrarImagen():
    plt.figure("IMAGEN ORIGINAL")
    path1 = easygui.fileopenbox(msg="Introduzca el path de la imagen", title="ABRIR IMAGEN", filetypes = ["*.png", ["*.jpg", "*.jpeg"]  ] )
    im = plt.imread(path1) # Leerpath imagen que contiene la mano
    implot = plt.imshow(im, origin='upper', extent=[0,10,0,10]) #Ubicar la imagen en la grilla
    plt.grid(True) #Mostrar grilla

def onclick(event):
    global ix, iy
    ix, iy = event.xdata, event.ydata
    print(("%.2f , %.2f")%(ix,iy))
    global coords
    global k
    k = k+1
    coords.append((ix, iy))
    return coords
#Función principal
def main():
    mostrarImagen()
    print("\n\t    ==== MENU ====\n 1) Para abrir puntos desde archivo \n 2) Para introducir puntos desde consola\n 3) Para graficar dinamicamente ")
    eleccion = int(input())
    if ( eleccion == 1):
        path = easygui.fileopenbox(msg="Introduzca coordenadas", title="ABRIR COORDENADAS", default="*.txt")
        f=open(path,"r")
        n = float(f.readline());
        i = 0
        x0,y0 = [],[]
        while i<n:
            x0.append(float(f.readline()))
            y0.append(float(f.readline()))
            i=i+1
    elif eleccion == 2:
        print("Digitar: Numero de puntos, seguido de coor x , coor y")
        n=int(input()) #Obtención de cantidad de coordenadas
        x0, y0 = [], [] #Listas en donde se guardarán los datos de X y Y
        i=0 #contador
        while i<n: #Ciclo donde se guardarán las coordenadas ingresadas por el usuario
            x0.append(float(input()))
            y0.append(float(input()))
            i=i+1
    else:
        print("COORDENDAS\n")
        print("X  ,  Y\n")
        root = tk2.Tk()
        root.withdraw()
        path2 = easygui.fileopenbox(msg="Introduzca el path de la imagen", title="ABRIR ARCHIVO")
        root.update()
        pathpro = tk2.filedialog.asksaveasfilename(title = "GUARDADO DE ARCHIIVO",filetypes = (("txt files","*.txt"),("all files","*.*")))
        f = open(pathpro,"w")
        root.destroy()
        img=mimg.imread(path2)
        imgplot=plt.imshow(img)
        ax = plt.gca()
        fig = plt.gcf()
        implot = ax.imshow(img, extent=[0,10,0,10])
        cid = fig.canvas.mpl_connect('button_press_event', onclick)
        plt.show()
        x0, y0 = zip(*coords)
        global k
        n = k
        f.write(("%d\n")%(k))
        for i in range(0,len(x0)):
            f.write(("%.1f\n")%(x0[i]))
            f.write(("%.1f\n")%(y0[i]))


    indices = []
    i, anterior, pos= 0, 99999, 0
    dec, crec = False, False
    # Separación de las coordenadas cada vez que se detecta un cambio decreciente o creciente
    while i < n-1:
        if x0[i+1] <= x0[i]:
            dec = True
            while dec:
                if x0[i+1]>x0[i]:
                    indices.append(i)
                    break
                i=i+1
                if i>n-2:
                    break
        if i>n-2:
            break
        if x0[i+1] > x0[i]:
            crec = True
            while crec:
                if x0[i+1]<x0[i]:
                    indices.append(i)
                    break
                i=i+1
                if i>n-2:
                    break

    indices.append(n-1)
    i = 0
    #Interpolación con cada lista de puntos ORDENADA 
    while i < len(indices):
        xi, yi=  [] ,[]
        if i==0:
            j=0
        else:

            xi.append(antx)
            yi.append(anty)
            j=indices[i-1]+1
        while j<= indices[i]:
            xi.append(x0[j])
            yi.append(y0[j])
            j=j+1
            if j== indices[i]:
                antx= x0[j]
                anty= y0[j]

        i=i+1
        plt.figure("IMAGEN INTERPOLADA")
        #Cuando en el arreglo ajustado hayan menos de 4 puntos se unen
        if len(xi) <= 3:
            plt.plot(xi,yi)
        #Si en el arreglo ajustado hay mas de 3 puntos y menos de 20 de usuario
        #interpolación de la libreria numpy. (INTERPOLACION LINEAL)
        elif len(xi) >3 and len(xi) <  20:
            for l in range(len(xi)):
                for k in range(len(xi)-1-l):
                        if xi[k] > xi[k+1]:
                            xi[k],xi[k+1]= xi[k+1],xi[k]
                            yi[k],yi[k+1]= yi[k+1],yi[k]
            x = np.linspace(min(xi), max(xi), len(xi))
            ysp= np.interp(x,xi,yi)
            plt.plot(x,ysp)
        # Si ninguna de las condiciones se cumple se realiza una interpolación (INTERPOLACION SPLINES)
        #por trazadores usando funciones de la libreria Scipy
        else:
            #Crear nuevas listas sin puntos repetidos porque la interpolación
            #requiere que las listas no tengan valores repetidos
            lista_nueva,ynueva=[],[]
            for u in range(0,len(xi)):
                z=xi[u]
                if z not in lista_nueva:
                    lista_nueva.append(xi[u])
                    ynueva.append(yi[u])
            x = np.linspace(min(lista_nueva), max(lista_nueva), num=1001)  # Dominio
            #Ordenamiento burbuja de los vectores con los puntos en X y Y
            for u in range(len(lista_nueva)):
                for z in range(len(lista_nueva)-1-u):
                    if lista_nueva[z] > lista_nueva[z+1]:
                        lista_nueva[z],lista_nueva[z+1]= lista_nueva[z+1],lista_nueva[z]
            #interpolación con splines
            ysp = interpolate.InterpolatedUnivariateSpline(lista_nueva, ynueva)(x)  # Llamamos a la clase con x
            plt.plot(x,ysp)
    #Mostrar Grilla
    plt.grid(True)
    #Límites de la gráfica
    plt.xlim(0, 10)
    plt.ylim(0, 10)
    plt.show()
#Entrar al programa principal
if __name__ == '__main__':
    main()
