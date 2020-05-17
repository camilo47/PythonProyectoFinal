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
    print(dataFrame.sum(axis=1))
    print(dataCompany)

def workCompany():
    tmp_datacompany = pd.Series(filterDataCompany(nameCompanys[1]))
    returnDataFrame1, data_frameAll  = createDataFrame1(tmp_datacompany)
    
    returnDataFrame1 = possibilityAndPercent(returnDataFrame1)
    print(returnDataFrame1)
    print(data_frameAll)
    
    createDataFrame2(returnDataFrame1)

#generar pdf

if __name__ == '__main__':
    readFileIN("input.txt")
    #print(dataIN)
    serieAll = pd.Series(dataIN)
    #series = pd.Series( tmp_split , index = MONTHS)
    indentityCompanys()
    workCompany()
    #print(nameCompanys)
    #print(serieAll)