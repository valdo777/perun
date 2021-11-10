# coding: utf8
from math import pi, acos, trunc

from Autodesk.Revit.DB import Line, ViewSection, XYZ, FilteredElementCollector, Grid, ReferencePlane, FamilyInstance, \
    BuiltInParameter, ElevationMarker, ViewType, Transaction
from Autodesk.Revit.UI.Selection import ObjectType
from Autodesk.Revit import Exceptions
from Autodesk.Revit.DB.Electrical import CableTray

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

typeCt = element.GetTypeId()
levelId = element.ReferenceLevel.Id
LevelOffset = element.LevelOffset
width = element.Width
height = element.Height

#print( round(lc.GetEndPoint(1).GetLength()) )
for connector in element.ConnectorManager.Connectors:
    #print( str(round(connector.Origin.GetLength(), 5)) )
    if round(connector.Origin.GetLength()) == round(lc.GetEndPoint(0).GetLength()):
        #print("conStar = " + str(round(connector.Origin.GetLength(), 5)))
        for con_Child in connector.AllRefs:
            conStart = con_Child
            #print("conStart")

    elif round(connector.Origin.GetLength()) == round(lc.GetEndPoint(1).GetLength()):
        #print("conEnd = " + str(round(connector.Origin.GetLength(), 5)))
        for con_Child in connector.AllRefs:
            conEnd = con_Child
            #print("conEnd")

v1 = element.Name.index("L=")
lct = int(element.Name[v1+2:v1+6:])
print(lc.Length * 304.8)
print(lct)

#print(conStart)
#print(conEnd)

if lc.Length * 304.8 > lct:
    #print(lc.Length * 304.8)
    count = trunc(lc.Length / (lct / 304.8))
    startP = lc.GetEndPoint(0)
    
    listC = []
    
    i = 0
    if element.LookupParameter("Смещение в начале").AsDouble() == element.LookupParameter("Смещение в конце").AsDouble():
    
        t = Transaction(doc, "Hor")
        t.Start()
        for i in range(i < count):
            if i < count:
                p1 = lc.Evaluate(0 + lct / (lc.Length * 304.8) * i, 1)
                p2 = lc.Evaluate(lct / (lc.Length * 304.8) + lct / (lc.Length * 304.8) * i, 1)
                ct = CableTray.Create(doc, typeCt, p1, p2, levelId)
                ct.LevelOffset = LevelOffset
                ct.get_Parameter(BuiltInParameter.RBS_CABLETRAY_WIDTH_PARAM).Set(width)
                ct.get_Parameter(BuiltInParameter.RBS_CABLETRAY_HEIGHT_PARAM).Set(height)
                print(str(p1) + "_" + str(p2))
                #if round(ct.ConnectorManager.Connectors.Origin.GetLength()) == round(p1.GetLength()):
                    #print(ct.ConnectorManager.Connectors.Origin.GetLength())
                #listC.append()
                #listC.append()
                
            if i == count - 1:
                p1 = lc.Evaluate(lct / (lc.Length * 304.8) + lct / (lc.Length * 304.8) * i, 1)
                p2 = lc.Evaluate(1, 1)
                ct = CableTray.Create(doc, typeCt, p1, p2, levelId)
                ct.LevelOffset = LevelOffset
                ct.get_Parameter(BuiltInParameter.RBS_CABLETRAY_WIDTH_PARAM).Set(width)
                ct.get_Parameter(BuiltInParameter.RBS_CABLETRAY_HEIGHT_PARAM).Set(height)
                #listC.append()
                #listC.append()
            print(i)
            i += 1

        #for i in range(i < (listC.Count - 2) / 2):
        t.Commit()
    
    else:
        t = Transaction(doc, "Vert")
        t.Start()
        for i in range(i < count):
            if i < count:
                p1 = lc.Evaluate(0 + lct / (lc.Length * 304.8) * i, 1)
                p2 = lc.Evaluate(lct / (lc.Length * 304.8) + lct / (lc.Length * 304.8) * i, 1)
                ct = CableTray.Create(doc, typeCt, p1, p2, levelId)
                ct.LevelOffset = LevelOffset
                ct.get_Parameter(BuiltInParameter.RBS_CABLETRAY_WIDTH_PARAM).Set(width)
                ct.get_Parameter(BuiltInParameter.RBS_CABLETRAY_HEIGHT_PARAM).Set(height)
                print(str(p1) + "_" + str(p2))
                
                #listC.append()
                #listC.append()
                
            if i == count - 1:
                p1 = lc.Evaluate(lct / (lc.Length * 304.8) + lct / (lc.Length * 304.8) * i, 1)
                p2 = lc.Evaluate(1, 1)
                ct = CableTray.Create(doc, typeCt, p1, p2, levelId)
                ct.LevelOffset = LevelOffset
                ct.get_Parameter(BuiltInParameter.RBS_CABLETRAY_WIDTH_PARAM).Set(width)
                ct.get_Parameter(BuiltInParameter.RBS_CABLETRAY_HEIGHT_PARAM).Set(height)
                
                #listC.append()
                #listC.append()
            print(i)
            i += 1
        t.Commit()

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