#!/usr/bin/python
# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import math

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm


MONTHS = [ 'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
DAYS = []
dataIN = []
nameCompanys = []

'''
Función que se encarga de  leer archivo con los datos del las empresas y cargarlo en un arreglo para luego realizar el manejo de los datos

recibe como parametro el nombre o ruta del archivo
'''
def readFileIN(fileIN):
    try:
        file = open(fileIN, 'r')
        count = 0
        for line in file.readlines():
            if count > 0 :
                line = line.rstrip('\n')
                tmpSplit = line.split('#')
                tmpSplit[2] = tmpSplit[2].split(',')
                dataIN.append(tmpSplit)
            count += 1
        print("lineas leidas " + str(count))
    except:
        print("Error leyendo el archivo, valide que exista  y que no contiene caracteres como tildes o ñ")
    finally:
        file.close()

'''
Función generica  que permite cargar valores de 1 a 31 para simular los dias calendario
'''
def loadDays():
    
    tmp_range = range(1,32)
    for x in tmp_range:
        DAYS.append(x)      
'''
Función que permite identificar cuales son las compañias que se cargaron por medio del nombre y las almacena en un  arreglo

'''
def indentityCompanys():
    for name in dataIN:
        if name[0] not in  nameCompanys:
            nameCompanys.append(name[0])

'''
Función que busca datos que le pertenecen a la empresa enviada.

recibe como parametro nombre de la empresa
'''
def filterDataCompany(nameCompany):
    tmpListData = []
    for data in dataIN:
        if data[0] == nameCompany:
            tmpListData.append(data)
    return tmpListData

'''
Función que  crea dataframe para mostra igual que la tabla 1 
recibe todos los datos de la compañia
'''
def createDataFrame1(dataCompany):
    datafirst = {}
    dataAll = { }
    first = True
    for dato in dataCompany:
        if first:
          datafirst[dato[1]] = dato[2]
          datafirst['Frecuencia'] = 1 
          first = False
        dataAll[dato[1]] = dato[2]
    data_frame1 = pd.DataFrame(datafirst, index = MONTHS) 
    data_frameAll = pd.DataFrame(dataAll, index = MONTHS)
    return data_frame1 , data_frameAll

'''
Función que  calcula elrango de procibilidad y la frecuecia para el data frame 1

recibe el dataframe ha ser procesado. 
'''
def possibilityAndPercent(dataFrame):
    tmp_range = []  
    tmp_percent = []
    #
    tmp_frecuencia = dataFrame['Frecuencia'].sum()
    for rango in dataFrame['Frecuencia']:
        tmp_range.append(rango/tmp_frecuencia)
        tmp_percent.append((rango/tmp_frecuencia)*100)
        
    dataFrame['Rango Probabilidad'] = tmp_range
    dataFrame['Porcentaje'] = tmp_percent
    print(dataFrame)
    return dataFrame

'''
Función que  crea dataframe para mostra igual que la tabla 2 
recibe todos los datos de la compañia
'''
def createDataFrame2(dataCompany):   
    dataFrame = pd.DataFrame(0.0, columns = MONTHS , index = DAYS)
    for x in range(len(MONTHS)):
        for y in range(len(DAYS)):
           if (dataFrame[MONTHS[x]].name == dataCompany.index.values[x]) and (int(dataCompany['2015'][x]) == int(dataFrame.index.values[y])):
               dataFrame[MONTHS[x]][DAYS[y]] = dataCompany['Porcentaje'][x]
    
    dataFrame['suma filas'] = dataFrame.sum(axis=1)
    #tmp_row_sum = pd.Series(dataFrame.sum(axis=0), name = 'Total X ') 
    #print(tmp_row_sum)
    #dataFrame.append(tmp_row_sum, ignore_index = False)
    print(dataFrame)
    #print(dataCompany)

'''
Función que  crea dataframe para mostra igual que la tabla 1 
recibe el dataframe 3 que equivale a la tabla 3, el tamaño del dataframe actual, el mes a buscar  y el día 
'''
def findDay(dataFrame3, tmp_index, month, day):
    tmp_return = False
    for s in range(tmp_index):
        if(dataFrame3['Mes'][s] == month and dataFrame3['Dia'][s] == day ):
            dataFrame3.loc[s]['Frecuencia'] += 1
            tmp_return =  True
    return tmp_return

'''
Función que  crea dataframe para mostra igual que la tabla 3 
recibe todos los datos de la compañia
'''
def createDataFrame3(data_frame_All):
    columnsDF = ['Mes', 'Dia', 'Frecuencia','Rango Probabilidad', 'Porcentaje' ]
    dataFrame3 = pd.DataFrame(columns =  columnsDF)
    tmp_columns = data_frame_All.columns
    tmp_index = 0
    for x in range(len(MONTHS)):
        for y in range(len(data_frame_All.columns)):
            tmp_serie = pd.Series([MONTHS[x], data_frame_All[tmp_columns[y]][MONTHS[x]], 1, 0, 0])
            #print(dataFrame3.query('Mes =="'+ MONTHS[x] +'" and  Dia =='+ data_frame_All[tmp_columns[y]][MONTHS[x]] ))
            if(findDay(dataFrame3, tmp_index, MONTHS[x], data_frame_All[tmp_columns[y]][MONTHS[x]]) == False):
                dataFrame3.loc[tmp_index] = tmp_serie
                dataFrame3.loc[tmp_index]['Mes'] = MONTHS[x]
                dataFrame3.loc[tmp_index]['Dia'] = data_frame_All[tmp_columns[y]][MONTHS[x]]
                dataFrame3.loc[tmp_index]['Frecuencia'] = 1
                dataFrame3.loc[tmp_index]['Rango Probabilidad'] = 0
                dataFrame3.loc[tmp_index]['Porcentaje'] = 0
                tmp_index += 1
    
    tmp_frecuencia = dataFrame3['Frecuencia'].sum()
    tmp_index = 0
    for rango in dataFrame3['Frecuencia']:
        dataFrame3.loc[tmp_index]['Rango Probabilidad'] = (rango/tmp_frecuencia)
        dataFrame3.loc[tmp_index]['Porcentaje'] = ((rango/tmp_frecuencia)*100)
        tmp_index += 1

    print(dataFrame3)
    return dataFrame3

'''
Función que  crea dataframe para mostra igual que la tabla 4 
recibe todos los datos de la compañia
'''
def createDateFrame4(dataFrame3):
    dataFrame4 = pd.DataFrame(0.0, columns = MONTHS , index = DAYS)
    for x in range(len(dataFrame3)):
        for y in range(len(MONTHS)):
            for z in range(len(DAYS)):
                    if (dataFrame4[MONTHS[y]].name == dataFrame3['Mes'][x]) and (int(dataFrame3['Dia'][x]) == int(dataFrame4.index.values[z])):
                        dataFrame4[MONTHS[y]][DAYS[z]] = dataFrame3['Porcentaje'][x]
                        
    print(dataFrame4)


def createFig1(dataFrame): 
    '''y = dataFrame['Porcentaje']
    x = dataFrame.index
    plt.title('Meses vs Porcentaje')
    plt.plot(x, y)
    plt.xticks(rotation='vertical')
    plt.show()


    x = (1,2,3,4,5,6,7,8,9,10,11,12)
    threedee = plt.figure( figsize=(10, 10)).gca(projection='3d')
    threedee.scatter(x , dataFrame['2015'], dataFrame['Porcentaje'], cmap='viridis')
    threedee.set_xvalue= MONTHS
    threedee.set_xlabel('Meses')
    threedee.set_ylabel('Dias')
    threedee.set_zlabel('Porcentaje')
    plt.show()
    '''
    
    result=[['2', '9', '3', '0', '19', '0','0','0','0','0','0','0','2', '9', '3', '0', '19', '0','0','0','0','0','0','0' '0','0','0','0','0','0','0'],
            ['2', '9', '3', '0', '19', '0','0','0','0','0','0','0','2', '9', '3', '0', '19', '0','0','0','0','0','0','0' '0','0','0','0','0','0','0'],
            ['2', '9', '3', '0', '19', '0','0','0','0','0','0','0','2', '9', '3', '0', '19', '0','0','0','0','0','0','0' '0','0','0','0','0','0','0'],
            ['2', '9', '3', '0', '19', '0','0','0','0','0','0','0','2', '9', '3', '0', '19', '0','0','0','0','0','0','0' '0','0','0','0','0','0','0'],
            ['2', '9', '3', '0', '19', '0','0','0','0','0','0','0','2', '9', '3', '0', '19', '0','0','0','0','0','0','0' '0','0','0','0','0','0','0'],
            ['2', '9', '3', '0', '19', '0','0','0','0','0','0','0','2', '9', '3', '0', '19', '0','0','0','0','0','0','0' '0','0','0','0','0','0','0'],
            ['2', '9', '3', '0', '19', '0','0','0','0','0','0','0','2', '9', '3', '0', '19', '0','0','0','0','0','0','0' '0','0','0','0','0','0','0'],
            ['2', '9', '3', '0', '19', '0','0','0','0','0','0','0','2', '9', '3', '0', '19', '0','0','0','0','0','0','0' '0','0','0','0','0','0','0'],
            ['2', '9', '3', '0', '19', '0','0','0','0','0','0','0','2', '9', '3', '0', '19', '0','0','0','0','0','0','0' '0','0','0','0','0','0','0'],
            ['2', '9', '3', '0', '19', '0','0','0','0','0','0','0','2', '9', '3', '0', '19', '0','0','0','0','0','0','0' '0','0','0','0','0','0','0'],
            ['2', '9', '3', '0', '19', '0','0','0','0','0','0','0','2', '9', '3', '0', '19', '0','0','0','0','0','0','0' '0','0','0','0','0','0','0'],
            ['2', '9', '3', '0', '19', '0','0','0','0','0','0','0','2', '9', '3', '0', '19', '0','0','0','0','0','0','0' '0','0','0','0','0','0','0']]
    '''['15', '407', '37', '10', '102'],
     ['100', '100', '100', '100', '100'],
     ['113', '25', '19', '31', '112'],
     ['43', '219', '35', '33', '14'],
     ['132', '108', '256', '119', '14'],
     ['22', '48', '352', '51', '438']]'''
    
    dataFrame2 = pd.DataFrame(0.0, columns = MONTHS , index = DAYS)
    
    result = np.array(result, dtype=np.int)
    
    fig=plt.figure(figsize=(20, 10), dpi=60)
    ax1=fig.add_subplot(111, projection='3d')
    
    xlabels = np.array(DAYS)
    xpos = np.arange(xlabels.shape[0])
    ylabels = np.array(MONTHS) 
    ypos = np.arange(ylabels.shape[0])
    
    xposM, yposM = np.meshgrid(xpos, ypos, copy=False)
    
    zpos = result
    zpos = zpos.ravel()
    
    dx=0.5
    dy=0.5
    dz=zpos
    
    ax1.w_xaxis.set_ticks(xpos + dx/2.)
    ax1.w_xaxis.set_ticklabels(xlabels)
    
    ax1.w_yaxis.set_ticks(ypos + dy/2.)
    ax1.w_yaxis.set_ticklabels(ylabels)
    
    values = np.linspace(0.2, 1., xposM.ravel().shape[0])
    colors = cm.rainbow(values)
    ax1.bar3d(xposM.ravel(), yposM.ravel(), dz*0, dx, dy, dz, color=colors)
    plt.show()
        


'''
Función que realzia el paso a paso para tratar y generar los datos de cada compañia del archivo
'''
def workCompany():
    for a in range(len(nameCompanys)):
        x = 0
        tmp_datacompany = pd.Series(filterDataCompany(nameCompanys[x]))
        print('\n')
        print('------>Calculos empresa '+ str(nameCompanys[x]) + ' <-----')
        print('\n')
        print('1) tabla 1: datos empresa primer año según frecuencia y rango de probabilidad ')
        print('\n')
        returnDataFrame1, data_frameAll  = createDataFrame1(tmp_datacompany)    
        returnDataFrame1 = possibilityAndPercent(returnDataFrame1)
        createFig1(returnDataFrame1)
        print('\n')
        print('2) tabla 2: datos empresa primer año meses por días')
        print('\n')
        createDataFrame2(returnDataFrame1)
        print('\n')
        print('3) tabla 3: datos empresa años cargados por frecuencia y rango de probabilidad día-mes')
        print('\n')
        dataFrame3 = createDataFrame3(data_frameAll)
        print('\n')
        print('4) tabla 4: datos empresa con el total de los años ingresado, meses por día ')
        print('\n')
        createDateFrame4(dataFrame3)

#generar pdf
def printPDF():
    pass

'''
Función principal del proyecto desde aquí se inicia todo el proceso de lectura de archivo y trabajo de la dta para cada compalia
se definen las propiedades para la consola de salida 
'''
if __name__ == '__main__':
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', -1)
    pd.set_option('expand_frame_repr', False)
    pd.set_option('display.html.table_schema', True)
    
    loadDays()
    
    readFileIN("input.txt")
    serieAll = pd.Series(dataIN)
    
    indentityCompanys()
    workCompany()
    printPDF()
    