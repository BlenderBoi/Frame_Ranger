from Frame_Ranger import Utility_Function
# from Frame_Ranger.Utility_Function import OAM_Util

from Frame_Ranger.Utility_Function import OAM_Functions
from Frame_Ranger.Draw_Helper import Draw_Action_List

import bpy

class FR_PT_Object_Action_Manager_Base(bpy.types.Panel):
    bl_label = "Object Action Manager"


    @classmethod
    def poll(self, context):
        preferences = Utility_Function.get_addon_preferences()
        if preferences.PANEL_Object_Action_Manager:
            return True

    def draw(self, context):
        
        obj = context.object

        layout = self.layout

        Draw_Action_List.draw_list(layout, context, obj, draw_strip=True, draw_action_counter=True)



    # def Draw_Pose_Marker_Listbox(self, context, action, layout):
    #     if action:
    #         row = layout.row()
    #         row.template_list("FR_UL_Pose_Markers_List", "", action, "pose_markers", action, "pose_markers_index")
    #
    #
    # def Draw_Pose_Marker_Listbox_Operators(self, context, action, layout):
    #     obj = context.object
    #     obj_name = obj.name
    #
    #     col = layout.column(align=True)
    #     op = col.operator("fr_pmm.add_pose_marker", text="", icon = "ADD")
    #     op.target_object = obj_name
    #
    #
    #     op = col.operator("fr_pmm.remove_pose_marker", text="", icon = "REMOVE")
    #     op.Index = action.pose_markers_index
    #     op.target_object = obj_name
    #
    #     col.separator()
    #     col.menu("OBJECT_MT_fr_pmm_icon_expose", text="", icon="FILTER")
    #     col.menu("OBJECT_MT_fr_pmm_extra", text="", icon="DOWNARROW_HLT")
    #     col.separator()
    #     operator = col.operator("fr_pmm.reorder_pose_marker", text="", icon = "TRIA_UP")
    #     operator.Index = action.pose_markers_index
    #     operator.Mode= "UP" 
    #     operator.target_object = obj_name
    #
    #     operator = col.operator("fr_pmm.reorder_pose_marker", text="", icon = "TRIA_DOWN")
    #     operator.Index = action.pose_markers_index
    #     operator.Mode= "DOWN" 
    #     operator.target_object = obj_name
    #
    #
    # def Draw_Pose_Marker_List(self, context, action, layout):
    #
    #     preferences = Utility_Function.get_addon_preferences()
    #     if Utility_Function.draw_subpanel(layout, "Pose Markers", preferences, "OAM_pmarker_Show"):
    #         
    #         row = layout.row()
    #         self.Draw_Pose_Marker_Listbox(context, action, row)
    #         self.Draw_Pose_Marker_Listbox_Operators(context, action, row)
    #         
    #         if len(action.pose_markers) > action.pose_markers_index:
    #             active_marker = action.pose_markers[action.pose_markers_index]
    #             layout.prop(active_marker, "notes", text="Notes") 
    #
    #         OAM_Functions.draw_show_pose_markers(context, layout)
    #
