# coding: utf8
from math import pi, acos

from Autodesk.Revit.DB import Line, ViewSection, XYZ, FilteredElementCollector, Grid, ReferencePlane, FamilyInstance, \
    BuiltInParameter, ElevationMarker, ViewType
from Autodesk.Revit.UI.Selection import ObjectType
from Autodesk.Revit import Exceptions

import rpw
from pyrevit import forms, script


__doc__ = """Сuts the busbar to length, including vertical sections"""
__title__ = "Trim busbar"
__authors__ = ["Vlad Sozutov"]
__highlight__ = 'new'

uidoc = rpw.revit.uidoc
doc = rpw.revit.doc
logger = script.get_logger()

def element_selection():
    try:
        with forms.WarningBar(title="Pick busbar to be cut into segments"):
            reference = uidoc.Selection.PickObject(ObjectType.Element, "Pick reference element")
            return reference.ElementId
    except Exceptions.OperationCanceledException:
        return False

element = doc.GetElement(element_selection())
print(element.Name)
