import bpy


from Frame_Ranger import Utility_Function

from Frame_Ranger.Utility_Function import OAM_Functions
from Frame_Ranger.Utility_Function import Pose_Marker_Functions


class FR_OT_PMM_Remove_Pose_Marker(bpy.types.Operator):
    """Remove Pose Marker"""
    bl_idname = "fr_pmm.remove_pose_marker"
    bl_label = "Remove Pose Marker"
    bl_options = {"REGISTER", "UNDO"}

    index: bpy.props.IntProperty()
    target_action: bpy.props.StringProperty()

    def execute(self, context):


        action = bpy.data.actions.get(self.target_action) 

        Pose_Marker_Functions.remove_pose_marker(self.index, action)

        Utility_Function.update_UI()

        return {'FINISHED'}

classes = [FR_OT_PMM_Remove_Pose_Marker]


def register():

    for cls in classes:
        bpy.utils.register_class(cls)



def unregister():

    for cls in classes:
        bpy.utils.unregister_class(cls)



if __name__ == "__main__":
    register()
