# coding: utf8
from math import pi, acos, trunc

from Autodesk.Revit.DB import Line, ViewSection, XYZ, FilteredElementCollector, Grid, ReferencePlane, FamilyInstance, \
    BuiltInParameter, ElevationMarker, ViewType
from Autodesk.Revit.UI.Selection import ObjectType
from Autodesk.Revit import Exceptions

import rpw
from pyrevit import forms, script


__doc__ = """Сuts the busbar to length, including vertical sections"""
__title__ = "Test"
__authors__ = ["Vlad Sozutov"]

uidoc = rpw.revit.uidoc
doc = rpw.revit.doc
logger = script.get_logger()

def element_selection():
    try:
        with forms.WarningBar(title="Pick busbar to be cut into segments"):
            reference = uidoc.Selection.PickObject(ObjectType.Element, "Pick reference element")
            return reference
    except Exceptions.OperationCanceledException:
        return False

element = doc.GetElement(element_selection().ElementId)
lc = element.Location.Curve


#print( round(lc.GetEndPoint(1).GetLength()) )
for connector in element.ConnectorManager.Connectors:
    #print( str(round(connector.Origin.GetLength(), 5)) )
    if round(connector.Origin.GetLength()) == round(lc.GetEndPoint(0).GetLength()):
        #print("conStar = " + str(round(connector.Origin.GetLength(), 5)))
        pass

    elif round(connector.Origin.GetLength()) == round(lc.GetEndPoint(1).GetLength()):
        #print("conEnd = " + str(round(connector.Origin.GetLength(), 5)))
        pass

v1 = element.Name.index("L=")
b = int(element.Name[v1+2:v1+6:])

if lc.Length * 304.8 > b:
    #print(lc.Length * 304.8)
    count = trunc(lc.Length / (b / 304.8))
    startP = lc.GetEndPoint(0)
    

# try:
#     v1 = element.Name.index("L=")
#     str2 = element.Name.Remove(0, v1 + 2)
#     lct = 
# except:
#     pass

# element = doc.GetElement(element_selection.ElementId)
# if element is Duct:
#     typeCt = element.GetTypeId()
#     levelId = element.ReferenceLevel.Id
    
#     LevelOffset = element.LevelOffset
#     width = element.Width
#     height = element.Height

#     Lc = element.Location.Curve

#     conStart = 0
#     conEnd = 0
    
#     for connector in element.ConnectorManager.Connectors:
#         if round(connector.Origin.GetLength(), 5) == round(Lc.GetEndPoint(0).GetLength(), 5):
#             for ref in connector.AllRefs:
#                 if (ref.Owner is FamilyInstance):
#                     conStart = ref
