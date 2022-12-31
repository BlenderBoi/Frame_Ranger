import bpy
import bpy_extras

from Frame_Ranger import Utility_Function
from Frame_Ranger.Utility_Function import FRM_Functions

class FR_OT_FRM_IO_Export_Frame_Ranges(bpy.types.Operator, bpy_extras.io_utils.ExportHelper):

    bl_idname = "fr_frm.io_export_frame_ranges"
    bl_label = "Export Frame Ranges"
    bl_description = "Export Frame Ranges"
    bl_options = {'UNDO', 'REGISTER'}

    filename_ext = ".fr"


    filter_glob: bpy.props.StringProperty(
        default="*.fr",
        options={'HIDDEN'},
        maxlen=255,  # Max internal buffer length, longer would be clamped.
    )


    def execute(self, context):

        FRM = FRM_Functions.get_fr_list()
        FRM_Functions.export_frm(self.filepath, FRM)

        return {'FINISHED'}




def export_menu_draw(self, context):

    preferences = Utility_Function.get_addon_preferences()

    if preferences.SHOW_IO_Frame_Range:
        self.layout.operator("fr_frm.io_export_frame_ranges", text="Frame Range (.fr)")



classes = [FR_OT_FRM_IO_Export_Frame_Ranges]


def register():



    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.TOPBAR_MT_file_export.append(export_menu_draw)


def unregister():

    for cls in classes:
        bpy.utils.unregister_class(cls)

    bpy.types.TOPBAR_MT_file_export.remove(export_menu_draw)

if __name__ == "__main__":
    register()
