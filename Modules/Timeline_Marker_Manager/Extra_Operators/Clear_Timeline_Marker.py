import bpy
from Frame_Ranger import Utility_Function
from Frame_Ranger.Utility_Function import Timeline_Marker_Function


class FR_OT_TMM_Clear_Markers(bpy.types.Operator):

    bl_idname = "fr_tmm.clear_markers"
    bl_label = "Clear Markers"
    bl_description = "Clear Markers"
    bl_options = {'UNDO', 'REGISTER'}
    

    def execute(self, context):

        scn = context.scene

        Timeline_Marker_Function.clear_timeline_markers(scn)

        Utility_Function.update_UI()

        return {'FINISHED'}


classes = [FR_OT_TMM_Clear_Markers]


def register():

    for cls in classes:
        bpy.utils.register_class(cls)



def unregister():

    for cls in classes:
        bpy.utils.unregister_class(cls)



if __name__ == "__main__":
    register()
