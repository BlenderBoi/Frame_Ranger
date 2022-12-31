import bpy
import bpy_extras
from Frame_Ranger import Utility_Function

from Frame_Ranger.Utility_Function import OAM_Functions
from Frame_Ranger.Utility_Function import Pose_Marker_Functions



class FR_OT_PMM_IO_Export_Markers(bpy.types.Operator, bpy_extras.io_utils.ExportHelper):

    bl_idname = "fr_pmm.io_export_markers"
    bl_label = "Export Markers"
    bl_description = "Export Markers"
    bl_options = {'UNDO', 'REGISTER'}
    
    target_action: bpy.props.StringProperty()


    filename_ext = ".marker"


    filter_glob: bpy.props.StringProperty(
        default="*.marker",
        options={'HIDDEN'},
        maxlen=255,  # Max internal buffer length, longer would be clamped.
    )


    def execute(self, context):


        action = bpy.data.actions.get(self.target_action) 

        if action:
            Markers = action.pose_markers

            Pose_Marker_Functions.export_markers(self.filepath, Markers)
            Utility_Function.update_UI()
        return {'FINISHED'}




# def export_menu_draw(self, context):
#     obj = context.object
#
#     if obj is not None:
#         action_list_helper = OAM_Functions.Action_List_Helper(obj)
#         action = action_list_helper.get_active_action()
#
#         if action is not None:
#             op = self.layout.operator("fr_pmm.io_export_markers", text="Export Pose Markers (.marker)")
#             op.target_action = action.name 




classes = [FR_OT_PMM_IO_Export_Markers]


def register():



    for cls in classes:
        bpy.utils.register_class(cls)

    # bpy.types.TOPBAR_MT_file_export.append(export_menu_draw)
    #

def unregister():

    for cls in classes:
        bpy.utils.unregister_class(cls)

    # bpy.types.TOPBAR_MT_file_export.remove(export_menu_draw)

if __name__ == "__main__":
    register()
