import bpy
import bpy_extras
import pathlib

from Frame_Ranger import Utility_Function

from Frame_Ranger.Utility_Function import OAM_Functions
from Frame_Ranger.Utility_Function import Pose_Marker_Functions


class FR_OT_PMM_IO_Export_Markers(bpy.types.Operator, bpy_extras.io_utils.ImportHelper):

    bl_idname = "fr_pmm.io_import_markers"
    bl_label = "Import Markers"
    bl_description = "Import Markers"
    bl_options = {'UNDO', 'REGISTER'}
    
    target_action: bpy.props.StringProperty()
    filename_ext = ".marker"


    filter_glob: bpy.props.StringProperty(
        default="*.marker",
        options={'HIDDEN'},
        maxlen=255,  # Max internal buffer length, longer would be clamped.
    )

    find_bind: bpy.props.BoolProperty(name="Find and Bind Camera", default=True)

    def execute(self, context):


        action = bpy.data.actions.get(self.target_action) 

        if action is not None:


            missing_cameras = Pose_Marker_Functions.import_markers(action, self.filepath, self.find_bind)

            if len(missing_cameras) > 0:

                report = "{} is missing and is not bind to imported markers".format(", ".join(missing_cameras))

                self.report({"INFO"}, report)

        Utility_Function.update_UI()
        return {'FINISHED'}



# def import_menu_draw(self, context):
#     obj = context.object
#
#     if obj is not None:
#         action_list_helper = OAM_Functions.Action_List_Helper(obj)
#         action = action_list_helper.get_active_action()
#
#         if action is not None:
#             op = self.layout.operator("fr_pmm.io_import_markers", text="Export Markers (.marker)")
#             op.target_action = action.name 



classes = [FR_OT_PMM_IO_Export_Markers]


def register():

    for cls in classes:
        bpy.utils.register_class(cls)

    # bpy.types.TOPBAR_MT_file_import.append(import_menu_draw)

def unregister():

    for cls in classes:
        bpy.utils.unregister_class(cls)

    # bpy.types.TOPBAR_MT_file_import.remove(import_menu_draw)

if __name__ == "__main__":
    register()
