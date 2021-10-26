# coding: utf8
from Autodesk.Revit.DB import FilteredElementCollector, BuiltInParameter, BuiltInCategory, Transaction
import rpw

__doc__ = """Number busbar marking duct systems sequentially"""
__title__ = "Number\nbusbar"
__authors__ = ["Vlad Sozutov"]
__highlight__ = 'new'

app = __revit__.Application
doc = __revit__.ActiveUIDocument.Document
ui = __revit__.ActiveUIDocument

fittings = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_DuctFitting).WhereElementIsNotElementType().ToElements()


count = 0
def find_next(element):
    global count
    count += 1

    try:
        #Instance
        connectors = element.MEPModel.ConnectorManager.Connectors
        if element.Name == "start":
            for connector in connectors:
                mepSystem_param = element.get_Parameter(BuiltInParameter.ALL_MODEL_INSTANCE_COMMENTS)
                mepSystem_value = connector.MEPSystem.Name.ToString()
                t = Transaction(doc, "Нумерация шинопровода")
                t.Start()
                mepSystem_param.Set(str(mepSystem_value[2]) + ".1")
                t.Commit()
                for ref in connector.AllRefs:
                    if str(type(ref.Owner)) == "<type 'Duct'>":
                        return find_next(ref.Owner)

        elif element.Name == "finish":
            for connector in connectors:
                mepSystem_param = element.get_Parameter(BuiltInParameter.ALL_MODEL_INSTANCE_COMMENTS)
                mepSystem_value = connector.MEPSystem.Name.ToString()
                t = Transaction(doc, "Нумерация шинопровода")
                t.Start()
                mepSystem_param.Set(str(mepSystem_value[2]) + "." + str(count))
                t.Commit()
            count = 0
            return 0

        else:
            for connector in connectors:
                mepSystem_param = element.get_Parameter(BuiltInParameter.ALL_MODEL_INSTANCE_COMMENTS)
                mepSystem_value = connector.MEPSystem.Name.ToString()
                t = Transaction(doc, "Нумерация шинопровода")
                t.Start()
                mepSystem_param.Set(str(mepSystem_value[2]) + "." + str(count))
                t.Commit()
                for ref in connector.AllRefs:
                    if str(type(ref.Owner)) == "<type 'Duct'>" and str(ref.Direction) == "Out":
                        return find_next(ref.Owner)
    except:
        pass
    try:
        #Duct
        connectors = element.ConnectorManager.Connectors
        for connector in connectors:    
            mepSystem_param = element.get_Parameter(BuiltInParameter.ALL_MODEL_INSTANCE_COMMENTS)
            mepSystem_value = connector.MEPSystem.Name.ToString()
            t = Transaction(doc, "Нумерация шинопровода")
            t.Start()
            mepSystem_param.Set(str(mepSystem_value[2]) + "." + str(count))
            t.Commit()
            for ref in connector.AllRefs:
                if str(type(ref.Owner)) == "<type 'FamilyInstance'>" and str(ref.Direction) == "Out":
                    return find_next(ref.Owner)
    except:
        pass


fittings = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_DuctFitting).WhereElementIsNotElementType().ToElements()
for fitting in fittings:
    if fitting.Name == "start":
        find_next(fitting)