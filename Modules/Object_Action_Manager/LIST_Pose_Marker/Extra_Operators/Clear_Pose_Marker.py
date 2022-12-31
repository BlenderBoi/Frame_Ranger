import bpy
from Frame_Ranger import Utility_Function

from Frame_Ranger.Utility_Function import OAM_Functions
from Frame_Ranger.Utility_Function import Pose_Marker_Functions

class FR_OT_PMM_Clear_Markers(bpy.types.Operator):

    bl_idname = "fr_pmm.clear_markers"
    bl_label = "Clear Markers"
    bl_description = "Clear Markers"
    bl_options = {'UNDO', 'REGISTER'}
    
    target_action: bpy.props.StringProperty()

    def execute(self, context):

        scn = context.scene

        
        action = bpy.data.actions.get(self.target_action) 

        Pose_Marker_Functions.clear_pose_markers(action)

        Utility_Function.update_UI()

        return {'FINISHED'}


classes = [FR_OT_PMM_Clear_Markers]


def register():

    for cls in classes:
        bpy.utils.register_class(cls)



def unregister():

    for cls in classes:
        bpy.utils.unregister_class(cls)



if __name__ == "__main__":
    register()
