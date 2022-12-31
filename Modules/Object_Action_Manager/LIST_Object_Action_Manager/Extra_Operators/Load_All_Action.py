
import bpy
from Frame_Ranger import Utility_Function
from bpy.types import Preferences
from Frame_Ranger.Utility_Function import OAM_Functions


ENUM_Mode = [("ALL","All","All"),("INCLUDE","Name Include","Name Exclude"),("EXCLUDE","Name Exclude","Name Exclude")]

class FR_OT_OAM_Load_All_Action(bpy.types.Operator):
    """Load All Action"""
    bl_idname = "fr_oam.load_all_action"
    bl_label = "Load All Action"
    bl_options = {'UNDO', 'REGISTER'}

    filter_mode: bpy.props.EnumProperty(items=ENUM_Mode)
    filter: bpy.props.StringProperty()

    show_detected: bpy.props.BoolProperty(default=True)
    target_object: bpy.props.StringProperty()

    show_options: bpy.props.BoolProperty(default=True)

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "filter_mode", expand=True)

        if self.filter_mode == "INCLUDE":
            layout.prop(self, "filter", text="Include")

        if self.filter_mode == "EXCLUDE":
            layout.prop(self, "filter", text="Exclude")
            
        if self.filter_mode in ["INCLUDE", "EXCLUDE"]:

            if Utility_Function.draw_subpanel(layout, "Detected Actions", self, "show_detected"):
                
                actions_to_load = self.get_action_to_load(context)

                box = layout.box()

                if len(actions_to_load) > 0:
                    
                    for action in actions_to_load:

                        box.label(text=action.name, icon="ACTION")

                else:
                    box.label(text="No Action Detected", icon="INFO")

    def invoke(self, context, event):

        if self.show_options:

            return context.window_manager.invoke_props_dialog(self)

        else:

            return self.execute(context)

    def get_action_to_load(self, context):

        actions_to_load = []

        for action in bpy.data.actions:

            if self.filter_mode == "ALL":
                actions_to_load.append(action)

            if self.filter_mode in ["INCLUDE", "EXCLUDE"]:

                if self.filter == "":
                    actions_to_load.append(action)
                
                else:

                    if self.filter_mode == "INCLUDE":

                        check_a = self.filter
                        check_b = action.name

                        check_a = check_a.lower()
                        check_b = check_b.lower()

                        if check_a in check_b:
                            actions_to_load.append(action)

                    if self.filter_mode == "EXCLUDE":

                        check_a = self.filter
                        check_b = action.name

                        check_a = check_a.lower()
                        check_b = check_b.lower()

                        if not check_a in check_b:
                            actions_to_load.append(action)

        return actions_to_load

    def execute(self, context):


        preferences = Utility_Function.get_addon_preferences()

        scn = context.scene
        obj = bpy.data.objects.get(self.target_object) 

        if obj is not None:

            action_list_helper = OAM_Functions.Action_List_Helper(obj)
            actions_to_load = self.get_action_to_load(context)

            for action in actions_to_load:


                slot =  action_list_helper.load_action(action, use_fake_user=True, update_index=True)

                if slot is not None:
                    self.report({"INFO"}, action.name + " is Loaded to " + obj.name)
                else:
                    self.report({"INFO"}, action.name + " already exist and loaded in " + obj.name + ", skip operation ")




        Utility_Function.update_UI()

        return {'FINISHED'}


classes = [FR_OT_OAM_Load_All_Action]


def register():

    for cls in classes:
        bpy.utils.register_class(cls)



def unregister():

    for cls in classes:
        bpy.utils.unregister_class(cls)



if __name__ == "__main__":
    register()
