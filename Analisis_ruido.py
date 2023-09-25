# -*- coding: utf-8 -*-
"""

@author: Belen Areal


"""


            #######################################
            ###                                 ###
            ###      Paquetes importados        ###
            ###                                 ###
            #######################################


import numpy as np 
import matplotlib.pyplot as plt
import scipy.signal as ss
import os as os



###############################################################################            



            #######################################
            ###                                 ###
            ###  Datos que se piden al usuario  ###
            ###                                 ###
            #######################################


directorio = input('Ingrese el directorio desde el home:\n')

os.chdir(directorio)


### Nombre de la estrella de estudio 

nombre_estrella = input('Ingrese el nombre de la estrella a estudiar, entre comillas (ejemplo hd17925)\n')
#nombre_estrella = 'hd35850'

inicio = nombre_estrella
#inicio = input('Ingrese el prefijo comun de los espectros ejemplo:hd, entre comillas\n')
#inicio = 'hd'




###############################################################################            



            #########################################
            ###                                   ###
            ###   Derminar las lineas de CaII y K ###
            ###                                   ###
            #########################################


### Limites de longitud de onda.

#print "Ingresar limites necesarios en longitud de onda" 
#xmin = input("Ingrese limite inferior:\n")# Limite inferior de grafica, antes 3890 (Ca II K).
#xmax = input("Ingrese limite superior:\n")# Limite superior de grafica, antes 4012 (Ca II H).
xmin = 3888
xmax = 4014

sigma = 0.545 # La mitad de 1.09.


#numero_lineas = input("Marque el numero de Lineas que quiere estudiar (maximo 2):\n") # Da la orden de analizar otra linea o no
numero_lineas = 1

#x_elem = input("Ingrese el centro de la linea que se quiere estudiar:\n") # General.
x_elem = 3933.664

if numero_lineas == 2:
    y_elem = 3968.470    
#    y_elem = input("Ingrese el centro de la segunda linea que se quiere estudiar:\n")
else:
    y_elem = 0    

if y_elem == 0:
    xElemento = x_elem
else:
    if y_elem > x_elem:
        xElemento = x_elem
        yElemento = y_elem
    else:
        xElemento = y_elem
        yElemento = x_elem
            
    

###############################################################################            




########################################
###                                  ###
###           Espectro               ###
###                                  ###
######################################## 
#
#
#para_guardar = open('/Espectros_buenos.txt', 'w')
#para_guardar.close()

### Crea un archivo con los nombres de los espectros.

fichero = open('Lista_espectros.txt', 'wt') # Crea el archivo, si ya existe lo reemplaza.

### Se escribe los nombres de los espectros a analizar.
for archivo in os.listdir("."):
    if archivo.startswith(str(inicio)): # Guarda los espectros cuyo nombre inicien con el termino dado anteriormente.
        fichero.write(archivo +'\n')
fichero.close()

### Se abre el archivo con los espectros a analizar usarlo en el siguiente for.
archi = open('Lista_espectros.txt','r') 
lineas = archi.readlines()
mediciones = [l[:-1] for l in lineas] # Cuando uno abre el archivo se tiene el nombre de la medicion\n para eleiminar el \n esta esta linea.
cant_espectros = len(mediciones)
#cant_espectros = 1
p = range(cant_espectros)    
pl = range(cant_espectros)  
d = range(cant_espectros) 
### Se analiza cada espectro.
    
for esp in range(cant_espectros):
#    datos = np.loadtxt('./hd23249_0904b.txt')    
    datos = np.loadtxt(mediciones[esp])
#    numero_med = esp
    
    ### Defino la longitud de onda y el flujo de cada espectro y de la resta. 
    
    ## Espectro.
    long_onda = datos[:,0]  # Toma la longitud de onda.
    flujo = datos[:,1] # Toma el flujo.
        
    
    
###############################################################################            
    
    
    
            ###############################
            ###                         ###    
            ###    Recorta el espectro  ###
            ###                         ###
            ###############################
    
     
    ## Recorta el espectro.
    for i in range(len(long_onda)): 
        if long_onda[i] > 3891 :
            index_min = i        
            break
        
    for i in range(len(long_onda)):
        if long_onda[i] > 3911:
            index_max = i        
            break
    
    ## Defino una nueva lista de datos de longitud de onda y flujo.
    new_long_onda = long_onda[index_min : index_max]
    new_flujo= flujo[index_min : index_max]
    
    
                #######################
                ###                 ###
                ###   Valor medio   ###         
                ###                 ###
                #######################
    
    ## Calcula el valor medio de todo el contiuo. 

    media = np.mean(new_flujo) # calcula el valor medio del continuo.
         
    p[esp] = media # genera una lista con el valor para cada espectro del valor medio del continuo.
    desv = np.std(new_flujo)
    d[esp] = desv  
###############################################################################

        
            
                ##############################    
                ###                        ###
                ###   Valor medio local    ###
                ###                        ###
                ##############################
    
    


    ## Recorta el espectro en una distancia de 3 sigmas de la linea de CaII K
    for i in range(len(long_onda)): 
        if long_onda[i] > xElemento - 3*sigma :
            index_min_new = i        
            break
    for i in range(len(long_onda)):
        if long_onda[i] > xElemento + 3*sigma :
            index_max_new = i        
            break
    
    ### Defino una nueva lista de datos de longitud de onda y flujo.
    min_long_onda = long_onda[index_min_new : index_max_new]
    min_flujo = flujo[index_min_new : index_max_new]
    

    media_local = np.mean(min_flujo) # calcula el valor medio del continuo.
         
    
    pl[esp] = media_local # genera una lista con el valor para cada espectro del valor medio local.
    
    
    
