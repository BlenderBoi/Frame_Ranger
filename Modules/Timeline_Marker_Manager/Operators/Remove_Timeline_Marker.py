import bpy


from Frame_Ranger import Utility_Function
from Frame_Ranger.Utility_Function import Timeline_Marker_Function



class FR_OT_TMM_Remove_Timeline_Marker(bpy.types.Operator):
    """Remove Timeline Marker"""
    bl_idname = "fr_tmm.remove_timeline_marker"
    bl_label = "Remove Timeline Marker"
    bl_options = {"REGISTER", "UNDO"}

    Index: bpy.props.IntProperty()

    def execute(self, context):

        scn = context.scene

        Timeline_Marker_Function.remove_timeline_marker(self.Index, scn)

        Utility_Function.update_UI()

        return {'FINISHED'}

classes = [FR_OT_TMM_Remove_Timeline_Marker]


def register():

    for cls in classes:
        bpy.utils.register_class(cls)



def unregister():

    for cls in classes:
        bpy.utils.unregister_class(cls)



if __name__ == "__main__":
    register()
