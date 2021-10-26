# -*- coding: utf-8 -*-

from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory, Transaction
import csv

app = __revit__.Application
doc = __revit__.ActiveUIDocument.Document
ui = __revit__.ActiveUIDocument

valid_names = {"ADSK_Перфорированный кабельный лоток": "IEK_PF_HDZ_Лоток перфорированный_(05.04.01.02.02.01)"}

header = []
values = []

#open CSV file
with open('C:\Users\\vladi\Google Диск\В работе\\revit\плагины\Extensions\\bd.csv') as csvFile:
    csvReader = csv.reader(csvFile, delimiter=',')
    
    count = 0
    for row in csvReader:
        if count == 0:
            header.append(row)
        else:
            values.append(row)
        count += 1

#Filter by cable trays
cableTrays = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_CableTray).WhereElementIsNotElementType()

#get parameters from 'cableTrays'
for el in cableTrays:
    familyTypeName = el.Name
    paramSize = el.LookupParameter("Размер").AsString()
    split = paramSize.split("/")
    size = split[1] + "х" + split[0] + "х3000"

    #changes 'familyTypeName' if equal to 'valid_names'
    for valid_name in valid_names:
        if valid_name in el.Name:
            familyTypeName = valid_names[valid_name]
            

    count = 0
    for value in values:
        if value[1].decode('utf-8') == familyTypeName and value[4].decode('utf-8') == size:
           
            #Start transaction
            t = Transaction(doc, "Добавление значений параметров для лотков")
            t.Start()

            print("Параметры добавлены для: " + value[3].decode('utf-8'))
            
            param = el.LookupParameter("IEK_Наименование")
            param.Set(value[2].decode('utf-8'))
            
            param = el.LookupParameter("IEK_Артикул")
            param.Set(value[3].decode('utf-8'))

            param = el.LookupParameter("IEK_Цена с НДС")
            param.Set(value[8].decode('utf-8'))

            param = el.LookupParameter("IEK_Производитель")
            param.Set(value[5].decode('utf-8'))

            param = el.LookupParameter("IEK_Единица измерения")
            param.Set(value[6].decode('utf-8'))

            param = el.LookupParameter("IEK_Цена за единицу")
            param.Set(float(value[8]))
            
            #Finish transaction
            t.Commit()

print("Транзакция завершена успешно!")