# coding: utf8
from Autodesk.Revit.DB import FilteredElementCollector, BuiltInParameter, BuiltInCategory
import rpw

__doc__ = """number busbar marking duct systems sequentially"""
__title__ = "Number\nbusbar"
__authors__ = ["Vlad Sozutov"]
__highlight__ = 'new'

uidoc = rpw.revit.uidoc
doc = rpw.revit.doc

fittings = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_DuctFitting).WhereElementIsNotElementType().ToElements()

count = 0
def find_next(element):
    global count
    count += 1
    print(count)
    try:
        #Instance
        connectors = element.MEPModel.ConnectorManager.Connectors
        if element.Name == "start":
            #print("START")
            for connector in connectors:    
                for ref in connector.AllRefs:
                    if str(type(ref.Owner)) == "<type 'Duct'>":
                        print(ref.Owner)
                        return find_next(ref.Owner)
        elif element.Name == "finish":
            #print("finish")
            return 0
        else:
            for connector in connectors:    
                for ref in connector.AllRefs:
                    if str(type(ref.Owner)) == "<type 'Duct'>" and str(ref.Direction) == "Out":
                        return find_next(ref.Owner)
    except:
        pass
    try:
        #Duct
        connectors = element.ConnectorManager.Connectors
        for connector in connectors:    
            for ref in connector.AllRefs:
                if str(type(ref.Owner)) == "<type 'FamilyInstance'>" and str(ref.Direction) == "Out":
                    return find_next(ref.Owner)
    except:
        pass


fittings = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_DuctFitting).WhereElementIsNotElementType().ToElements()
for fitting in fittings:
    if fitting.Name == "start":
        find_next(fitting)