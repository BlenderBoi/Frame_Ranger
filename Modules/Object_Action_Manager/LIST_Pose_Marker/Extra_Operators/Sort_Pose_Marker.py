
import bpy

from Frame_Ranger import Utility_Function
from bpy.types import Preferences

from Frame_Ranger.Utility_Function import OAM_Functions
from Frame_Ranger.Utility_Function import Pose_Marker_Functions



ENUM_Mode = [("DOWN", "Down", "Down"),("UP", "Up", "Up")]
ENUM_Sort_By = [("FRAME","Frame","Frame"),("NAME","Name","Name")]

class FR_OT_PMM_Sort_Pose_Marker(bpy.types.Operator):
    """Sort Pose Marker"""
    bl_idname = "fr_pmm.sort_pose_markers"
    bl_label = "Sort Pose Marker"
    bl_options = {'UNDO', 'REGISTER'}
    
    sort_by: bpy.props.EnumProperty(items=ENUM_Sort_By)
    reversed: bpy.props.BoolProperty(default=False)
    disable_warning: bpy.props.BoolProperty(default=False)
    target_action: bpy.props.StringProperty()

    def invoke(self, context, event):

        preferences = Utility_Function.get_addon_preferences()

        return context.window_manager.invoke_props_dialog(self)


    def draw(self, context):
        layout = self.layout
        layout.label(text="Sort By")
        layout.prop(self, "sort_by", text="")
        layout.prop(self, "reversed", text="Reverse")
        layout.prop(self, "disable_warning", text="Disable Warning")


        if not self.disable_warning:
            layout.label(text="This Operator: ", icon="ERROR")
            box = layout.box()
            box.label(text="Removes All Markers and Recreating it", icon="ERROR")
            box.label(text="Depending on the Situation, It might be destructive")
            box = layout.box()
            box.label(text="You Might Lose All Your Markers", icon="ERROR")
            box.label(text="If this Operator Fails Halfway")

    def execute(self, context):

        scn = context.scene
        
        preferences = Utility_Function.get_addon_preferences()


        action = bpy.data.actions.get(self.target_action) 
        
        if action:
            pose_markers_index = action.pose_markers_index 

            proto_markers = []

            
            for pose_marker in action.pose_markers:
                proto_marker = Pose_Marker_Functions.collect_marker_data(pose_marker, type="POSEMARKER")
                proto_markers.append(proto_marker)

            Pose_Marker_Functions.clear_pose_markers(action)

            if self.sort_by == "NAME":
                proto_markers = sorted(proto_markers, key=lambda item: item.name, reverse=self.reversed)
            if self.sort_by == "FRAME":
                proto_markers = sorted(proto_markers, key=lambda item: item.frame, reverse=self.reversed)
            #
            Pose_Marker_Functions.recreate_pose_markers(proto_markers, action)
            action.pose_markers_index = pose_markers_index



        Utility_Function.update_UI()

        return {'FINISHED'}


classes = [FR_OT_PMM_Sort_Pose_Marker]


def register():

    for cls in classes:
        bpy.utils.register_class(cls)



def unregister():

    for cls in classes:
        bpy.utils.unregister_class(cls)



if __name__ == "__main__":
    register()
