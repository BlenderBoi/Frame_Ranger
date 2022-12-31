import bpy

from Frame_Ranger import Utility_Function

from Frame_Ranger.Utility_Function import OAM_Functions
from Frame_Ranger.Utility_Function import Pose_Marker_Functions



class FR_OT_PMM_Move_To_Marker(bpy.types.Operator):
    """Click to Move to Marker (Shift Click to also Frame View)"""
    bl_idname = "fr_pmm.move_to_pose_marker"
    bl_label = "Move To Pose Marker"
    bl_options = {'UNDO', 'REGISTER'}
    
    index : bpy.props.IntProperty()
    target_action: bpy.props.StringProperty()
    view: bpy.props.BoolProperty()

    def invoke(self, context, event):

        if event.shift:
            self.view = True
        else:
            self.view = False

        return self.execute(context)




    def execute(self, context):

        action = bpy.data.actions.get(self.target_action) 
        Pose_Marker_Functions.move_frame_to_pose_marker_by_index(self.index, action, view=self.view)

        Utility_Function.update_UI()

        return {'FINISHED'}


classes = [FR_OT_PMM_Move_To_Marker]


def register():

    for cls in classes:
        bpy.utils.register_class(cls)



def unregister():

    for cls in classes:
        bpy.utils.unregister_class(cls)



if __name__ == "__main__":
    register()
