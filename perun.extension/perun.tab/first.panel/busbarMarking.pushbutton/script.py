# coding: utf8
from Autodesk.Revit.DB import FilteredElementCollector, BuiltInParameter, BuiltInCategory
import rpw

__doc__ = """Маркирует элементы шинопровода по порядку"""
__title__ = "Маркировка\nшинопровода"
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
        print("Instance")
        #Instance
        connectors = element.MEPModel.ConnectorManager.Connectors
        if element.Name == "start":
            #print("START")
            for connector in connectors:    
                for ref in connector.AllRefs:
                    if str(type(ref.Owner)) == "<type 'Duct'>":
                        print(ref.Owner)
                        return find_next(ref.Owner)
            #ref = connectors[0].AllRefs[0]
            # if str(type(ref.Owner)) == "<type 'Duct'>":
            #     print(ref.Owner)
            #     return find_next(ref.Owner)
        elif element.Name == "finish":
            # for connector in connectors:    
            #     for ref in connector.AllRefs:
            #         if str(type(ref.Owner)) == "<type 'Duct'>":
            print("finish")
            return 0
        else:
            for connector in connectors:    
                for ref in connector.AllRefs:
                    if str(type(ref.Owner)) == "<type 'Duct'>" and str(ref.Direction) == "Out":
                        return find_next(ref.Owner)
    except:
        pass

    try:
        print("Duct")
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
    
    # if fitting.Name == "start":
    #     connectors = fitting.MEPModel.ConnectorManager.Connectors
    #     for connector in connectors:
    #         for ref in connector.AllRefs:
    #         	print(ref.Owner)
    #             if str(type(ref.Owner)) == "<type 'Duct'>":
    #                 secondElements.append(ref.Owner)
    #                 #print(ref.Owner)
    #                 if ref.Owner == 1:
    #                 	print("YES " + str(ref.Owner))
    #                 for contr in ref.Owner.ConnectorManager.Connectors:
    #                 	#print(contr.AllRefs)
    #                 	for i in contr.AllRefs:
    #                 		#print(i.Owner)
    #                 		if str(type(i.Owner)) == "<type 'FamilyInstance'>":
    #                 			if str(i.Direction) == "Out":
    #                 				pass