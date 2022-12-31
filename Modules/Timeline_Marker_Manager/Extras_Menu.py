import bpy
from Frame_Ranger import Utility_Function

class FR_MT_TMM_Extra_Menu(bpy.types.Menu):
    bl_label = "Timeline Marker List Extras Menu"
    bl_idname = "OBJECT_MT_fr_tmm_extra"

    def draw(self, context):

        layout = self.layout
        scn = context.scene
        obj = context.object

        preferences = Utility_Function.get_addon_preferences()

        layout.operator("fr_tmm.io_import_markers", text="Import Timeline Markers", icon="IMPORT")
        layout.operator("fr_tmm.io_export_markers", text="Export Timeline Markers", icon="EXPORT")
        layout.separator()
        layout.operator("fr_tmm.sort_timeline_markers", text="Sort Timeline Markers", icon="SORTALPHA")
        layout.operator("fr_tmm.batch_rename_markers", text="Batch Rename Timeline Markers", icon="SORTALPHA")
        layout.separator()
        layout.operator("fr_tmm.bind_cameras_to_markers_by_name", text="Bind Cameras to Markers By Name", icon="VIEW_CAMERA")
        layout.operator("fr_tmm.remove_non_binded_camera", text="Remove Non Binded Camera", icon="VIEW_CAMERA")
        layout.separator()
        layout.operator("fr_tmm.clean_markers", text="Clean Overlapped Timeline Markers", icon="BRUSH_DATA")
        layout.operator("fr_tmm.clear_markers", text="Clear Timeline Markers", icon="TRASH")
        layout.operator("fr_tmm.remove_timeline_markers_by_name", text="Remove Timeline Markers By Name", icon="TRASH")


class FR_MT_TMM_Icon_Expose_Menu(bpy.types.Menu):
    bl_label = "Timeline Marker List Icon Expose Menu"
    bl_idname = "OBJECT_MT_fr_tmm_icon_expose"

    def draw(self, context):


        scn = context.scene
        obj = context.object
        layout = self.layout

        preferences = Utility_Function.get_addon_preferences()


        options = [
            ("OAM_tmarker_ICON_Move_To", "Move to", "MARKER_HLT"),
            ("OAM_tmarker_ICON_Selection", "Selection", None),
            ("OAM_tmarker_ICON_Frame", "Frame", None),
            ("OAM_tmarker_ICON_Camera", "Camera", "CAMERA_DATA"),
            ("OAM_tmarker_ICON_Remove", "Remove", "TRASH"),
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








classes = [FR_MT_TMM_Extra_Menu, FR_MT_TMM_Icon_Expose_Menu]



def register():

    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():

    for cls in classes:
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
