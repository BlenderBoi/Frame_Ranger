import bpy
from Frame_Ranger import Utility_Function
import textwrap

class FR_UL_Timeline_Markers_List(bpy.types.UIList):

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):

        preferences = Utility_Function.get_addon_preferences()
        
        row = layout.row(align=True)
        # row.alignment="LEFT"

        if preferences.OAM_tmarker_ICON_Move_To:
            row.operator("fr_tmm.move_to_timeline_marker", text="", icon = "MARKER_HLT").Index = index
            row.separator()

        if preferences.OAM_tmarker_ICON_Selection:
            row.prop(item, "select", text="", emboss=True)

        row.prop(item, "name", text="", emboss=False)

        row = layout.row(align=True)
        row.alignment="RIGHT"

        if preferences.OAM_tmarker_ICON_Camera:

            if item.camera:
                name = item.camera.name

                set_marker = row.operator("fr_tmm.set_marker_camera", text=name, icon="OUTLINER_OB_CAMERA")
                set_marker.Index = index

                remove_cam = row.operator("fr_tmm.remove_marker_camera", text="", icon="X")
                remove_cam.Index = index

                row.separator()
            else:
                row.operator("fr_tmm.set_marker_camera", text="Set Camera", icon="EYEDROPPER").Index = index
                row.separator()

            # row.prop(item, "camera", text="", icon="CAMERA_DATA")







        if preferences.OAM_tmarker_ICON_Frame:
            row.scale_x = 1
            row.prop(item, "frame", text="", emboss=True)
            # row.separator()




        if preferences.OAM_tmarker_ICON_Remove:
            row.operator("fr_tmm.remove_timeline_marker", text="", icon = "TRASH").Index = index



classes = [FR_UL_Timeline_Markers_List]


def register():

    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():

    for cls in classes:
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()
