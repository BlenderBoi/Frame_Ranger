from Frame_Ranger import Utility_Function
# from Frame_Ranger.Utility_Function import OAM_Util


import bpy

class FR_PT_Timeline_Marker_Manager_Base(bpy.types.Panel):
    bl_label = "Timeline Marker Manager"

    @classmethod
    def poll(self, context):
        preferences = Utility_Function.get_addon_preferences()
        if preferences.PANEL_Timeline_Marker_Manager:
            return True

    def draw(self, context):

        layout = self.layout
        
        col = layout.column(align=True)

        row = col.row()
        scn = context.scene
        self.Draw_List(context, scn, row)        
        self.Draw_Active_Timeline_Marker_Settings(context, layout)
           
    def Draw_Active_Timeline_Marker_Settings(self, context, layout):

        row = layout.row(align=True)

        scn = context.scene

        if len(scn.timeline_markers) > scn.timeline_markers_index:

            marker = scn.timeline_markers[scn.timeline_markers_index]
            layout.prop(marker, "notes", text="Notes: ") 
   

            if marker.camera:
                set_marker = row.operator("fr_tmm.set_marker_camera", text=marker.camera.name, icon="OUTLINER_OB_CAMERA")
                set_marker.Index = scn.timeline_markers_index

                remove_cam = row.operator("fr_tmm.remove_marker_camera", text="", icon="X")
                remove_cam.Index = scn.timeline_markers_index

                row.separator()
            else:
                row.operator("fr_tmm.set_marker_camera", text="Set Camera", icon="EYEDROPPER").Index = scn.timeline_markers_index 
                row.separator()






    def Draw_Listbox(self, context, scn, layout):
        if scn:
            row = layout.row()
            row.template_list("FR_UL_Timeline_Markers_List", "", scn, "timeline_markers", scn, "timeline_markers_index")


    def Draw_Listbox_Operators(self, context, scn, layout):

        col = layout.column(align=True)
        col.operator("fr_tmm.add_timeline_marker", text="", icon = "ADD")
        col.operator("fr_tmm.remove_timeline_marker", text="", icon = "REMOVE").Index = scn.timeline_markers_index
        col.separator()
        col.menu("OBJECT_MT_fr_tmm_icon_expose", text="", icon="VIS_SEL_11")
        col.menu("OBJECT_MT_fr_tmm_extra", text="", icon="DOWNARROW_HLT")
        col.separator()
        operator = col.operator("fr_tmm.reorder_timeline_marker", text="", icon = "TRIA_UP")
        operator.Index = scn.timeline_markers_index
        operator.Mode= "UP" 
        operator = col.operator("fr_tmm.reorder_timeline_marker", text="", icon = "TRIA_DOWN")
        operator.Index = scn.timeline_markers_index
        operator.Mode= "DOWN" 


    def Draw_List(self, context, scn, layout):

        row = layout.row()
        self.Draw_Listbox(context, scn, row)
        self.Draw_Listbox_Operators(context, scn, row)
        
