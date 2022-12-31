from . import Base_Panel
from Frame_Ranger import Utility_Function
import bpy

Master_Panel = Base_Panel.FR_PT_TU_Frame_Range_Remapper_Panel

class FR_PT_Remapper_Panel_VIEW3D(Master_Panel):

    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Frame Ranger"

    @classmethod
    def poll(self, context):
    
        preferences = Utility_Function.get_addon_preferences()
        
        if preferences.PANEL_Frame_Remapper:
            return preferences.PANEL_Frame_Remapper_Side_Panel
        else:
            return False


class FR_PT_Remapper_Panel_GRAPH(Master_Panel):

    bl_space_type = 'GRAPH_EDITOR'
    bl_region_type = 'UI'
    bl_category = "Frame Ranger"

    @classmethod
    def poll(self, context):
    
        preferences = Utility_Function.get_addon_preferences()
        
        if preferences.PANEL_Frame_Remapper:
            return preferences.PANEL_Frame_Remapper_Side_Panel
        else:
            return False



class FR_PT_Remapper_Panel_DOPESHEET(Master_Panel):

    bl_space_type = 'DOPESHEET_EDITOR'
    bl_region_type = 'UI'
    bl_category = "Frame Ranger"


    @classmethod
    def poll(self, context):
    
        preferences = Utility_Function.get_addon_preferences()
        
        if preferences.PANEL_Frame_Remapper:
            return preferences.PANEL_Frame_Remapper_Side_Panel
        else:
            return False

class FR_PT_Remapper_Panel_SEQUENCER(Master_Panel):

    bl_space_type = 'SEQUENCE_EDITOR'
    bl_region_type = 'UI'
    bl_category = "Frame Ranger"


    @classmethod
    def poll(self, context):
    
        preferences = Utility_Function.get_addon_preferences()
        
        if preferences.PANEL_Frame_Remapper:
            return preferences.PANEL_Frame_Remapper_Side_Panel
        else:
            return False


class FR_PT_Remapper_Panel_NLA(Master_Panel):

    bl_space_type = 'NLA_EDITOR'
    bl_region_type = 'UI'
    bl_category = "Frame Ranger"

    @classmethod
    def poll(self, context):
    
        preferences = Utility_Function.get_addon_preferences()
        
        if preferences.PANEL_Frame_Remapper:
            return preferences.PANEL_Frame_Remapper_Side_Panel
        else:
            return False

class FR_PT_Remapper_Panel_OUTPUT_PROPERTIES(Master_Panel):

    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "output"

    @classmethod
    def poll(self, context):
    
        preferences = Utility_Function.get_addon_preferences()
        
        if preferences.PANEL_Frame_Remapper:
            return preferences.PANEL_Frame_Remapper_Output_Properties_Panel
        else:
            return False






classes = [
    FR_PT_Remapper_Panel_OUTPUT_PROPERTIES,
    FR_PT_Remapper_Panel_VIEW3D, 
    FR_PT_Remapper_Panel_GRAPH, 
    FR_PT_Remapper_Panel_DOPESHEET, 
    FR_PT_Remapper_Panel_SEQUENCER, 
    FR_PT_Remapper_Panel_NLA
]
