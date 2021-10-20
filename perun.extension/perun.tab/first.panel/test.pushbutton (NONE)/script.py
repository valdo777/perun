# -*- coding: utf-8 -*-

# """This extension add constant parameter values"""

# __doc__ = 'test'

# __title__ = 'test'

# __author__ = 'Vlad Sozutov'

# __min_revit_ver__= 2019
# __max_revit_ver__ = 2020


#---------------------CODE---------------------
#Adding constant parameter values
# from Autodesk.Revit.DB import Transaction, XYZ, Line, ElementTransformUtils
# from Autodesk.Revit.UI.Selection import ObjectType

# doc = __revit__.ActiveUIDocument.Document
# app = __revit__.Application
# uidoc = __revit__.ActiveUIDocument

# el = uidoc.Selection.PickObject()
# print(el)

# t = Transaction(doc, 'This is my new transaction')
# t.Start()

# el = uidoc.Selection.PickObject(ObjectType.Element, "Select something.")

# el_ID = doc.GetElement(el)     

# el_bb = el_ID.get_BoundingBox(doc.ActiveView)

# el_bb_max = el_bb.Max
# el_bb_min = el_bb.Min

# el_bb_center = (el_bb_max + el_bb_min) / 2

# p1 = XYZ(el_bb_center[0], el_bb_center[1], 0)
# p2 = XYZ(el_bb_center[0], el_bb_center[1], 1)
# myLine = Line.CreateBound(p1, p2)

# ElementTransformUtils.RotateElement(doc, el_bb, myLine, 90.0)

# t.Commit()
