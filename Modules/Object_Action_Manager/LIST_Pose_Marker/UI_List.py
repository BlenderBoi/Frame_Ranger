import bpy
from Frame_Ranger import Utility_Function

class FR_UL_Pose_Markers_List(bpy.types.UIList):

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):

        action = item.id_data

        preferences = Utility_Function.get_addon_preferences()
        
        row = layout.row(align=True)
        row.alignment="LEFT"

        if preferences.OAM_pmarker_ICON_Move_To:
            operator = row.operator("fr_pmm.move_to_pose_marker", text="", icon = "PMARKER_ACT")
            operator.index = index
            operator.target_action = action.name

            row.separator()

        if preferences.OAM_pmarker_ICON_Selection:
            row.prop(item, "select", text="", emboss=True)

        row = layout.row(align=True)
        row.alignment="EXPAND"
        row.prop(item, "name", text="", emboss=False)

        row = layout.row(align=True)
        row.alignment="RIGHT"

        if preferences.OAM_pmarker_ICON_Frame:
            row.scale_x = 1
            row.prop(item, "frame", text="", emboss=True)
            # row.separator()

        # if preferences.OAM_pmarker_ICON_Camera:
        #     row.prop(item, "camera", text="", icon="CAMERA_DATA")

        if preferences.OAM_pmarker_ICON_Camera:

            if item.camera:
                operator = row.operator("fr_pmm.set_marker_camera", text=item.camera.name, icon="OUTLINER_OB_CAMERA")
                operator.target_action = action.name
                operator.index = index

                operator = row.operator("fr_pmm.remove_marker_camera", text="", icon="X")
                operator.target_action = action.name
                operator.index = index

                row.separator()
            else:
                operator = row.operator("fr_pmm.set_marker_camera", text="Set Camera", icon="EYEDROPPER")
                operator.target_action = action.name
                operator.index = index
                row.separator()






        if preferences.OAM_pmarker_ICON_Remove:
            operator = row.operator("fr_pmm.remove_pose_marker", text="", icon = "TRASH")
            operator.index = index
            operator.target_action = action.name



classes = [FR_UL_Pose_Markers_List]


def register():

    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():

    for cls in classes:
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()
