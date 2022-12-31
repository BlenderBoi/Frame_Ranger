import bpy
from Frame_Ranger import Utility_Function
from Frame_Ranger.Utility_Function import OAM_Functions


class FR_OT_OAM_Select_Object_With_Action(bpy.types.Operator):
    """"Select objects with Action, Click to Check Active Only, Shift Click to Check All Slot"""
    bl_idname = "fr_oam.select_object_with_action"
    bl_label = "Select Object with Action"
    bl_options = {"REGISTER", "UNDO"}

    index: bpy.props.IntProperty()
    target_object: bpy.props.StringProperty()
    check_all: bpy.props.BoolProperty(default=False)

    def invoke(self, context, event):

        if event.shift:
            self.check_all = True 
        else:
            self.check_all = False 

        return self.execute(context)

    def execute(self, context):

        scn = context.scene
        obj = bpy.data.objects.get(self.target_object) 

        chosen_objects = []

        if obj:

            action_list_helper = OAM_Functions.Action_List_Helper(obj)

            action = action_list_helper.get_action(self.index) 


            if action:
                
                for scene_object in scn.objects:

                    scn_action_list_helper = OAM_Functions.Action_List_Helper(scene_object)

                    if self.check_all:
                        check_action_list = scn_action_list_helper.collect_action_list()
                        if action in check_action_list:
                            chosen_objects.append(scene_object)
                        
                    else:
                        check_action = scn_action_list_helper.get_active_action()
                        if check_action == action:
                            chosen_objects.append(scene_object)

                   



        toogle_check = not any([object.select_get() for object in chosen_objects])


        if len(chosen_objects) > 0:
            if obj in chosen_objects:
            
                context.view_layer.objects.active = obj
            else:
                context.view_layer.objects.active = chosen_objects[0]

        for object in chosen_objects:
            object.select_set(toogle_check)




        return {'FINISHED'}


classes = [FR_OT_OAM_Select_Object_With_Action]


def register():

    for cls in classes:
        bpy.utils.register_class(cls)



def unregister():

    for cls in classes:
        bpy.utils.unregister_class(cls)



if __name__ == "__main__":
    register()
