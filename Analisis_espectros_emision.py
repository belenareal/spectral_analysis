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


directorio = input('Ingrese el directorio desde el home (entre comillas):\n')

os.chdir(directorio)

### Nombre de la estrella de estudio 

nombre_estrella = input('Ingrese el nombre de la estrella a estudiar, con el fin de guardar el analisis en una carpeta con dicho nombre:\n')
#nombre_estrella = 'hd37572'

inicio = nombre_estrella
#inicio = input('Ingrese el prefijo comun de los espectros para analizarlos todos juntos \nEjemplo: hd\n')
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
#    y_elem = 3968.470    
    y_elem = input("Ingrese el centro de la segunda linea que se quiere estudiar:\n")
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
            
    

### Seleccionar la distancia maxima entre la linea de interes y el pico del espectro.

#dist = input("Ingrese la distancia maxima de validez entre la linea de interes y el pico del espectro: \n sigma por ") # General.
dist = 2

          

###############################################################################            




########################################
###                                  ###
###           Espectro               ###
###                                  ###
######################################## 


### Crea el txt para guardar la lista de los nuevos espectros y el JD
guardar = open('Espectros_buenos_alineados.txt', 'wt') # Crea el archivo, si ya existe lo reemplaza.
guardar.close()

### Crea un archivo con los nombres de los espectros.

archi = open('Espectros_buenos.txt','r') 
lineas = archi.readlines()
mediciones = [l[:-1] for l in lineas] # Cuando uno abre el archivo se tiene el nombre de la medicion\n para eleiminar el \n esta esta linea.
cant_espectros = len(mediciones)

#cant_espectros = 1
    
### Se analiza cada espectro.
    
for esp in range(cant_espectros):
#    datos = np.loadtxt('./hd37572_0307b.txt')    
    datos = np.loadtxt(mediciones[esp])
    numero_med = esp



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
    
    
    ## Espectro.
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
                ###   Defino los maximos   ###
                ###                        ###
                ##############################
    
    ## Espectro.
    for i in range(len(new_long_onda)): 
        if new_long_onda[i] > xElemento - 2*sigma :
            index_min_new = i        
            break
    for i in range(len(long_onda)):
        if new_long_onda[i] > xElemento + 2*sigma :
            index_max_new = i        
            break
    
    ### Defino una nueva lista de datos de longitud de onda y flujo.
    max_long_onda = new_long_onda[index_min_new : index_max_new]
    max_flujo = new_flujo[index_min_new : index_max_new]
    
            
    ## Espectro
    maxlist = ss.argrelextrema(max_flujo,np.greater,order=1) # Puntos entre un maximo y el siguiente.
    ymax = max_flujo[maxlist] # Todos los maximos.
    
    ## Este if sirve para el caso que sea ruido y justo no se encuentren maximos locales, evita que salte un error.
    if len(ymax) == 0:
        ymax = 0      
        ymax2 = 0
    else:
        ### Me quedo con los maximos que esten por encima de un determinado valor.
        ymax.sort() # Ordena los maximos de menor a mayor. Dejando el maximo de interes al final.
        ymax2 = ymax[len(ymax)-1] # Toma el ultimo valor de ymax que es el maximo de interes, y lo llama ymax1.
        
    
    max_espectro = xElemento
    max_espectro_flujo = 0
    
    ### Veo para que valor de longitud de onda corresponde el maximo flujo
    for i in range(len(new_long_onda)):
        if xElemento + 1*sigma > new_long_onda[i] > xElemento-1*sigma: # Busca valores cercanos a la longitud de onda de la linea.
            flujo_maximo = new_flujo[i]            
            if new_flujo[i] == ymax2:
                max_espectro = new_long_onda[i]
                max_espectro_flujo = new_flujo[i]


###############################################################################


                #######################
                ###                 ###
                ###   Valor medio   ###         
                ###                 ###
                #######################
    
   
    valor_medio = np.mean(new_flujo)

       
        
            
    

