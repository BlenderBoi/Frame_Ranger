import bpy
import bpy_extras
import pathlib

from Frame_Ranger import Utility_Function
from Frame_Ranger.Utility_Function import Timeline_Marker_Function


class FR_OT_TMM_IO_Export_Markers(bpy.types.Operator, bpy_extras.io_utils.ImportHelper):

    bl_idname = "fr_tmm.io_import_markers"
    bl_label = "Import Markers"
    bl_description = "Import Markers"
    bl_options = {'UNDO', 'REGISTER'}
    
    filename_ext = ".marker"


    filter_glob: bpy.props.StringProperty(
        default="*.marker",
        options={'HIDDEN'},
        maxlen=255,  # Max internal buffer length, longer would be clamped.
    )

    find_bind: bpy.props.BoolProperty(name="Find and Bind Camera", default=True)

    def execute(self, context):


        scn = context.scene

        if scn:


            missing_cameras = Timeline_Marker_Function.import_markers(self.filepath, self.find_bind)

            if len(missing_cameras) > 0:

                report = "{} is missing and is not bind to imported markers".format(", ".join(missing_cameras))

                self.report({"INFO"}, report)

        Utility_Function.update_UI()
        return {'FINISHED'}


def import_menu_draw(self, context):

    preferences = Utility_Function.get_addon_preferences()

    if preferences.SHOW_IO_Timeline_Markers:

        self.layout.operator("fr_tmm.io_import_markers", text="Timeline Markers (.marker)")



classes = [FR_OT_TMM_IO_Export_Markers]


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
