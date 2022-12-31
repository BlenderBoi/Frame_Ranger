import bpy

from Frame_Ranger import Utility_Function
from Frame_Ranger.Utility_Function import OAM_Functions

def Update_Range_Start(self, context):

    if self.Start > self.End:
        self.End = self.Start

def Update_Range_End(self, context):

    if self.End < self.Start:
        self.Start = self.End


class FR_OT_OAM_Load_Action_Slot(bpy.types.Operator):

    bl_idname = "fr_oam.load_action_slot"
    bl_label = "Load Action"
    bl_description = "Load Action"
    bl_options = {"REGISTER", "UNDO"}

    load_action_name: bpy.props.StringProperty()
    target_object: bpy.props.StringProperty()

    show_options: bpy.props.BoolProperty(default=False)

    def invoke(self, context, event):

        if self.show_options:

            return context.window_manager.invoke_props_dialog(self)

        else:

            return self.execute(context)

    def draw(self, context):
        layout = self.layout
        layout.prop_search(self, "load_action_name", bpy.data, "actions", text="Action")

    def execute(self, context):


        preferences = Utility_Function.get_addon_preferences()
        
        scn = context.scene
        obj = bpy.data.objects.get(self.target_object) 
        action = bpy.data.actions.get(self.load_action_name)


        if obj is not None:

            if action is not None:


                action_list_helper = OAM_Functions.Action_List_Helper(obj)
                slot =  action_list_helper.load_action(action, use_fake_user=True, update_index=True)

                if slot is not None:
                    self.report({"INFO"}, action.name + " is Loaded to " + obj.name)
                else:
                    self.report({"INFO"}, action.name + " already exist and loaded in " + obj.name + ", skip operation ")



        Utility_Function.update_UI()

        return {'FINISHED'}


classes = [FR_OT_OAM_Load_Action_Slot]


def register():

    for cls in classes:
        bpy.utils.register_class(cls)



def unregister():

    for cls in classes:
        bpy.utils.unregister_class(cls)



if __name__ == "__main__":
    register()
