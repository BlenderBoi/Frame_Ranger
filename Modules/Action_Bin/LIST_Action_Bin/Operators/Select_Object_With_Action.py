import bpy

from Frame_Ranger import Utility_Function
from Frame_Ranger.Utility_Function import AB_Functions
from Frame_Ranger.Utility_Function import OAM_Functions



class FR_OT_AB_Select_Object_With_Action(bpy.types.Operator):
    """Select Object with Action (Hold Shift to Only Check Active Action)"""
    bl_idname = "fr_ab.select_object_with_action"
    bl_label = "Select Object with Action"
    bl_options = {"REGISTER", "UNDO"}

    index: bpy.props.IntProperty()
    active_only: bpy.props.BoolProperty(default=False)

    def invoke(self, context, event):

        if event.shift:
            self.active_only = True

        return self.execute(context)

    def execute(self, context):

        objects = context.scene.objects
        actions = bpy.data.actions
       

        choosen_objects = [] 

        if len(actions) > self.index:
            check_action = actions[self.index]


            for obj in objects:

                action_list_helper = OAM_Functions.Action_List_Helper(obj)

                if self.active_only:


                    active_action = action_list_helper.get_active_action()
                    actual_action = action_list_helper.get_actual_action()

                    action_checklist = [active_action, actual_action]

                    if check_action in action_checklist:
                        choosen_objects.append(obj)

                else:

                
                    actual_action = action_list_helper.get_actual_action()
                    collected_actions = action_list_helper.collect_action_list()
                    collected_actions.append(actual_action)

                    action_checklist = collected_actions

                    if check_action in action_checklist:
                        choosen_objects.append(obj)



        toogle_check = not any([object.select_get() for object in choosen_objects])

        if len(choosen_objects) > 0:
            context.view_layer.objects.active = choosen_objects[0]

        for object in choosen_objects:
            object.select_set(toogle_check)


        return {'FINISHED'}


classes = [FR_OT_AB_Select_Object_With_Action]


def register():

    for cls in classes:
        bpy.utils.register_class(cls)



def unregister():

    for cls in classes:
        bpy.utils.unregister_class(cls)



if __name__ == "__main__":
    register()
