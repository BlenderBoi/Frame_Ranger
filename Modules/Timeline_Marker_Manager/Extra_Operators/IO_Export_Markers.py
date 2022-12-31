import bpy
import bpy_extras
from Frame_Ranger import Utility_Function
from Frame_Ranger.Utility_Function import Timeline_Marker_Function


class FR_OT_TMM_IO_Export_Markers(bpy.types.Operator, bpy_extras.io_utils.ExportHelper):

    bl_idname = "fr_tmm.io_export_markers"
    bl_label = "Export Markers"
    bl_description = "Export Markers"
    bl_options = {'UNDO', 'REGISTER'}
    
    filename_ext = ".marker"


    filter_glob: bpy.props.StringProperty(
        default="*.marker",
        options={'HIDDEN'},
        maxlen=255,  # Max internal buffer length, longer would be clamped.
    )


    def execute(self, context):


        scn = context.scene

        if scn:
            Markers = scn.timeline_markers

            Timeline_Marker_Function.export_markers(self.filepath, Markers)
            Utility_Function.update_UI()
        return {'FINISHED'}




def export_menu_draw(self, context):

    preferences = Utility_Function.get_addon_preferences()

    if preferences.SHOW_IO_Timeline_Markers:
        self.layout.operator("fr_tmm.io_export_markers", text="Timeline Markers (.marker)")



classes = [FR_OT_TMM_IO_Export_Markers]


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
