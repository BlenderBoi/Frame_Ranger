import bpy

from Frame_Ranger import Utility_Function
from Frame_Ranger.Utility_Function import OAM_Functions

ENUM_Mode = [("DOWN", "Down", "Down"),("UP", "Up", "Up")]


class FR_OT_OAM_LIST_Reorder_Action_Slot(bpy.types.Operator):
    """Reorder Action Slot"""
    bl_idname = "fr_oam.reorder_action_slot"
    bl_label = "Reorder Action Slot"
    bl_options = {"REGISTER", "UNDO"}

    index: bpy.props.IntProperty()
    mode: bpy.props.EnumProperty(items=ENUM_Mode)

    target_object: bpy.props.StringProperty()

    def execute(self, context):


        scn = context.scene
        obj = bpy.data.objects.get(self.target_object) 


        if obj is not None:
            action_list_helper = OAM_Functions.Action_List_Helper(obj)

            if self.mode == "DOWN":

                action_list_helper.move_active_down(update_index=True, sync=True)

            if self.mode == "UP":

                action_list_helper.move_active_up(update_index=True, sync=True)

        Utility_Function.update_UI()
        return {'FINISHED'}





classes = [FR_OT_OAM_LIST_Reorder_Action_Slot]


def register():

    for cls in classes:
        bpy.utils.register_class(cls)



def unregister():

    for cls in classes:
        bpy.utils.unregister_class(cls)



if __name__ == "__main__":
    register()