###############################################################################


### Vuelve a recorrer los archivos para poder graficarlos usando los valores medios calculados.

### Se analiza cada espectro.
    
for esp in range(cant_espectros):
#    datos = np.loadtxt('./hd23249_0904b.txt')    
    datos = np.loadtxt(mediciones[esp])
#    numero_med = esp
    
    ### Defino la longitud de onda y el flujo de cada espectro y de la resta. 
    
    ## Espectro.
    long_onda = datos[:,0]  # Toma la longitud de onda.
    flujo = datos[:,1] # Toma el flujo.
        
    
    
###############################################################################            
    
    
    
            ###############################
            ###                         ###    
            ###    Recorta el espectro  ###
            ###                         ###
            ###############################
    
     
    ## Recorta el espectro.
     
    for i in range(len(long_onda)): 
        if long_onda[i] > xmin :
            index_min = i        
            break
        
    for i in range(len(long_onda)):
        if long_onda[i] > xmax :
            index_max = i        
            break
    
    ## Defino una nueva lista de datos de longitud de onda y flujo.
    new_long_onda = long_onda[index_min : index_max]
    new_flujo= flujo[index_min : index_max]
    
    
    
    
###############################################################################
            
                ##############################    
                ###                        ###
                ###    Graficar espectros  ###
                ###                        ###
                ##############################
    
    media_local = pl[esp]
    media= p[esp]
    dd = d[esp]
    ## Se fija si el valor medio local esta entro del valor medio del continuo mas menos la desviacion lo considera ruido. 
    if media-dd < media_local < media+dd:
        print['Espectro descartado por ruido ' + str(mediciones[esp])]
        plt.figure('Espectro descartado '+str(mediciones[esp]))
        plt.xlim(xmin, xmax) # Limite en eje x.
#        plt.ylim(0, 4e-12) # Limite en eje y.
        plt.ylabel('Flujo') # Etiqueta al eje y.
        plt.xlabel('Longitud de Onda') # Etiqueta al eje x.
#        plt.yticks([-4e-12, -2e-12, 0, 2e-12, 4e-12])
        plt.xticks([xElemento])
        plt.axvline(xElemento, color = 'r')  # Dibujamos una línea vertical verde centrada en xElemento
#        plt.axvline(yElemento, color = 'r')  # Dibujamos una línea vertical verde centrada en yElemento
        plt.axhline(media, color = 'g') # Grafica una linea en el valor medio del continuo.
        plt.axhline((media-dd), color = 'y') # Grafica una linea en el valor medio del continuo - la desviacion.
        plt.axhline((media+dd), color = 'y') # Grafica una linea en el valor medio del continuo + la desviacion.
        plt.axhline(media_local, color = 'r') # Grafica una linea en el valor medio local.     
        plt.plot(new_long_onda, new_flujo, 'b', label='Espectro descartado por ruido')      
#        plt.savefig('EspectroDescartado_por_ruido_' + str(mediciones[esp]) + '.png')
        
#        para_guardar_malos = open('Espectros_malos.txt', 'a')
#        ### Se escribe los nombres de los espectros a analizar.
#        para_guardar_malos.write(str(mediciones[esp])+'\n')
#        para_guardar_malos.close()

    else: # sino es un buen espectro.
        print['Espectro bueno ' + str(mediciones[esp])]
        plt.figure('Espectro bueno '+str(mediciones[esp]))
        plt.xlim(xmin, xmax) # Limite en eje x.
#        plt.ylim(0, 4e-12) # Limite en eje y.
        plt.ylabel('Flujo') # Etiqueta al eje y.
        plt.xlabel('Longitud de Onda') # Etiqueta al eje x.
#        plt.yticks([-4e-12, -2e-12, 0, 2e-12, 4e-12])
        plt.xticks([xElemento])
        plt.axvline(xElemento, color = 'r')  # Dibujamos una línea vertical verde centrada en xElemento
#        plt.axvline(yElemento, color = 'r')  # Dibujamos una línea vertical verde centrada en yElemento
        plt.axhline(media, color = 'g') # Grafica una linea en el valor medio del continuo.
        plt.axhline((media-dd), color = 'y') # Grafica una linea en el valor medio del continuo - la desviacion.
        plt.axhline((media+dd), color = 'y') # Grafica una linea en el valor medio del continuo + la desviacion.
        plt.axhline(media_local, color = 'r') # Grafica una linea en el valor medio local.     
        plt.plot(new_long_onda, new_flujo, 'b', label='Espectro bueno') 
        
        
#        guardar = open('Espectros_buenos.txt', 'a') # Crea el archivo, si ya existe lo reemplaza.
#        guardar.close()
        
        para_guardar = open('Espectros_buenos.txt', 'a') # Abre el archivo, escribe cada linea debajo de la anterior
        ### Se escribe los nombres de los espectros a analizar.
        para_guardar.write(str(mediciones[esp])+'\n')
        para_guardar.close()