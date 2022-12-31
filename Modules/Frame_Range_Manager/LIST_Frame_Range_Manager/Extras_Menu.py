import bpy
from Frame_Ranger import Utility_Function

class FR_MT_FRM_Extra_Menu(bpy.types.Menu):
    bl_label = "Frame Range Manager Extras Menu"
    bl_idname = "OBJECT_MT_fr_frm_extra"

    def draw(self, context):

        layout = self.layout
        scn = context.scene
        obj = context.object

        preferences = Utility_Function.get_addon_preferences()
        layout.operator("fr_frm.clear_frame_range", text="Clear Frame Range", icon="TRASH")
        layout.operator("fr_frm.batch_rename_frame_ranges", text="Batch Rename", icon="SORTALPHA")
        layout.operator("fr_frm.sort_frame_range", text="Sort Frame Range", icon="SORTALPHA")
        layout.separator()
        layout.operator("fr_frm.io_export_frame_ranges", text="Export Frame Range", icon="IMPORT")
        layout.operator("fr_frm.io_import_frame_ranges", text="Import Frame Range", icon="EXPORT")
        layout.separator()
        layout.operator("fr_frm.markers_from_frame_range", text="Markers From Frame Range", icon="MARKER_HLT")
        layout.operator("fr_frm.frame_ranges_from_markers", text="Frame Ranges From Markers", icon="TIME")

class FR_MT_FRM_Icon_Expose_Menu(bpy.types.Menu):
    bl_label = "Frame Range Manager Icon Expose Menu"
    bl_idname = "OBJECT_MT_fr_frm_icon_expose"

    def draw(self, context):

        scn = context.scene
        obj = context.object
        layout = self.layout

        preferences = Utility_Function.get_addon_preferences()

        options = [
            ("FRM_ICON_Set_Range", "Set Range", "TIME"),                #
            ("FRM_ICON_Frame_Range", "Frame Range", None),                                #
            ("FRM_ICON_Remove", "Remove Slot", "TRASH"),                            #
        ]


        for option in options:
            
            if option[2]:

                row = layout.row(align=True)
                row.label(text="", icon=option[2])
                row.prop(preferences, option[0], text=option[1], icon=option[2])
                row.separator()
            else:
                row = layout.row(align=True)
                row.label(text="", icon="DOT")
                row.prop(preferences, option[0], text=option[1])
                row.separator()



class FR_MT_FRS_Extra_Menu(bpy.types.Menu):
    bl_label = "Frame Range Set Extras Menu"
    bl_idname = "OBJECT_MT_fr_frs_extra"

    def draw(self, context):

        layout = self.layout
        scn = context.scene
        obj = context.object

        preferences = Utility_Function.get_addon_preferences()
        layout.operator("fr_frm.batch_rename_frame_range_sets", text="Batch Rename", icon="SORTALPHA")
        layout.operator("fr_frm.sort_frame_range_set", text="Sort", icon="SORTALPHA")
        layout.operator("fr_frm.clear_frame_range_set", text="Clear", icon="TRASH")
        layout.operator("fr_frm.clear_empty_frame_range_set", text="Clear Empty", icon="TRASH")


class FR_MT_FRS_Icon_Expose_Menu(bpy.types.Menu):
    bl_label = "Frame Range Set Icon Expose Menu"
    bl_idname = "OBJECT_MT_fr_frs_icon_expose"

    def draw(self, context):

        scn = context.scene
        obj = context.object
        layout = self.layout

        preferences = Utility_Function.get_addon_preferences()

        options = [
            ("FRS_ICON_Remove", "Remove Slot", "TRASH"),                            #
        ]

        for option in options:
            
            if option[2]:

                row = layout.row(align=True)
                row.label(text="", icon=option[2])
                row.prop(preferences, option[0], text=option[1], icon=option[2])
                row.separator()
            else:
                row = layout.row(align=True)
                row.label(text="", icon="DOT")
                row.prop(preferences, option[0], text=option[1])
                row.separator()






classes = [FR_MT_FRM_Extra_Menu, FR_MT_FRS_Extra_Menu, FR_MT_FRM_Icon_Expose_Menu, FR_MT_FRS_Icon_Expose_Menu]



def register():

    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():

    for cls in classes:
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