###############################################################################



                ##############################
                ###                        ###
                ###  Alineo los espectros  ###
                ###                        ###
                ##############################


    ## Distancia entre el pico maximo que se encuentra cerca de la linea de estudio y la linea de estudio.
    long_max = max_espectro - xElemento 
    
    ## Defino una nueva lista de la misma longitud que los datos que me interesan. 
    ## En ella luego se van a guardar las longitudes de onda corridas de cada espectro.        
    corrido_long_onda =  []
    corrido_long_onda = range(len(new_long_onda))
    
    
    ## Si esta corrido a la derecha.
    if max_espectro >= xElemento:
        ## Y esta a menos de 2 sigma
        if max_espectro <= xElemento + (dist*sigma):
            for i in range(len(new_long_onda)):
                corrido_long_onda[i] = new_long_onda[i] - long_max
    else: ## Si esta corrido a la izquierda del espectro testigo. 
        ## Y esta a menos de 2 sigma
        if max_espectro >= xElemento - (dist*sigma):
            for i in range(len(new_long_onda)):
                corrido_long_onda[i] = new_long_onda[i] - long_max
                
                
                
                ### Defino las nuevas coordenadas del maximo ###
                                            
    ## Espectro.                
    for i in range(len(corrido_long_onda)): 
        if corrido_long_onda[i] > xElemento - 2*sigma :
            index_min_new2 = i        
            break
    for i in range(len(corrido_long_onda)):
        if corrido_long_onda[i] > xElemento + 2*sigma :
            index_max_new2 = i        
            break
    
    
    ### Defino una nueva lista de datos de longitud de onda y flujo.
    max2_long_onda = corrido_long_onda[index_min_new2 : index_max_new2]
    max2_flujo = new_flujo[index_min_new2 : index_max_new2]
    
            
    ## Espectro
    maxlist_corrido = ss.argrelextrema(max2_flujo,np.greater,order=1) # Puntos entre un maximo y el siguiente.
    ymax_corrido = max2_flujo[maxlist_corrido] # Todos los maximos.
    
    if len(ymax_corrido) == 0:
        ymax_corrido = 0
        ymax_corrido2 = 0
    else:      
        ### Me quedo con los maximos que esten por encima de un determinado valor.  
        ymax_corrido.sort() # Ordena los maximos de menor a mayor. Dejando el maximo de interes al final.
        ymax_corrido2 = ymax_corrido[len(ymax_corrido)-1] # Toma el ultimo valor de ymax que es el maximo de interes, y lo llama ymax1.
     
       
    
    ### Veo para que valor de longitud de onda corresponde el maximo flujo
    for i in range(len(corrido_long_onda)):
        if xElemento + 1*sigma > corrido_long_onda[i] > xElemento-1*sigma: # Busca valores cercanos a la longitud de onda de la linea.
            flujo_maximo_corrido = new_flujo[i]            
            if new_flujo[i] == ymax_corrido2:
                max_espectro_corrido = corrido_long_onda[i]
                max_espectro_flujo_corrido = new_flujo[i]




###############################################################################


    
        #############################################################
        ###                                                       ###
        ###  Construccion del triangulo al rededor de cada linea  ###
        ###                                                       ###
        #############################################################    
    
    
    ###    Busco el maximo para la construccion del triangulo   
            
    ## Espectro testigo
    maximo_triangulo = ss.argrelextrema(max2_flujo,np.greater,order=1) # Puntos entre un maximo y el siguiente.
    ymax_triangulo = max2_flujo[maximo_triangulo] # Todos los maximos.
    
    if len(ymax_triangulo) != 0:
        ### Me quedo con los maximos que esten por encima de un determinado valor.   
        ymax_triangulo.sort() # Ordena los maximos de menor a mayor. Dejando el maximo de interes al final.
        ymax_util = ymax_triangulo[len(ymax_triangulo)-1] # Toma el ultimo valor de ymax que es el maximo de interes, y lo llama ymax_testigo2.
                                            
        ### Linea de estudio.
        x1 = xElemento - sigma
        x2 = xElemento + sigma  
        y0 = ymax_util * 1.01  ## 50% mas que el valor del pico, hay que automatizarlo.
        y1 = ymax_util/2
        
        ## Recta ascendente.
        aElemento = (y0 - y1)/(xElemento - x1) # Pendiente.
        bElemento = (y1*xElemento - x1*y0)/(xElemento - x1) # Ordenada al origen.
        
        def fb(x):
            return aElemento*x + bElemento
        
        ## Recta descendente.
        cElemento = (y1*xElemento - x2*y0)/(xElemento - x2) # Ordenada al origen.
            
        def fc(x):
            return -aElemento*x + cElemento
            
            

        
####################################################################            
        
        
            
            ######################################################
            ###                                                ###
            ###    Grafico el espectro y la linea a estudiar   ###
            ###                                                ###     
            ######################################################
    

    if len(ymax) == 0:
        plt.xlim(xmin, xmax) # Limite en eje x.
#        plt.ylim(0, 4e-12) # Limite en eje y.
        plt.ylabel('Flujo') # Etiqueta al eje y.
        plt.xlabel('Longi11tud de Onda') # Etiqueta al eje x.
#        plt.yticks([-4e-12, -2e-12, 0, 2e-12, 4e-12])
        plt.xticks([xElemento])
        plt.axvline(xElemento, color = 'r')  # Dibujamos una línea vertical verde centrada en xElemento
