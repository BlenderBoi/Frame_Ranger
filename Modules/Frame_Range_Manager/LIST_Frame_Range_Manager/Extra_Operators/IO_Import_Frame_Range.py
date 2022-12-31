import bpy
import bpy_extras
import pathlib


from Frame_Ranger import Utility_Function
from Frame_Ranger.Utility_Function import FRM_Functions



mode =[("CURRENT","Add to Current","Add to Current Frame Set"),("NEW","New Frame Range Set","As a New Frame Set")]

class FR_OT_FRM_IO_Import_Frame_Ranges(bpy.types.Operator, bpy_extras.io_utils.ImportHelper):

    bl_idname = "fr_frm.io_import_frame_ranges"
    bl_label = "Import Frame Ranges"
    bl_description = "Import Frame Ranges"
    bl_options = {'UNDO', 'REGISTER'}

    filename_ext = ".fr"


    filter_glob: bpy.props.StringProperty(
        default="*.fr",
        options={'HIDDEN'},
        maxlen=255,  # Max internal buffer length, longer would be clamped.
    )

    mode: bpy.props.EnumProperty(items=mode, default ="CURRENT")

    def draw(self, context):

        layout = self.layout
        layout.prop(self, "mode", text="Mode")

    def execute(self, context):





        name = pathlib.Path(self.filepath).stem

        if self.mode == "NEW":
            FRM_Functions.add_set(name)



        FRM_Functions.import_frm(self.filepath)

        return {'FINISHED'}


def import_menu_draw(self, context):

    preferences = Utility_Function.get_addon_preferences()

    if preferences.SHOW_IO_Frame_Range:
        self.layout.operator("fr_frm.io_import_frame_ranges", text="Frame Range (.fr)")



classes = [FR_OT_FRM_IO_Import_Frame_Ranges]


def register():

    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.TOPBAR_MT_file_import.append(import_menu_draw)

def unregister():

    for cls in classes:
        bpy.utils.unregister_class(cls)

    bpy.types.TOPBAR_MT_file_import.remove(import_menu_draw)

if __name__ == "__main__":
    register()
