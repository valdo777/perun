# coding: utf8
from math import pi, acos

from Autodesk.Revit.DB import Line, ViewSection, XYZ, FilteredElementCollector, Grid, ReferencePlane, FamilyInstance, \
    BuiltInParameter, ElevationMarker, ViewType, BuiltInCategory, Transaction
from Autodesk.Revit.UI.Selection import ObjectType
from Autodesk.Revit import Exceptions

import rpw
from pyrevit import forms, script

__doc__ = """Маркирует элементы шинопровода по порядку"""
__title__ = "Маркировка\nшинопровода"
__authors__ = ["Vlad Sozutov"]
__highlight__ = 'new'

uidoc = rpw.revit.uidoc
doc = rpw.revit.doc
logger = script.get_logger()


fittings = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_DuctFitting).WhereElementIsNotElementType().ToElements()
elementsPast = []
secondElements = []

for fitting in fittings:
    if fitting.Name == "start":
        elementsPast.append(fitting.Name)
        SystemName = fitting.get_Parameter(BuiltInParameter.RBS_SYSTEM_NAME_PARAM).AsString()
        #print(SystemName)
        connectors = fitting.MEPModel.ConnectorManager.Connectors
        for connector in connectors:
            for ref in connector.AllRefs:
                if str(type(ref.Owner)) == "<type 'Duct'>":
                    secondElements.append(ref.Owner)
                    #print(ref.Owner)
                    #for i in el.MEPSystem.DuctNetwork:
                        #print(i)
                        #logger.debug("Ошибка! здесь")


for i in secondElements:
    for k in i.MEPSystem.DuctNetwork:
        print(k)
        if k.Name not in elementsPast:
            print(str(k.Id) + " - not Past")
        else:
            elementsPast.append(k)

    # for j in range(7):
    #     try:
    #         connectors = i.ConnectorManager.Connectors
    #         for connector in connectors:
    #             for ref in connector.AllRefs:
    #                 if str(type(ref.Owner)) == "<type 'Duct'>":
    #                     element = ref.Owner
    #     except:
    #         print("notDuct")

    #     try:
    #         connectors = i.MEPModel.ConnectorManager.Connectors
    #         for connector in connectors:
    #             for ref in connector.AllRefs:
    #                 if str(type(ref.Owner)) == "<type 'FamilyInstance'>":
    #                     element = ref.Owner
    #     except:
    #         print("notFamilyInstance")