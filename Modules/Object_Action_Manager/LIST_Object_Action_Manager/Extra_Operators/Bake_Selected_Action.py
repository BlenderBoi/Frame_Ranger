import bpy

from Frame_Ranger import Utility_Function
from Frame_Ranger.Utility_Function import OAM_Functions
from bpy_extras import anim_utils




ENUM_Bake_Target = [("NEW","Bake to New Action","Bake to New Action"), ("SELF", "Bake to Self", "Bake to Self")]
ENUM_Rename_Mode = [("SUFFIX","Suffix","Suffix"),("PREFIX","Prefix","Prefix"),("REPLACE","Replace","Replace")]

class FR_OT_OAM_Bake_Selected_Action(bpy.types.Operator):
    """Bake Selected Action"""
    bl_idname = "fr_oam.bake_selected_action"
    bl_label = "Bake Selected Slot"
    bl_options = {"REGISTER", "UNDO"}



    bake_target: bpy.props.EnumProperty(items=ENUM_Bake_Target)
    replace: bpy.props.BoolProperty(default=True)
    move_to_bottom: bpy.props.BoolProperty(default=True)

    only_selected: bpy.props.BoolProperty(default=False)
    do_pose: bpy.props.BoolProperty(default=True)
    do_object: bpy.props.BoolProperty(default=False)
    do_visual_keying: bpy.props.BoolProperty(default=True)
    do_constraint_clear: bpy.props.BoolProperty(default=False)
    do_parents_clear: bpy.props.BoolProperty(default=False)
    do_clean: bpy.props.BoolProperty(default=False)

    show_bake_settings: bpy.props.BoolProperty()


    rename_mode: bpy.props.EnumProperty(items=ENUM_Rename_Mode)
    string_a: bpy.props.StringProperty(default="_bake")
    string_b: bpy.props.StringProperty()

    use_bake_name_when_available: bpy.props.BoolProperty(default=True)

    use_fake_user: bpy.props.BoolProperty(default=True)

    target_object: bpy.props.StringProperty()

    def draw_rename_settings(self, layout):
        col = layout.column(align=True)

        col.label(text="Rename")
        row = col.row(align=True)
        row.prop(self, "rename_mode", expand=True) 

        if self.rename_mode == "REPLACE":
            col.prop(self, "string_a", text="From") 
            col.prop(self, "string_b", text="To") 

        if self.rename_mode == "SUFFIX":
            col.prop(self, "string_a", text="Suffix") 

        if self.rename_mode == "PREFIX":
            col.prop(self, "string_a", text="Prefix") 

        col.separator()
        col.prop(self, "use_bake_name_when_available", text="Use Bake Name When Available") 
        col.prop(self, "use_fake_user", text="Use Fake User") 
        col.separator()

    def draw(self, context):



        layout = self.layout

        layout.prop(self, "bake_target", expand=True)

        if self.bake_target == "NEW":
            
            layout.prop(self, "replace", text="Replace if Exist") 
            layout.prop(self, "move_to_bottom", text="Move Slot to Bottom") 

            self.draw_rename_settings(layout)
        
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

        obj = bpy.data.objects.get(self.target_object) 

        if obj.type == "ARMATURE":
            self.do_pose = True
            self.do_object = False
        else:
            self.do_pose = False
            self.do_object = True




        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):

        scn = context.scene
        obj = bpy.data.objects.get(self.target_object) 

        if obj is not None:

            action_list_helper = OAM_Functions.Action_List_Helper(obj)

            bake_settings = {}

            bake_settings["only_selected"] = self.only_selected
            bake_settings["do_pose"] = self.do_pose
            bake_settings["do_object"] = self.do_object
            bake_settings["do_visual_keying"] = self.do_visual_keying   
            bake_settings["do_constraint_clear"] = self.do_constraint_clear
            bake_settings["do_parents_clear"] = self.do_parents_clear
            bake_settings["do_clean"] = self.do_clean


            batch_rename_dict = {}

            batch_rename_dict["mode"] = self.rename_mode
            batch_rename_dict["string_a"] = self.string_a
            batch_rename_dict["string_b"] = self.string_b



            if self.bake_target == "NEW":
                copy = True
            if self.bake_target == "SELF":
                copy = False 


            action_list_helper.bake_selected(bake_settings, batch_rename_dict, copy, replace=self.replace, use_fake_user=self.use_fake_user, update_index=True, move_to_bottom=self.move_to_bottom, use_bake_name_if_available=self.use_bake_name_when_available)


                    

        return {'FINISHED'}


classes = [FR_OT_OAM_Bake_Selected_Action]


def register():

    for cls in classes:
        bpy.utils.register_class(cls)



def unregister():

    for cls in classes:
        bpy.utils.unregister_class(cls)



if __name__ == "__main__":
    register()
