import bpy
from Frame_Ranger import Utility_Function

from Frame_Ranger.Utility_Function import OAM_Functions
from Frame_Ranger.Utility_Function import Pose_Marker_Functions


Rename_Mode = [("PREFIX","Prefix","Prefix"),("SUFFIX","Suffix","Suffix"),("REPLACE","Replace","Replace"),("REMOVE","Remove","Remove")]

class FR_OT_PMM_Batch_Rename_Pose_Markers(bpy.types.Operator):

    bl_idname = "fr_pmm.batch_rename_markers"
    bl_label = "Batch Rename Pose Markers"
    bl_description = "Batch Rename Pose Markers"
    bl_options = {'UNDO', 'REGISTER'}
    
    mode: bpy.props.EnumProperty(items=Rename_Mode)

    string_a: bpy.props.StringProperty()
    string_b: bpy.props.StringProperty()

    selected_only: bpy.props.BoolProperty()
    target_action: bpy.props.StringProperty()

    def draw(self, context):
        layout = self.layout

        layout.prop(self, "mode", text="Mode")
        if self.mode == "PREFIX":
            layout.prop(self, "string_a", text="Prefix")
        if self.mode == "SUFFIX":
            layout.prop(self, "string_a", text="Suffix")
        if self.mode == "REPLACE":
            layout.prop(self, "string_a", text="Find")
            layout.prop(self, "string_b", text="Replace")
        if self.mode == "REMOVE":
            layout.prop(self, "string_a", text="Remove")

        layout.prop(self, "selected_only", text="Selected Only")

    def invoke(self, context, event):

        return context.window_manager.invoke_props_dialog(self)


    def execute(self, context):


        scn = context.scene
        
        action = bpy.data.actions.get(self.target_action) 
        if action is not None:
            Pose_Marker_Functions.batch_rename_pose_markers(action, self.mode, string_a=self.string_a, string_b=self.string_b, check_select=self.selected_only)


        Utility_Function.update_UI()

        return {'FINISHED'}


classes = [FR_OT_PMM_Batch_Rename_Pose_Markers]


def register():

    for cls in classes:
        bpy.utils.register_class(cls)



def unregister():

    for cls in classes:
        bpy.utils.unregister_class(cls)



if __name__ == "__main__":
    register()