#        plt.axvline(yElemento, color = 'r')  # Dibujamos una línea vertical verde centrada en yElemento
        plt.axhline(valor_medio, color = 'g')
        plt.plot(new_long_onda, new_flujo, 'b', label='Espectro descartado por ruido') # Dibujo flujo en funcion de longitud de onda    
        print['Espectro descartado por no poseer maximo locales en la linea de estudio. Ruido'+ str(mediciones[esp])]
#        print['Espectro descartado por no poseer maximo locales en la linea de estudio. Ruido']
        
        para_guardar_malos = open('Espectros_malos.txt', 'a')
        ### Se escribe los nombres de los espectros a analizar.
        para_guardar_malos.write(str(mediciones[esp])+'\n')
        para_guardar_malos.close()
    else:
        plt.figure('Espectro '+str(mediciones[esp]))
##        plt.subplot(2, 1, 1)
        print['Espectro '+ str(mediciones[esp])]
        plt.xlim(xmin, xmax) # Limite en eje x.
        plt.ylim(0, max_espectro_flujo *1.2) # Limite en eje y.
        plt.ylabel('Flujo') # Etiqueta al eje y.
        plt.xlabel('Longitud de Onda') # Etiqueta al eje x.
#        plt.plot(long_onda, flujo) # Dibujo flujo en funcion de longitud de onda, del espectro completo.
        # Dibujo flujo en funcion de longitud de onda, del espectro recortado.
        plt.plot(corrido_long_onda,new_flujo,'b') 
        plt.axvline(xElemento, color = 'r')  # Dibujamos una línea vertical verde centrada en xElemento
#        plt.axvline(yElemento, color = 'r')  # Dibujamos una línea vertical verde centrada en yElemento
        plt.axhline(valor_medio, color = 'g')  
#        plt.axhline(max_espectro_flujo, color = 'y')
        plt.plot(max_espectro_corrido,max_espectro_flujo_corrido,'*y') # Marca los maximos encontrados.
        plt.hold(True) # Me permite continuar adicionando curvas al grafico.

        ### Grafica las lineas.
        # Limites de las rectas utilizadas.
        xbElemento = np.linspace(xmin,xElemento,20)
        xcElemento = np.linspace(xElemento,xmax,20)
        # Grafica las rectas utilizadas.
        plt.plot(xbElemento,fb(xbElemento),'--r')
        plt.plot(xcElemento,fc(xcElemento),'--r')
        
        if numero_lineas == 1: # No hay otra linea de estudio.
            pass
        else: # Hay otra linea de estudio.
            x3 = yElemento - sigma
            x4 = yElemento + sigma
            
            # Recta ascendente.
            a_otro = (y0 - y1)/(yElemento - x3) # Pendiente.
            b_otro = (y1*yElemento - x3*y0)/(yElemento - x3) # Ordenada al origen.
            
            def fb_otro(x):
                return a_otro*x + b_otro
            
            # Recta descendente.
            c_otro = (y1*yElemento - x4*y0)/(yElemento - x4) # Ordenada al origen.
            
            def fc_otro(x):
                return -a_otro*x + c_otro
                
            ### Grafica las lineas.
            # Limites de las rectas utilizadas
            ybElemento = np.linspace(xmin,yElemento,20)
            ycElemento = np.linspace(yElemento,xmax,20)
            # Grafica las rectas utilizadas
            plt.plot(ybElemento,fb_otro(ybElemento),'--r')
            plt.plot(ycElemento,fc_otro(ycElemento),'--r')
        
##        plt.show()
        
        ### Recorta el nombre dejando en exp el nombre del espectro sin el .txt y en JD el JD correspondiente a la medicion
        nombre_del_espectro = str(mediciones[esp])
        exp = nombre_del_espectro[:-4]
        exp2 = nombre_del_espectro[:-5]
        JD = exp2[-4:]

        
        plt.savefig('Espectro_' + str(exp)+ '.png')


        para_guardar = open('Espectros_buenos_alineados.txt', 'a') # Abre el archivo, escribe cada linea debajo de la anterior
        ### Se escribe los nombres de los espectros a analizar.
        para_guardar.write(str(exp) +'_corr_emi.txt'+' '+ str(JD) +'\n')
        para_guardar.close()
#            
#
        
################################################################################     
        
        
            ###########################################
            ###                                     ###
            ###     Guarda los nuevos espectros     ###          
            ###                                     ###            
            ###########################################
        
        nuevo_archivo = open(str(exp) +'_corr_emi.txt', 'w')
        for i in range(len(corrido_long_onda)):    
            nuevo_archivo.write(repr(corrido_long_onda[i])+' '+repr(new_flujo[i])+'\n' ) # Guarda los datos corregidos
        nuevo_archivo.close()   