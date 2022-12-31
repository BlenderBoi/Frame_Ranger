import bpy

from Frame_Ranger import Utility_Function
from bpy.types import Preferences
from Frame_Ranger.Utility_Function import OAM_Functions
from Frame_Ranger.Utility_Function import Pose_Marker_Functions



ENUM_Mode = [("DOWN", "Down", "Down"),("UP", "Up", "Up")]

class FR_OT_PMM_Reorder_Pose_Marker(bpy.types.Operator):
    """Reorder Pose Marker"""
    bl_idname = "fr_pmm.reorder_pose_marker"
    bl_label = "Reorder Pose Marker"
    bl_options = {'UNDO', 'REGISTER'}
    
    index: bpy.props.IntProperty()
    mode: bpy.props.EnumProperty(items=ENUM_Mode)
    target_action: bpy.props.StringProperty()

    disable_warning: bpy.props.BoolProperty(default=True)

    def invoke(self, context, event):

        preferences = Utility_Function.get_addon_preferences()

        if preferences.OAM_Pose_Marker_Warning:
            return context.window_manager.invoke_props_dialog(self)
        else:
            return self.execute(context)


    def draw(self, context):
        layout = self.layout
        layout.label(text="This Operator: ", icon="ERROR")
        box = layout.box()
        box.label(text="Removes All Markers and Recreating it", icon="ERROR")
        box.label(text="Depending on the Situation, It might be destructive")
        box = layout.box()
        box.label(text="You Might Lose All Your Markers", icon="ERROR")
        box.label(text="If this Operator Fails Halfway")
        layout.prop(self, "disable_warning", text="Disable Warning")

    def execute(self, context):

        
        preferences = Utility_Function.get_addon_preferences()

        if preferences.OAM_Pose_Marker_Warning:
            if self.disable_warning:
                preferences.OAM_Pose_Marker_Warning = False


        action = bpy.data.actions.get(self.target_action) 
        
        if action is not None:
            pose_markers_index = action.pose_markers_index 

            proto_markers = []
            
            for pose_marker in action.pose_markers:
                proto_marker = Pose_Marker_Functions.collect_marker_data(pose_marker, type="POSEMARKER")
                proto_markers.append(proto_marker)



            if self.mode == "UP":
                if self.index-1 >= 0:

                    Pose_Marker_Functions.clear_pose_markers(action)
                    item = proto_markers.pop(self.index)
                    proto_markers.insert(self.index-1, item)
                    Pose_Marker_Functions.recreate_pose_markers(proto_markers, action)
                    action.pose_markers_index = pose_markers_index

                Pose_Marker_Functions.index_up(action)

            if self.mode == "DOWN":
                if self.index+1 < len(proto_markers):
                    Pose_Marker_Functions.clear_pose_markers(action)
                    item = proto_markers.pop(self.index)
                    proto_markers.insert(self.index+1, item)
                    # proto_markers = Utility_Function.list_swap_item(proto_markers, self.Index-1, self.Index)
                    Pose_Marker_Functions.recreate_pose_markers(proto_markers, action)
                    action.pose_markers_index = pose_markers_index
                Pose_Marker_Functions.index_down(action)


        Utility_Function.update_UI()

        return {'FINISHED'}


classes = [FR_OT_PMM_Reorder_Pose_Marker]


def register():

    for cls in classes:
        bpy.utils.register_class(cls)



def unregister():

    for cls in classes:
        bpy.utils.unregister_class(cls)



if __name__ == "__main__":
    register()
