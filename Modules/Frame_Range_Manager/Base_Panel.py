
import bpy

from Frame_Ranger import Utility_Function
from Frame_Ranger.Utility_Function import FRM_Functions

class FR_PT_Frame_Range_Manager_Base(bpy.types.Panel):
    bl_label = "Frame Range Manager"

    @classmethod
    def poll(self, context):
        preferences = Utility_Function.get_addon_preferences()
        if preferences.PANEL_Frame_Range_Manager:
            return True

    def draw(self, context):

        layout = self.layout
        
        col = layout.column(align=True)
        scn = context.scene



        if FRM_Functions.get_set_size() > 0:
            if FRM_Functions.get_set_size() > FRM_Functions.get_set_index() and FRM_Functions.get_set_index() >= 0:
                row = col.row()
                self.draw_frame_range_manager(row)
                self.draw_frame_range_manager_list_operator(row)
            else:
                box = layout.box()
                box.label(text="Invalid Active Frame Range Set Index", icon="ERROR") 
                box = layout.box()
                box.label(text="Please Pick a Frame Range Set", icon="INFO") 
                row = layout.row()
                self.draw_frame_range_set_list(box)

        else:
            #Create New Frame Range Set
            box = layout.box()
            box.label(text="No Frame Range Set Found", icon="INFO") 
            box.operator("fr_frm.add_frame_range_set", text="Add Frame Range Set", icon = "ADD")



        box = layout.box()
        if Utility_Function.draw_subpanel(box, "Frame Range Set", scn, "FRM_Set_Show"):
            row = box.row()
            self.draw_frame_range_set_list(row)
            self.draw_frame_range_set_list_operator(row)




    def draw_frame_range_manager(self, layout):
        active_set = FRM_Functions.get_active_set() 
        layout.template_list("FR_UL_Frame_Range_Manager_List", "", active_set, "FRM", active_set, "FRM_Index")
    
    def draw_frame_range_manager_list_operator(self, layout):

        index = FRM_Functions.get_fr_index()

        col = layout.column(align=True) 
        operator = col.operator("fr_frm.add_frame_range", text="", icon = "ADD")

        col.operator("fr_frm.remove_frame_range", text="", icon = "REMOVE").index = index
        col.separator()

        col.menu("OBJECT_MT_fr_frm_icon_expose", icon="VIS_SEL_11", text="")
        col.menu("OBJECT_MT_fr_frm_extra", icon="DOWNARROW_HLT", text="")

        col.separator()
        reorder_Up = col.operator("fr_frm.reorder_frame_range", text="", icon = "TRIA_UP")
        reorder_Up.index = index 
        reorder_Up.mode = "UP"

        reorder_Down = col.operator("fr_frm.reorder_frame_range", text="", icon = "TRIA_DOWN")
        reorder_Down.index = index 
        reorder_Down.mode = "DOWN"



    def draw_frame_range_set_list(self, layout):

        scn = bpy.context.scene
        layout.template_list("FR_UL_Frame_Range_Set_List", "", scn, "FRM_Set", scn, "FRM_Set_Index")
    
    def draw_frame_range_set_list_operator(self, layout):

        index = FRM_Functions.get_set_index()

        col = layout.column(align=True) 
        operator = col.operator("fr_frm.add_frame_range_set", text="", icon = "ADD")

        col.operator("fr_frm.remove_frame_range_set", text="", icon = "REMOVE").index = index
        col.separator()

        col.menu("OBJECT_MT_fr_frs_icon_expose", icon="VIS_SEL_11", text="")
        col.menu("OBJECT_MT_fr_frs_extra", icon="DOWNARROW_HLT", text="")

        col.separator()
        reorder_Up = col.operator("fr_frm.reorder_frame_range_set", text="", icon = "TRIA_UP")
        reorder_Up.index = index 
        reorder_Up.mode = "UP"

        reorder_Down = col.operator("fr_frm.reorder_frame_range_set", text="", icon = "TRIA_DOWN")
        reorder_Down.index = index 
        reorder_Down.mode = "DOWN"


