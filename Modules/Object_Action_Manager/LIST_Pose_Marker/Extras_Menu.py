import bpy
from Frame_Ranger import Utility_Function

from Frame_Ranger.Utility_Function import Pose_Marker_Functions
from bpy.types import Pose

class FR_MT_PMM_Extra_Menu(bpy.types.Menu):
    bl_label = "Pose Marker List Extras Menu"
    bl_idname = "OBJECT_MT_fr_pmm_extra"

    def draw(self, context):

        layout = self.layout
        scn = context.scene

        action = Pose_Marker_Functions.MENU_ACTION

        if action is not None:
            action_name = action.name

            preferences = Utility_Function.get_addon_preferences()

            op = layout.operator("fr_pmm.io_import_markers", text="Import Pose Markers", icon="IMPORT")
            op.target_action = action_name

            op = layout.operator("fr_pmm.io_export_markers", text="Export Pose Markers", icon="EXPORT")
            op.target_action = action_name

            op = layout.separator()

            # op = layout.operator("fr_pmm.sort_pose_markers", text="Sort Pose Markers", icon="SORTALPHA")
            # op.target_action = action_name

            op = layout.operator("fr_pmm.batch_rename_markers", text="Batch Rename Markers", icon="SORTALPHA")
            op.target_action = action_name

            op = layout.separator()

            op = layout.operator("fr_pmm.clean_markers", text="Clean Overlapped Pose Markers", icon="BRUSH_DATA")
            op.target_action = action_name

            op = layout.operator("fr_pmm.clear_markers", text="Clear Markers", icon="TRASH")
            op.target_action = action_name

            op = layout.operator("fr_pmm.remove_pose_markers_by_name", text="Remove Pose Markers By Name", icon="TRASH")
            op.target_action = action_name

            layout.separator()

            # op = layout.operator("fr_pmm.find_and_set_marker_as_range", text="Find Range Markers", icon="VIEWZOOM")
            # op.target_action = action.name
            # op.all_action = False

class FR_MT_PMM_Icon_Expose_Menu(bpy.types.Menu):
    bl_label = "Pose Marker List Icon Expose Menu"
    bl_idname = "OBJECT_MT_fr_pmm_icon_expose"

    def draw(self, context):


        scn = context.scene
        obj = context.object
        layout = self.layout

        preferences = Utility_Function.get_addon_preferences()


        options = [
            ("OAM_pmarker_ICON_Move_To", "Move to", "PMARKER_ACT"),
            ("OAM_pmarker_ICON_Selection", "Selection", None),
            ("OAM_pmarker_ICON_Frame", "Frame", None),
            ("OAM_pmarker_ICON_Camera", "Camera", "CAMERA_DATA"),
            ("OAM_pmarker_ICON_Remove", "Remove", "TRASH"),
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








classes = [FR_MT_PMM_Extra_Menu, FR_MT_PMM_Icon_Expose_Menu]



def register():

    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():

    for cls in classes:
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
