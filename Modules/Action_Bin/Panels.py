from . import Base_Panel
from Frame_Ranger import Utility_Function
import bpy

Master_Panel = Base_Panel.FR_PT_Action_Bin_Base


class FR_PT_AB_Panel_SCENE_PROPERTIES(Master_Panel):

    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "scene"

    @classmethod
    def poll(self, context):
        preferences = Utility_Function.get_addon_preferences()
        if preferences.PANEL_Action_Bin:
            if preferences.PANEL_Action_Bin_Scene_Properties_Panel:
                return True
        
class FR_PT_AB_Panel_VIEW3D(Master_Panel):

    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Frame Ranger"

    @classmethod
    def poll(self, context):
        preferences = Utility_Function.get_addon_preferences()
        if preferences.PANEL_Action_Bin:
            if preferences.PANEL_Action_Bin_Side_Panel:
                return True

class FR_PT_AB_Panel_GRAPH(Master_Panel):


    bl_space_type = 'GRAPH_EDITOR'
    bl_region_type = 'UI'
    bl_category = "Frame Ranger"


    @classmethod
    def poll(self, context):
        preferences = Utility_Function.get_addon_preferences()
        if preferences.PANEL_Action_Bin:
            if preferences.PANEL_Action_Bin_Side_Panel:
                return True



class FR_PT_AB_Panel_DOPESHEET(Master_Panel):

    bl_space_type = 'DOPESHEET_EDITOR'
    bl_region_type = 'UI'
    bl_category = "Frame Ranger"


    @classmethod
    def poll(self, context):
        preferences = Utility_Function.get_addon_preferences()
        if preferences.PANEL_Action_Bin:
            if preferences.PANEL_Action_Bin_Side_Panel:
                return True



class FR_PT_AB_Panel_SEQUENCER(Master_Panel):

    bl_space_type = 'SEQUENCE_EDITOR'
    bl_region_type = 'UI'
    bl_category = "Frame Ranger"

    @classmethod
    def poll(self, context):
        preferences = Utility_Function.get_addon_preferences()
        if preferences.PANEL_Action_Bin:
            if preferences.PANEL_Action_Bin_Side_Panel:
                return True



class FR_PT_AB_Panel_NLA(Master_Panel):

    bl_space_type = 'NLA_EDITOR'
    bl_region_type = 'UI'
    bl_category = "Frame Ranger"


    @classmethod
    def poll(self, context):
        preferences = Utility_Function.get_addon_preferences()
        if preferences.PANEL_Action_Bin:
            if preferences.PANEL_Action_Bin_Side_Panel:
                return True


classes = [
    FR_PT_AB_Panel_SCENE_PROPERTIES,
    FR_PT_AB_Panel_VIEW3D, 
    FR_PT_AB_Panel_GRAPH, 
    FR_PT_AB_Panel_DOPESHEET, 
    FR_PT_AB_Panel_SEQUENCER, 
    FR_PT_AB_Panel_NLA
]
