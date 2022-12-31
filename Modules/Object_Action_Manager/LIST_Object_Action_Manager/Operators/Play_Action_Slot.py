import bpy

from Frame_Ranger import Utility_Function
from Frame_Ranger.Utility_Function import OAM_Functions

#GAM add LAM to Selected Object
#Reorder LAM
#SlotName
#Custom Range
#Range and Mode on Icon List

#Set/Change Action Slot Action


class FR_OT_OAM_Play_Action_Slot(bpy.types.Operator):
    """Click to Play and Pause on the same action, Shift Click to Play from the start of action"""
    bl_idname = "fr_oam.play_action_slot"
    bl_label = "Play Action Slot"


    index: bpy.props.IntProperty()
    pause: bpy.props.BoolProperty()

    target_object: bpy.props.StringProperty()

    def invoke(self, context, event):

        if event.shift:
            self.pause = False
        else:
            self.pause = True

        return self.execute(context)

    def execute(self, context):

        scn = context.scene
        obj = bpy.data.objects.get(self.target_object) 


        if obj:

            action_list_helper = OAM_Functions.Action_List_Helper(obj)
            slot = action_list_helper.get_slot(self.index)
            current_index = action_list_helper.get_active_index() 


            action_list_helper.set_active_index(self.index, sync=True)


            if self.pause:
                if action_list_helper.get_active_index() == current_index:

                    bpy.ops.screen.animation_play()

                else:
                    scn.frame_current = scn.frame_start
                    bpy.ops.screen.animation_cancel()
                    bpy.ops.screen.animation_play()
            else:
                bpy.ops.screen.animation_cancel()
                scn.frame_current = scn.frame_start
                bpy.ops.screen.animation_play()

        return {'FINISHED'}


classes = [FR_OT_OAM_Play_Action_Slot]


def register():

    for cls in classes:
        bpy.utils.register_class(cls)



def unregister():

    for cls in classes:
        bpy.utils.unregister_class(cls)



if __name__ == "__main__":
    register()
