import bpy

from Frame_Ranger import Utility_Function
from Frame_Ranger.Utility_Function import Timeline_Marker_Function

class FR_OT_TMM_Move_To_Marker(bpy.types.Operator):
    """Click to Move to Marker (Shift Click to also Frame View)"""

    bl_idname = "fr_tmm.move_to_timeline_marker"
    bl_label = "Move To Timeline Marker"
    bl_options = {'UNDO', 'REGISTER'}
    
    Index : bpy.props.IntProperty()

    def invoke(self, context, event):

        if event.shift:
            self.view = True
        else:
            self.view = False

        return self.execute(context)


    def execute(self, context):

        scn = context.scene
        
        Timeline_Marker_Function.move_frame_to_timeline_marker_by_index(self.Index, scn, view=self.view)

        Utility_Function.update_UI()

        return {'FINISHED'}


classes = [FR_OT_TMM_Move_To_Marker]


def register():

    for cls in classes:
        bpy.utils.register_class(cls)



def unregister():

    for cls in classes:
        bpy.utils.unregister_class(cls)



if __name__ == "__main__":
    register()
