#!/usr/bin/python
# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import math


MONTHS = [ 'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
DAYS = []
dataIN = []
nameCompanys = []

#leer  archivo
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
        print("Error leyendo el archivo, valide que exista  y qu no contiene caracteres como tildes o ñ")
    finally:
        file.close()

def loadDays():
    tmp_range = range(1,32)
    for x in tmp_range:
        DAYS.append(x)      

def indentityCompanys():
    for name in dataIN:
        if name[0] not in  nameCompanys:
            nameCompanys.append(name[0])

def filterDataCompany(nameCompany):
    tmpListData = []
    for data in dataIN:
        if data[0] == nameCompany:
            tmpListData.append(data)
    return tmpListData

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
    return dataFrame

def createDataFrame2(dataCompany):
    loadDays()
    dataFrame = pd.DataFrame({}, columns = MONTHS , index = DAYS)
    for x in range(len(MONTHS)):
        for y in range(len(DAYS)):
           '''print(dataFrame[MONTHS[x]].name)
            print(dataCompany.index.values[x])
            print(dataFrame.index.values[y])
            print(dataCompany['2015'][x])
            #print(dataCompany['Frecuencia'][x])
            print(int(dataCompany['2015'][x]))# == int(dataFrame.index.values[x]))
            '''
           if (dataFrame[MONTHS[x]].name == dataCompany.index.values[x]) and (int(dataCompany['2015'][x]) == int(dataFrame.index.values[y])):
               dataFrame[MONTHS[x]][DAYS[y]] = dataCompany['Porcentaje'][x]
           elif (math.isnan(dataFrame[MONTHS[x]][DAYS[y]])):
               dataFrame[MONTHS[x]][DAYS[y]] = 0
    
    dataFrame['suma filas'] = dataFrame.sum(axis=1)
    #tmp_row_sum = pd.Series(dataFrame.sum(axis=0), name = 'Total X ') 
    #print(tmp_row_sum)
    #dataFrame.append(tmp_row_sum, ignore_index = False)
    print(dataFrame)
    print(dataCompany)

def findDay(dataFrame3, tmp_index, month, day):
    tmp_return = False
    for s in range(tmp_index):
        if(dataFrame3['Mes'][s] == month and dataFrame3['Dia'][s] == day ):
            dataFrame3.loc[s]['Frecuencia'] += 1
            tmp_return =  True
    return tmp_return
    
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

def createDateFrame4(dataFrame3):
    dataFrame4 = pd.DataFrame({}, columns = MONTHS , index = DAYS)
    for x in range(len(MONTHS)):
        for y in range(len(DAYS)):
            if (dataFrame4[MONTHS[x]].name == dataFrame3['Mes'][x]) and (int(dataFrame3['Dia'][x]) == int(dataFrame3.index.values[y])):
               dataFrame4[MONTHS[x]][DAYS[y]] = dataFrame3['Porcentaje'][x]
            elif (math.isnan(dataFrame4[MONTHS[x]][DAYS[y]])):
               dataFrame4[MONTHS[x]][DAYS[y]] = 0
    print(dataFrame4)

def workCompany():
    tmp_datacompany = pd.Series(filterDataCompany(nameCompanys[0]))
    returnDataFrame1, data_frameAll  = createDataFrame1(tmp_datacompany)
    
    returnDataFrame1 = possibilityAndPercent(returnDataFrame1)

    createDataFrame2(returnDataFrame1)
    dataFrame3 = createDataFrame3(data_frameAll)
    createDateFrame4(dataFrame3)

#generar pdf

if __name__ == '__main__':
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None) 
    
    readFileIN("input.txt")
    #print(dataIN)
    serieAll = pd.Series(dataIN)
    #series = pd.Series( tmp_split , index = MONTHS)
    indentityCompanys()
    workCompany()
    #print(nameCompanys)
    #print(serieAll)