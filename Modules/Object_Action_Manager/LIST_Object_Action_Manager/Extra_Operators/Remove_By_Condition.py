
import bpy

from Frame_Ranger import Utility_Function
from Frame_Ranger.Utility_Function import OAM_Functions



ENUM_Condition = [("NAME","Name","Name"), ("SIZE","Range Size","Frame Range Size")]
ENUM_Mode_Name = [("INCLUDE","Include","Include"),("EXCLUDE","Exclude","Exclude")]
ENUM_Mode_Operator = [("GREATER","Greater or Equal","Greater or Equal"),("LESSER","Lesser or Equal","Lesser or Equal"), ("EQUAL","Equal","Equal")]

class FR_OT_OAM_Remove_By_Condition(bpy.types.Operator):
    """Remove By Condition"""
    bl_idname = "fr_oam.remove_by_condition"
    bl_label = "Remove By Condition"
    bl_options = {"REGISTER", "UNDO"}

    condition: bpy.props.EnumProperty(items=ENUM_Condition)

    # Mode_Name: bpy.props.EnumProperty(items=ENUM_Mode_Name)
    # Search_Name: bpy.props.StringProperty()

    search_mode: bpy.props.EnumProperty(items=ENUM_Mode_Name)
    search_name: bpy.props.StringProperty()

    search_size: bpy.props.IntProperty(min=0)

    # Mode_Operator: bpy.props.EnumProperty(items=ENUM_Mode_Operator)
    search_operator: bpy.props.EnumProperty(items=ENUM_Mode_Operator)

    use_curve_frame_range: bpy.props.BoolProperty(default=False)

    show_detected: bpy.props.BoolProperty(default=True)

    remove_action: bpy.props.BoolProperty(default=False)


    target_object: bpy.props.StringProperty()

    def draw(self, context):


        layout = self.layout
        layout.prop(self, "condition", text="Condition")

        if self.condition == "NAME":
            layout.prop(self, "search_mode", expand=True)
            layout.prop(self, "search_name", text="")

        if self.condition == "SIZE":
            layout.prop(self, "search_operator", text="")
            layout.prop(self, "search_size", text="Frame Range Size")
            layout.prop(self, "use_curve_frame_range", text="Use Curve Frame Range")
            

        layout.prop(self, "remove_action", text="Remove Action")
        

        obj = bpy.data.objects.get(self.target_object) 
        
        if obj is not None:
            self.draw_match(context, layout, obj)

    def draw_match(self, context, layout, obj):

        action_list_helper = OAM_Functions.Action_List_Helper(obj)
        action_list = action_list_helper.get_action_list()


        if Utility_Function.draw_subpanel(layout, "Show Detected", self, "show_detected"):

            box = layout.box()
            
            detected_actions = self.detect_action(context, obj)

            if len(detected_actions) > 0:

                for action in detected_actions:

                    if self.condition == "NAME":

                        box.label(text=action.name, icon="ACTION")

                    if self.condition == "SIZE":

                        row = box.row()
                        row.label(text=action.name, icon="ACTION")


                        if action.use_frame_range:

                            start = int(action.frame_start)
                            end = int(action.frame_end)

                        else:
                            start = int(action.curve_frame_range[0])
                            end = int(action.curve_frame_range[1])


                        if self.use_curve_frame_range:

                            start = int(action.curve_frame_range[0])
                            end = int(action.curve_frame_range[1])

                        size = Utility_Function.calculate_range_size(start, end)

                        row.label(text="Size: " + str(size))

            else:

                box.label(text="No Match", icon="INFO")



    def detect_action(self, context, obj):

        action_list_helper = OAM_Functions.Action_List_Helper(obj)
        action_list = action_list_helper.get_action_list()

        detected_actions = []

        if action_list is not None:

            for index, slot in enumerate(action_list):

                action = slot.action

                if action:

                    if self.condition == "NAME":
                        if not self.search_name == "":

                            search_name = self.search_name
                            action_name = action.name

                            search_name = search_name.lower()
                            action_name = action_name.lower()

                            if self.search_mode == "INCLUDE":

                                if search_name in action_name:

                                    detected_actions.append(action)

                            if self.search_mode == "EXCLUDE":

                                if not search_name in action_name:

                                    detected_actions.append(action)

                    if self.condition == "SIZE":

                        size = action_list_helper.calculate_slot_range_size_by_index(index, use_curve_range=self.use_curve_frame_range)
                        
                        if self.search_operator == "GREATER":
                            if size >= self.search_size:
                                detected_actions.append(action)

                        if self.search_operator == "LESSER":
                            if size <= self.search_size:
                                detected_actions.append(action)

                        if self.search_operator== "EQUAL":
                            if size == self.search_size:
                                detected_actions.append(action)

        return detected_actions

















    def invoke(self, context, event):

        return context.window_manager.invoke_props_dialog(self)


    def execute(self, context):



        obj = bpy.data.objects.get(self.target_object) 

        if obj is not None:
            bpy.ops.fr_oam.clean_action_list(target_object=obj.name)

            action_list_helper = OAM_Functions.Action_List_Helper(obj)
            action_list = action_list_helper.get_action_list()
            detected_actions = self.detect_action(context, obj)

           
            for loop in action_list:
                for index, slot in enumerate(action_list):
                    
                    if slot.action in detected_actions:
                        action_list_helper.remove_slot(index, remove_action=self.remove_action, sync=True)
                        break 



        Utility_Function.update_UI()

        return {'FINISHED'}

classes = [FR_OT_OAM_Remove_By_Condition]


def register():

    for cls in classes:
        bpy.utils.register_class(cls)



def unregister():

    for cls in classes:
        bpy.utils.unregister_class(cls)



if __name__ == "__main__":
    register()
