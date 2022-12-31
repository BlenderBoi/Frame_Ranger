import bpy

from Frame_Ranger import Utility_Function
from Frame_Ranger.Utility_Function import OAM_Functions
from Frame_Ranger.Utility_Function import Pose_Marker_Functions


ENUM_Find_Mode = [("SUFFIX", "Suffix", "Suffix"),("PREFIX","Prefix","Prefix"), ("INCLUDE", "Include", "Include")]

class FR_OT_OMM_Find_And_Set_All_Actions_Range_Marker(bpy.types.Operator):
    """Find and Set All Action's Range Markers"""
    bl_idname = "fr_oam.find_all_actions_range_markers"
    bl_label = "Find and Set Marker As Range"
    bl_options = {'UNDO', 'REGISTER'}

    find_mode: bpy.props.EnumProperty(items=ENUM_Find_Mode)

    find_a: bpy.props.BoolProperty(default=True)
    find_b: bpy.props.BoolProperty(default=True)
    marker_a_find: bpy.props.StringProperty(default="_start")
    marker_b_find: bpy.props.StringProperty(default="_end")

    target_object: bpy.props.StringProperty()


    def draw(self, context):
        scn = context.scene

        layout = self.layout
        layout.prop(self, "find_mode", text="Find")



        layout.prop(self, "find_a", text="Find Marker A") 

        if self.find_a:
            layout.prop(self, "marker_a_find", text="Marker A")


        layout.prop(self, "find_b", text="Find Marker B") 

        if self.find_b:
            layout.prop(self, "marker_b_find", text="Marker B")


    def invoke(self, context, event):

        return context.window_manager.invoke_props_dialog(self)


    def execute(self, context):

        scn = context.scene


        obj = bpy.data.objects.get(self.target_object) 

        if obj is not None:
            action_list_helper = OAM_Functions.Action_List_Helper(obj)
            action_list = action_list_helper.collect_action_list()

            for action in action_list:
                if action is not None:
                    Pose_Marker_Functions.find_and_set_range_markers(action, self.find_mode, self.find_a, self.marker_a_find, self.find_b, self.marker_b_find)


        Utility_Function.update_UI()

        return {'FINISHED'}


classes = [FR_OT_OMM_Find_And_Set_All_Actions_Range_Marker]


def register():

    for cls in classes:
        bpy.utils.register_class(cls)



def unregister():

    for cls in classes:
        bpy.utils.unregister_class(cls)



if __name__ == "__main__":
    register()
