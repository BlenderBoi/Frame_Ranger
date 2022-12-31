import bpy

from Frame_Ranger import Utility_Function
from Frame_Ranger.Utility_Function import OAM_Functions
from bpy_extras import anim_utils

ENUM_Bake_Target = [("NEW","Bake to New Action","Bake to New Action"), ("SELF", "Bake This Action", "Bake This Action")]

class FR_OT_OAM_Bake_Action(bpy.types.Operator):
    """Bake This Action"""
    bl_idname = "fr_oam.bake_action"
    bl_label = "Bake Action Slot"
    bl_options = {"REGISTER", "UNDO"}

    name: bpy.props.StringProperty()
    index: bpy.props.IntProperty()

    # Load: bpy.props.BoolProperty(default=True)
    # Replace_Slot: bpy.props.BoolProperty(default=False)
    bake_target: bpy.props.EnumProperty(items=ENUM_Bake_Target)

    replace: bpy.props.BoolProperty(default=True)
    use_action: bpy.props.BoolProperty(default=False)

    only_selected: bpy.props.BoolProperty(default=False)
    do_pose: bpy.props.BoolProperty(default=True)
    do_object: bpy.props.BoolProperty(default=False)
    do_visual_keying: bpy.props.BoolProperty(default=True)
    do_constraint_clear: bpy.props.BoolProperty(default=False)
    do_parents_clear: bpy.props.BoolProperty(default=False)
    do_clean: bpy.props.BoolProperty(default=False)

    show_bake_settings: bpy.props.BoolProperty()


    target_object: bpy.props.StringProperty()


    def draw(self, context):

        layout = self.layout

        layout.prop(self, "bake_target", expand=True)

        if self.bake_target == "NEW":
            
            row = layout.row(align=True)
            if self.replace:

                if self.use_action:
                    row.prop_search(self, "name", bpy.data, "actions", text="")
                else:
                    row.prop(self, "name", text="Name")

                row.prop(self, "use_action", text="", icon="ACTION")

            else:
                row.prop(self, "name", text="Name")


            layout.prop(self, "replace", text="Replace if Exist") 
            
        
        box = layout.box()
        if Utility_Function.draw_subpanel(box, "Bake Settings", self, "show_bake_settings"):

            box.prop(self, "only_selected", text="Only Selected Bone")
            box.prop(self, "do_pose", text="Bake Pose")
            box.prop(self, "do_object", text="Bake Object")
            box.prop(self, "do_visual_keying", text="Visual Keying")
            box.prop(self, "do_constraint_clear", text="Constraint Clear")
            box.prop(self, "do_parents_clear", text="Parent Clear")
            box.prop(self, "do_clean", text="Clean")


    def invoke(self, context, event):


        scn = context.scene
        obj = bpy.data.objects.get(self.target_object) 
       
        if obj is not None:

            action_list_helper = OAM_Functions.Action_List_Helper(obj)
            slot = action_list_helper.get_slot(self.index)

            if slot is not None:
                action = slot.action
            else:
                action = None



            if obj.type == "ARMATURE":
                self.do_pose = True
                self.do_object = False
            else:
                self.do_pose = False
                self.do_object = True


            if action is not None:
                if not action.fr_settings.bake_name == "":
                    self.name = action.fr_settings.bake_name

                else:
                    self.name = action.name + "_baked"


            else:
                self.report({"INFO"}, "No Action to Bake")


            return context.window_manager.invoke_props_dialog(self)

        else: 
            self.report({"INFO"}, "No Object to Bake")

        self.report({"INFO"}, "Operation Terminated")
        return {'FINISHED'}



    def execute(self, context):


        scn = context.scene
        obj = bpy.data.objects.get(self.target_object) 

        if obj is not None:

            action_list_helper = OAM_Functions.Action_List_Helper(obj)

            slot = action_list_helper.get_slot(self.index)

            if slot is not None:

                action = slot.action

                if action is not None:

                    action_list_helper.set_active_index(self.index, sync=True)
                    
                    frame_ranges = action_list_helper.get_slot_frame_range(slot, use_curve_range=False)

                    start_frame = int(frame_ranges[0])
                    end_frame = int(frame_ranges[1])

                    bake_settings = {}

                    bake_settings["only_selected"] = self.only_selected
                    bake_settings["do_pose"] = self.do_pose
                    bake_settings["do_object"] = self.do_object
                    bake_settings["do_visual_keying"] = self.do_visual_keying   
                    bake_settings["do_constraint_clear"] = self.do_constraint_clear
                    bake_settings["do_parents_clear"] = self.do_parents_clear
                    bake_settings["do_clean"] = self.do_clean
       
                    copy = False

                    if self.bake_target == "NEW":
                        copy = True
                    if self.bake_target == "SELF":
                        copy = False 

                    action_list_helper.bake_slot_by_index(self.index, bake_settings, copy, name=self.name, replace=self.replace, move_to_bottom=False)
            


                    

        return {'FINISHED'}


classes = [FR_OT_OAM_Bake_Action]


def register():

    for cls in classes:
        bpy.utils.register_class(cls)



def unregister():

    for cls in classes:
        bpy.utils.unregister_class(cls)



if __name__ == "__main__":
    register()
